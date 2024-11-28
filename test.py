import requests
import json

def test_query():
    url = "http://localhost:8000/query"
    
    # Test data
    payload = {
        "query": "What courses are available?",
        "conversation_id": "test-1",
        "chat_history": []
    }
    
    # Make request
    response = requests.post(url, json=payload)
    
    # Print results
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))

def test_webhook():
    url = "http://localhost:8000/webhook"
    
    # Test data
    payload = {
        "message": "Tell me about the available courses",
        "conversation_id": "test-1",
        "chat_history": []
    }
    
    # Make request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    # Print results
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))

def test_query_with_history():
    url = "http://localhost:8000/query"
    
    # Test data with chat history
    payload = {
        "query": "What are the cost for this course and can you provide me link to it?",
        "conversation_id": "test-1",
        "chat_history": [
            {
                "human": "What courses are available?",
                "ai": "Yes! Telescopic handler (Telehandler, Manitou) course is avaliable."
            }
        ]
    }
    
    # Make request
    response = requests.post(url, json=payload)
    
    # Print results
    print("\nTesting Query with History:")
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing Query Endpoint:")
    test_query()
    print("\nTesting Webhook Endpoint:")
    test_webhook()
    test_query_with_history()