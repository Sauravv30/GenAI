from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

groq_model = ChatGroq(model="Gemma2-9b-It")
prompt_template = ChatPromptTemplate([
    ('system', 'Translate the following from English to {language}'),
    ('user', '{input}')
])
parser = StrOutputParser()

chain = prompt_template | groq_model | parser
app = FastAPI(title="Langchain Server", version="1.0", description="Api integration the langchain")

# Adding chain
add_routes(app=app, runnable=chain, path="/chain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

