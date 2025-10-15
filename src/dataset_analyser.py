from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict, Any, Annotated
import pandas as pd


#load env file for secure API key
load_dotenv("../Langchain/.env")

#initialize llm
llm = ChatGoogleGenerativeAI(
            temperature = 0,
            model = "gemini-2.5-flash"
)

#load Dataset
df = pd.read_csv("employees.csv")

#define data structure
class State(TypedDict):
    metadata: Annotated[dict, ... , "Stores dataset overview"]
    query: Annotated[str, ..., "The user’s input question about the dataset"]
    generated_code: Annotated[str, ..., "pandas expression to answer the user query"]
    answer: Annotated[Any, ..., "The output obtained by executing the generated pandas expression"]
    final_output: Annotated[Any, ..., "The final human-readable explanation of the output"]


# Runnable 1 to get the metadata about dataset
def get_dataset_overview(state: State) -> State:
    """
    Expects state to contain 'query' (direct access: state['query']).
    Attaches 'metadata' and returns the full state.

    """
    df_shape = {
                    "Rows": df.shape[0],
                    "Columns": df.shape[1]
                }
    
    df_columns = df.columns

    df_head = df.head(5)
    
    df_duplicates = df.duplicated().sum()
    unique_value = pd.DataFrame({
            "Columns": df.columns,
            "Unique_Values": [df[col].unique().tolist() for col in df.columns]
    })

    metadata = {
        "shape" : df_shape,
        "df_columns" : df_columns,
        "head" : df_head.to_dict(orient='records'),
        "total no of duplicates" : df_duplicates,
        "unique_vlues" : unique_value.to_dict(orient='records') } 
    
    state['metadata'] = metadata
    return state


# Runnable 2 to generate pandas expression using python
def generate_code(state: State) -> State:
    """
    Expects state to already contain 'metadata' and 'query' (direct access).
    Produces 'generated_code' (string) and attaches it to state.

    """

    metadata: dict = state['metadata']
    query: str = state['query']

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an expert python data analyst who writes a concise pandas expression"),
        ("human", '''
                    You are given dataset metadata as JSON in the variable {metadata}.\n\n
                    The metadata contains: shape, column names, a small sample of rows (head), duplicate count, and unique_values per column.\n\n
                    User query: {query}\n\n
                    Produce ONLY a single-line Python pandas expression using the variable name `df`.\n
                    Do NOT use backticks (`) or quotes around the code.\n
                    Do NOT include any explanation or text.\n
         '''
        )
    ]
    )
    parser = StrOutputParser()
    code_gen = prompt | llm | parser
    generated_code = code_gen.invoke(
        {
            "metadata" : metadata,
            "query" : query
        }
    )
    state['generated_code'] = generated_code
    return state


# Runnable 3 to execute the python code and print answer
def execute_code(state: State) -> State:
    """
    Expects state['generated_code'] to exist (direct access).
    Executes result = <generated_code> with df available and attaches 'answer' to state.

    """
    code = state['generated_code']
    local_vars = {}
    result = exec(f"result = {code}", globals(), local_vars) or local_vars['result']
    state['answer'] = result
    return state


#Runnable 4 to print the output in natural Language
def data_description(state: State) -> State:
    """
    Expects state['query'] and state['answer'] to exist (direct access).
    Calls LLM to produce a short natural-language explanation and attaches it as 'answer_explanation'.
    """
    query: str = state['query']
    result: Any = state['answer']

    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        {
        ("system",  '''
                    You are an expert data analyst and Python instructor.

                    You will be given two inputs:
                    1. User Query – the question or task the user asked.
                    2. Result – the computed output of that query.

                    Your task:
                    - Present the result neatly and in a readable format.
                    - Then explain briefly what this result means in the context of the user’s query.
                    - If it's a DataFrame or Series → display it as a small clean table.
                    - If it's a number, string, list, or dictionary → format it clearly.
                    - Keep the response professional and concise.
                      
                    '''
         ),
        ("human", ''' 
                    User Query:
                    {query}

                    Result:
                    {result}

                    Please present the result neatly and give a short explanation of what it represents.
                '''
         )       
        }
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser
    output = chain.invoke(
        {
            "query" : query,
            "result" : result
        }
    )
    state['final_output'] = output
    return state

# Create RunnableLambda wrappers for each function to build a modular processing pipeline
runnable_1 = RunnableLambda(get_dataset_overview)
runnable_2 = RunnableLambda(generate_code)
runnable_3 = RunnableLambda(execute_code)
runnable_4 = RunnableLambda(data_description)

# Final chain 
chain: RunnableSequence = RunnableSequence(
    runnable_1 | runnable_2 | runnable_3 | runnable_4
)

while True:
    query = input("Enter your query about dataset: ")
    if query=="quit":
        break
    else:

        result = chain.invoke(
            {
                'query' : query
            }
        )
        print(result['final_output'])