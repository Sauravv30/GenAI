from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import create_retriever_tool, Tool
from langchain_groq import ChatGroq

from constants import app_constants
from langchain_ollama import OllamaLLM
import os
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)

# Run query to outside world
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
# llm = OllamaLLM(model="llama3.2")
llm = ChatGroq(model=app_constants.LLM_MODEL, temperature=0.5, max_tokens=100,
               api_key=os.getenv("GROQ_API_KEY"))


def llm_search_tool(query):
    # Ensure the required parameter (__arg1, in this case `query`) is passed to llm.invoke
    if not query:
        raise ValueError(f"Query is required. {query}")
    return llm.invoke(input=query)  # Pass the query to llm.invoke()


def webTools():
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
    wiki = WikipediaQueryRun(name="WikiSearch", api_wrapper=wiki_wrapper)
    search = DuckDuckGoSearchRun(name="DuckDuckSearch", doc_content_chars_max=2000)
    llm_tool = Tool(name="llm", description="Default LLM tool search", func=llm_search_tool)
    return [llm_tool, wiki, search]


def custom_tools(retriever):
    return create_retriever_tool(name="database-search-tool", retriever=retriever,
                                 description="This is custom langchain search")


def sql_tools():
    pass
