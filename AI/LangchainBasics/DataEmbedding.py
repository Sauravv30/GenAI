# The way to convert chunks to embeddings
import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# for llama you need to download model to local machine
from dotenv import load_dotenv

# load all environment variables
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
print(os.environ["HF_TOKEN"])

# Converting text to vectors
hf_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text = "this is some text"
query = hf_embedding.embed_query(text)

print(query)
print(len(query))
