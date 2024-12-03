from langchain_huggingface import HuggingFaceEndpoint

repo = "google/gemma-2-2b-it"

llm = HuggingFaceEndpoint(
    repo_id=repo,
    max_new_tokens=512,
    # top_k=10,
    # top_p=0.95,
    # typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
    huggingfacehub_api_token=""
)
print(llm.invoke("What is Deep Learning?"))
# print(llm.invoke("Define yourself"))
