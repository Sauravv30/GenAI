from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, WikipediaLoader

loader = TextLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\test_speech.txt")
print(loader.load())

pdf_loader = PyPDFLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\resume.pdf")
print(pdf_loader.load())

csv_loader = CSVLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\data.csv")
print(csv_loader.load())

wikipedia_loader = WikipediaLoader(query="Generative AI", lang="en", load_max_docs=5)
print(wikipedia_loader.load())
