from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

#load env file for secure API key
load_dotenv("../.env")

#initialize llm
llm = ChatGoogleGenerativeAI(
            temperature = 0,
            model = "gemini-2.5-flash"
)

