import os

from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain import hub

from langchain.agents import create_openai_tools_agent, AgentExecutor

# In built tool
# We need wrapper to run the query
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)

# Run query to outside world
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
print(f"Tool name is {wiki.name}")

axiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
axiv = ArxivQueryRun(api_wrapper=axiv_wrapper)
print(f"Tool name is {axiv.name}")

# Custom tool
documents = WebBaseLoader(web_path="https://python.langchain.com/docs/concepts/").load()

# chunks
chunk_documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(documents)

# DB
hf_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(collection_name="web_loader", documents=chunk_documents, embedding=hf_embedding)
retriever = db.as_retriever()

retriever_tool = create_retriever_tool(name="langchain-tool", retriever=retriever,
                                       description="This is custom langchain search")
tools = [wiki, axiv, retriever_tool]
print(tools)

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
model = ChatGroq(model="Llama3-8b-8192")

## langchain hub, where prebuild prompt resides
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

# Agents
agent = create_openai_tools_agent(tools=tools, llm=model, prompt=prompt)
print(agent)

executor = AgentExecutor(agent=agent, tools=tools, verbos=True)
response = executor.invoke(input={"input": "Tell me about Shiva"})

print(f"response for shiva {response}")

response = executor.invoke(input={"input": "What is Retrieval in LangChain ?"})
print(f"response for langchain {response}")
