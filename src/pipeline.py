import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence
from schema import State
from config import llm
from prompts import get_code_prompt, get_plot_prompt, get_description_prompt

# Load dataset
df = pd.read_csv("../data/employees.csv")

# Runnable 1
def get_dataset_overview(state: State) -> State:
    df_shape = {"Rows": df.shape[0], "Columns": df.shape[1]}
    df_columns = df.columns
    df_head = df.head(5)
    df_duplicates = df.duplicated().sum()
    unique_value = pd.DataFrame(
        {
        "Columns": df.columns,
        "Unique_Values": [df[col].unique().tolist() for col in df.columns]
        }
        )
    metadata = {
        "shape": df_shape,
        "df_columns": df_columns,
        "head": df_head.to_dict(orient='records'),
        "total no of duplicates": df_duplicates,
        "unique_vlues": unique_value.to_dict(orient='records')
    }
    state['metadata'] = metadata
    return state


# Runnable 2
def generate_code(state: State) -> State:
    metadata = state['metadata']
    query = state['query']
    prompt = get_code_prompt()
    parser = StrOutputParser()
    code_gen = prompt | llm | parser
    generated_code = code_gen.invoke({"metadata": metadata, "query": query})
    state['generated_code'] = generated_code
    return state


# Runnable 3
def generate_plotly_plot(state: State) -> State:
    metadata = state['metadata']
    query = state['query']
    prompt = get_plot_prompt()
    parser = StrOutputParser()
    chain = prompt | llm | parser
    plotly_code = chain.invoke({"metadata": metadata, "query": query, "df": df})
    state['plotly_code'] = plotly_code
    return state


# Runnable 4
def execute_code(state: State) -> State:
    code = state['generated_code']
    plotly = state['plotly_code']
    local_vars, local_vars2 = {}, {}
    exec(f"result = {code}", globals(), local_vars)
    result = local_vars['result']
    state['answer'] = result
    exec(plotly, globals(), local_vars2)
    plotly_result = local_vars2['fig']
    state['graph'] = plotly_result
    return state


# Runnable 5
def data_description(state: State) -> State:

    query = state['query']
    result = state['answer']
    prompt = get_description_prompt()
    parser = StrOutputParser()
    chain = prompt | llm | parser
    output = chain.invoke({"query": query, "result": result})
    state['explanation'] = output
    return state


# Create chain
runnable_1 = RunnableLambda(get_dataset_overview)
runnable_2 = RunnableLambda(generate_code)
runnable_3 = RunnableLambda(generate_plotly_plot)
runnable_4 = RunnableLambda(execute_code)
runnable_5 = RunnableLambda(data_description)

chain = RunnableSequence(runnable_1 | runnable_2 | runnable_3 | runnable_4 | runnable_5)