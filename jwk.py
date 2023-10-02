#Done by Rohit Kumar Shaw
#CSCE 3550
#rks0134

# Import necessary libraries and modules
from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone
from jwt.utils import base64url_encode, bytes_from_int
import json
import uuid
import jwt

# Custom request handler class inheriting from BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    JWKS = {"keys": []}  # Storage for JSON Web Key Set (JWKS)

    # HTTP methods handling
    def do_PUT(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

    def do_DELETE(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

    def do_PATCH(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

    def do_HEAD(self):
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

    # Handle GET requests
    def do_GET(self):
        if self.path == "/.well-known/jwks.json":
            self.send_response(200)  # OK
            self.end_headers()
            self.wfile.write(json.dumps(self.JWKS, indent=1).encode("UTF-8"))
            return
        else:
            self.send_response(405)  # Method Not Allowed
            self.end_headers()
            return

    # Handle POST requests
    def do_POST(self):
        if self.path in ["/auth", "/auth?expired=true", "/auth?expired=false"]:
            expired = self.path == "/auth?expired=true"
            self.send_response(200)  # OK
            self.end_headers()
            private_key = self.generate_key_pair()
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_key = private_key.public_key()
            key_id = str(uuid.uuid4())
            expiry_time = (datetime.now(tz=timezone.utc) - timedelta(seconds=3600)) if expired else (datetime.now(tz=timezone.utc) + timedelta(seconds=3600))
            jwt_token = jwt.encode({"exp": expiry_time}, private_key_bytes, algorithm="RS256", headers={"kid": key_id})
            self.wfile.write(bytes(jwt_token, "UTF-8"))
            jwk = {
                "kid": key_id,
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": base64url_encode(bytes_from_int(public_key.public_numbers().n)).decode("UTF-8"),
                "e": base64url_encode(bytes_from_int(public_key.public_numbers().e)).decode("UTF-8"),
            }
            if expiry_time > datetime.now(tz=timezone.utc):
                self.JWKS["keys"].append(jwk)  # Add JWK to JWKS if not expired
            return
        else:
            self.send_response(405)  # Method Not Allowed
            self.end_headers()
            return

    # Generate RSA key pair
    def generate_key_pair(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return private_key

# Create an HTTP server on localhost and port 8080
http_server = HTTPServer(("", 8080), RequestHandler)
print("HTTP Server is running on localhost port 8080!")
try:
    http_server.serve_forever()  # Run the server indefinitely
except KeyboardInterrupt:
    pass
http_server.server_close()  # Close the server on keyboard interrupt
