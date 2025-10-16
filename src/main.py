from pipeline import chain
from schema import State

if __name__ =="__main__":

    while True:
        query = input("Enter your query about dataset: ")
        if query=="quit":
            break
        else:

            result: State = chain.invoke(
                {
                    'query' : query
                }
            )
            print(result['explanation'])
            print(result['generated_code'])
            print(result['answer'])
            print(result['graph'])
            print(result['plotly_code'])