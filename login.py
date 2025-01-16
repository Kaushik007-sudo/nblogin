import http.server
import socketserver
from pymongo import MongoClient
from urllib.parse import parse_qs, quote_plus
from werkzeug.security import check_password_hash

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

# Connect to MongoDB
client = connect_to_mongodb(MONGO_URI)
db = client["nb"]
users_collection = db["admin"]

PORT = 8000

class LoginHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            # Parse form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            # Extract email and password
            email = form_data.get('email', [None])[0]
            password = form_data.get('password', [None])[0]

            if not email or not password:
                self.respond_with_message("Missing email or password.", 400)
                return

            # Validate credentials with MongoDB
            user = users_collection.find_one({"email": email})

            if user and check_password_hash(user['password'], password):
                self.redirect_to_admin()
            else:
                self.respond_with_message("Invalid email or password.", 401)
        else:
            self.send_response(404)
            self.end_headers()

    def respond_with_message(self, message, status_code):
        """Send a plain text response."""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def redirect_to_admin(self):
        """Redirects to admin.html on successful login."""
        self.send_response(302)
        self.send_header('Location', '/admin.html')
        self.end_headers()

# Start the server
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), LoginHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
