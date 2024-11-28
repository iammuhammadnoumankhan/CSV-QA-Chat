import os
from data_processor import DataProcessor
# from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import pandas as pd

def initialize_system():
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'CSV_FILE']
    csv_path = os.getenv("CSV_FILE")
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Initialize data processor
    processor = DataProcessor()
    
    # Process CSV if it exists
    # csv_path = "data/courses.csv"
    
    # if os.path.exists(csv_path):
    #     print("Converting CSV to SQLite database...")
    #     processor.csv_to_sqlite(csv_path)
    #     print("Creating vector store...")
    #     processor.create_vector_store(csv_path)
    # else:
    #     raise FileNotFoundError(f"CSV file not found at {csv_path}")

    try:
        # Attempt to read the CSV from the URL
        # df = pd.read_csv(csv_path)
        print("Converting CSV to SQLite database...")
        processor.csv_to_sqlite(csv_path)  # Pass the DataFrame instead of the URL
        print("Creating vector store...")
        processor.create_vector_store(csv_path)  # Pass the DataFrame instead of the URL
    except Exception as e:
        raise FileNotFoundError(f"Failed to read CSV file from {csv_path}: {e}")
    
    print("System initialized successfully!")
    return processor

if __name__ == "__main__":
    try:
        # Initialize the system
        processor = initialize_system()
        
        # Start the FastAPI server
        print("Starting FastAPI server...")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print(f"Error during startup: {str(e)}")