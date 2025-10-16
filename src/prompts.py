from langchain_core.prompts import ChatPromptTemplate

# Prompt for generating pandas expression
def get_code_prompt():
    return ChatPromptTemplate.from_messages([
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
    ])

# Prompt for generating plotly visualization
def get_plot_prompt():
    return ChatPromptTemplate.from_messages({
        ("system", ''' 
                        You're an expert data analyst who writes complete Plotly scripts to visualize dataset answers.
                        Always ensure that any code you produce:
                        - Has no unnecessary leading or trailing spaces.
                        - Starts immediately on the first line.
                        - Has correct indentation for Python.
                        - Can be safely executed with Python exec() without modification.
                        - the code SHOULD NOT included with markdown annotations like ```python, it SHOULD be pure code.
             
                        '''
        ),
        ("human", '''
                        You are given the dataset{df} metadata in {metadata} and a user query: {query}.

                        Produce a COMPLETE, ready-to-execute Python code snippet (can be multiple lines) that:
                        - imports required Plotly modules (for example: import plotly.express as px),
                        - constructs a Plotly Figure object named `fig` that visualizes the answer to the user's query using `df`,
                        - calls `fig.show()` at the end so the figure displays when executed,
                        - does NOT include extra commentary — return only the Python code as plain text.
                        Before producing code, decide whether a visualization actually adds value for the given query. 
                        If a plot is NOT appropriate (e.g., the query asks for a single scalar value such as a row count, a boolean check, or a single-cell lookup), do NOT generate a figure. 
                        Instead, return a single-line, valid Python statement that sets `fig` to None, exactly like:
                        fig = None
                        Return only that one line (no comments or extra text) so it can be executed with exec().

                        Important:
                        - Use `df` as the DataFrame variable (assume df is available in the execution environment).
                        - Make the plot appropriate for the query and the likely data types (e.g., bar for categorical counts, histogram for distribution, scatter for relationships).
                        - Keep code robust: handle common column name patterns using the metadata if helpful.
                        - Keep the code concise and practical for direct execution.
                        - You should strictly follow the same instruction for each and every run. follow the instruction carefully for code snippet format.
                        '''
             )
    })    

# Prompt for generating explanation
def get_description_prompt():
    return ChatPromptTemplate.from_messages({
        ("system", '''
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
    })