from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.pgvector import PgVector
from phi.agent import Agent

vector_database = PgVector(table_name="pdf_reader", db_url="some_db_url")

pdf_knowledge_base = PDFKnowledgeBase(
    path=r"C:/Users/Saurav/Desktop/Saurav_Verma_2025.pdf",
    reader=PDFReader(chunk=True),
    vector_db=vector_database
)

rag_agent = Agent(
    knowledge=pdf_knowledge_base,
    search_knowledge=True
)
rag_agent.knowledge.load(recreate=False)
