from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

import os 
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = init_chat_model(
    model="groq:openai/gpt-oss-120b"
) 