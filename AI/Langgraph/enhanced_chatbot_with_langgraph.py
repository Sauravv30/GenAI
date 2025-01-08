import os
from io import BytesIO

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import create_retriever_tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from typing import Annotated, List, Literal
from typing_extensions import TypedDict
from langchain_groq import ChatGroq

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchResults, TavilySearchResults
from preprocessing import PreProcessing
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wiki_tool = WikipediaQueryRun(name="wiki-search", api_wrapper=wiki_wrapper)

duck_duck_search = DuckDuckGoSearchResults(name="duck-duck-search", max_results=500)

pre_processing = PreProcessing()
custom_retriever = pre_processing.do_preprocessing(
    PyPDFLoader(file_path=r"C:\Users\Saurav\Desktop\Saurav_Verma_2025.pdf", extract_images=False).load())
#
# tavily_search = TavilySearchResults(name="tavily-search", max_results=1,
#                                     include_answer=True,
#                                     include_raw_content=True,
#                                     include_images=True, )

custom_tool = create_retriever_tool(name="db_retriever", retriever=custom_retriever,
                                    description="This is custom retriever from database")


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["db_retriever", "wiki-search", "duck-duck-search"] = Field(
        ...,
        description="Given a user question choose to route it to suitable source",
    )


# tools = [custom_tool, wiki_tool, duck_duck_search]

llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.5, max_tokens=100
               )

structured_llm_router = llm.with_structured_output(RouteQuery)

# Prompt
system = """You are an expert at routing a user question to a db_retriever, wiki-search or duck-duck-search.
The db_retriever contains documents related to person, profile, skills and projects.
Use the db_retriever for questions on these topics. Otherwise, use wiki-search or duck-duck-search for detail"""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router


def route_question(state):
    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "wiki-search":
        print("---ROUTE QUESTION TO Wiki SEARCH---")
        return "wiki_search"
    elif source.datasource == "db_retriever":
        print("---ROUTE QUESTION TO RAG---")
        return "db_retriever"


class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]

graph_builder = StateGraph(GraphState)

graph_builder.add_node("wiki_search", wiki_tool)
graph_builder.add_node("db_retriever", custom_tool)
graph_builder.add_node("web-search", duck_duck_search)

graph_builder.add_conditional_edges(START, route_question,
                                    {"wiki_search": "wiki_search", "db_retriever": "db_retriever",
                                     "web-search": 'web-search'})

# graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("wiki_search", END)
graph_builder.add_edge("db_retriever", END)
graph_builder.add_edge("web-search", END)
# Compile graph builder
graph = graph_builder.compile()

# from PIL import Image
#
# # Assuming graph.get_graph().draw_mermaid_png() returns binary PNG data
# image = Image.open(BytesIO(graph.get_graph().draw_mermaid_png()))
#
# # Save the image to a file
# image.save("output_image.png")


from pprint import pprint

# Run
inputs = {
    "question": "Summarize me about Saurav Verma"
}
for output in graph.stream(inputs):
    for key, value in output.items():
        # Node
        pprint(f"Node '{key}':")
        # Optional: print full state at each node
        # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
    pprint("\n---\n")

# Final generation
pprint(value['documents'][0].dict()['metadata']['description'])


