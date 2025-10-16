from typing import TypedDict, Any, Annotated

#define data structure
class State(TypedDict):
    metadata: Annotated[dict, ... , "Overview of the given dataset"]
    query: Annotated[str, ..., "query from the user"]
    generated_code: Annotated[str, ..., "Generated pandas expression for the given query"]
    plotly_code: Annotated[str, ..., "Full Python Plotly code to create and show the visualization for the query"]
    answer: Annotated[Any, ..., "result for the given query"]
    graph: Annotated[Any, ..., "plotly graph for the given query"]
    explanation: Annotated[Any, ..., "Explanation of the data for the answer "]

