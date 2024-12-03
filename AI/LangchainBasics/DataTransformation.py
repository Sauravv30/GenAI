from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, HTMLHeaderTextSplitter

pdf_loader = PyPDFLoader(file_path=r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\resume.pdf")
resume = pdf_loader.load()
print(type(resume))
## Recursively split text by characters, this is more generic way to do
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
split_content = text_splitter.split_documents(resume)
print(split_content[0])
print(split_content[1])

## Split with character text splitter
with open(r"E:\Workspace\Python_Workspace\GenAI\AI\test_documents\test_speech.txt") as f:
    text_file_content = f.read()

character_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10,separator="/n")
print(character_splitter.split_text(text_file_content))

html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>foo-bar</title>
</head>
<body>
  <h2>foo-bar application</h2>
  <p>Start the local server in this folder using <pre>http-server -p 3003</pre></p>
  <button id="foo">Click Foo</button>o
  <button id="bar">Click Bar</button>
  <p>See details at <a href="https://github.com/bahmutv/foo-bar">bahmutov/foo-bar</a>
  <script src="app.js"></script>
</body>
</html>'''

headers = [("h2", "header2")]
header_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers)
print(header_splitter.split_text(html))
