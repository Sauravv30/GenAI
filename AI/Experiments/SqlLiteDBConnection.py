import re
import sqlite3

import streamlit
from langchain_groq import ChatGroq
from sqlalchemy import create_engine, text

connection = None
# from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase


def sqllite():
    global connection
    try:
        connection = sqlite3.connect(uri=f"C:/Users/Saurav/Documents/sql/employee.db", database="EMPLOYEE")
        cursor = connection.cursor()

        query = """
        SELECT NAME FROM EMPLOYEE
        """

        # response = cursor.execute(query)
        # cursor.execute("INSERT INTO EMPLOYEE VALUES('Shiva', 1, 'Universe', 'Shiv Lok')")
        # cursor.execute("INSERT INTO EMPLOYEE VALUES('Shiva', 1, 'Universe', 'Shiv Lok')")
        cursor.execute("INSERT INTO EMPLOYEE VALUES('Vishnu', 2, 'Universe', 'Baikund')")
        cursor.execute("INSERT INTO EMPLOYEE VALUES('Bhrama', 3, 'Universe', 'Bhram Lok')")
        cursor.execute("INSERT INTO EMPLOYEE VALUES('Ram', 4, 'Vishnu', 'Prithvi')")
        cursor.execute("INSERT INTO EMPLOYEE VALUES('Krishna', 5, 'Vishnu', 'Prithvi')")
        cursor.execute("INSERT INTO EMPLOYEE VALUES('Hanuman', 6, 'Shiva', 'Prithvi')")

        response = cursor.execute("Select * FROM EMPLOYEE")
        print(response.rowcount)
        # rows = response.row_factory()
        for row in response:
            print(f"Row -> {row}")
        # connection.commit()
        # connection.close()
        # connection.commit()
    finally:
        if connection:
            connection.commit()
            connection.close()


def postgress():
    database_uri = "postgresql://postgres:password@localhost:5432/postgres"

    # Create SQLAlchemy engine
    engine = create_engine(database_uri)

    # Establish a connection
    with engine.connect() as conn:
        # Set the search_path for the specific schema (e.g., 'hrs-hotel')
        conn.execute(text('SET search_path TO "hrs-hotel"'))

        # You can now use the `database` object, which will operate on the `hrs-hotel` schema by default
        # Example query
        query = "DELETE FROM hotel_entity;"
        result = conn.execute(text(query)).fetchall()
        for row in result:
            print(row)


postgress()
