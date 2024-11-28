import pandas as pd
import sqlite3
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

class DataProcessor:
    def __init__(self, db_path="knowledge_base.db"):
        self.db_path = db_path
        load_dotenv()
        
    def csv_to_sqlite(self, csv_path):
        """Convert CSV to SQLite database"""
        df = pd.read_csv(csv_path)
        
        # Clean column names
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        # Create SQLite connection
        conn = sqlite3.connect(self.db_path)
        
        # Save to SQLite
        df.to_sql('courses', conn, if_exists='replace', index=False)
        conn.close()
        
    def create_vector_store(self, csv_path):
        """Create vector store for semantic search"""
        df = pd.read_csv(csv_path)
        
        # Combine relevant columns into text
        texts = df.apply(lambda row: ' '.join(row.astype(str)), axis=1).tolist()
        
        # Split texts
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200
        )
        documents = text_splitter.create_documents(texts)
        
        # Create vector store
        embeddings = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory="vectorstore"
        )
        # vectordb.persist()
        
        return vectordb

    def query_database(self, query):
        """Query SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results