from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from urllib.parse import quote_plus

# MongoDB credentials and URI
username = "kaushik"
password = "kaushik@2025"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

MONGO_URI = f"mongodb+srv://{encoded_username}:{encoded_password}@kaushik.wybs7.mongodb.net/?retryWrites=true&w=majority"

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri)
        client.admin.command("ping")  # Test connection
        print("Connected to MongoDB successfully!")
        return client
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def save_user(client, email, plaintext_password):
    try:
        db = client["nb"]  # Ensure this database exists
        users_collection = db["admin"]  # Ensure this collection exists

        # Hash the password
        hashed_password = generate_password_hash(plaintext_password)
        user_document = {
            "email": email,
            "password": hashed_password
        }

        # Insert into MongoDB
        result = users_collection.insert_one(user_document)
        print(f"User saved successfully with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error saving user: {e}")

# Main Execution
if __name__ == "__main__":
    client = connect_to_mongodb(MONGO_URI)
    if client:
        email = "itpmkaushik@gmail.com"
        plaintext_password = "test1234"
        save_user(client, email, plaintext_password)
