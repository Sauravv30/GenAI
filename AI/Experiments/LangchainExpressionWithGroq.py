from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

groq_model = ChatGroq(model="Gemma2-9b-It")

# basic messages
messages = [
    SystemMessage(content="Translate the following from English to French"),
    # Instruction to LLM model to what to do with input ?
    HumanMessage(content="Hello, What are you doing ?")  # input to LLM
]

# output = groq_model.invoke(messages)
# print(f" from groq {output}")

parser = StrOutputParser()
# final_output = parser.invoke(output)

# print(final_output)


# Chain components together using expression languages

chain = groq_model | parser

print(f"Chain with model and parser :{chain.invoke(messages)}")

# Prompt Template
generic_message = "Translate the following from English to {Language}"

chatPrompt = ChatPromptTemplate.from_messages([
    ("system", generic_message), ("user", "{text}")
])

# print(chatPrompt.invoke({"Language": "French", "text": "How are you ?"}))

input_keys = {"Language": "French", "text": "How are you ?"}
prompt_chain = chatPrompt | groq_model | parser  # create chain from prompt templates
print(f"Chain with prompt , model and parser {prompt_chain.invoke(input_keys)}")
