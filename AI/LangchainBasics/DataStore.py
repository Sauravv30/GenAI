from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# loader = TextLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\test_speech.txt")
loader = TextLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\Projects\uploaded_pdfs\hote-booking.txt")
document = loader.load()

# Text splitter

splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=20)
splitted_doc = splitter.split_documents(document)
print(len(splitted_doc))
print(type(splitted_doc))
# Embeddnings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(splitted_doc, embeddings, persist_directory="./chrome-persistance")

query = "What is Booking Service URL ?"

# print(db.similarity_search_with_score(query=query))

print("With retrievers...")
result = db.as_retriever().invoke(query)

print(type(result))
print(result[0])