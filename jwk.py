from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric import padding
import datetime
import jwt

app = Flask(__name__)

# Store RSA keys with kid and expiry timestamp
keys = []

# Function to generate a new RSA key pair
def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key

# Function to convert RSA key to JWKS format
def rsa_key_to_jwks(private_key, kid, expiry):
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')
    jwk = {
        "kid": kid,
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": public_key.public_numbers().n,
        "e": public_key.public_numbers().e,
        "exp": expiry,
    }
    return jwk

@app.route('/jwks', methods=['GET'])
def get_jwks():
    current_time = datetime.datetime.utcnow()
    active_keys = [key for key in keys if key['exp'] > current_time]
    jwks = {
        "keys": active_keys,
    }
    return jsonify(jwks)

@app.route('/auth', methods=['POST'])
def authenticate():
    # Mocking authentication (you can replace this with real authentication logic)
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
        if username == "userABC" and password == "password123":
            # Generate and return a JWT
            kid = "sample-key"
            expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            private_key = generate_rsa_key()
            jwk = rsa_key_to_jwks(private_key, kid, expiry)
            keys.append(jwk)  # Store the new key temporarily
            payload = {
                "sub": username,
                "iat": datetime.datetime.utcnow(),
                "exp": expiry,
            }
            token = jwt.encode(payload, private_key, algorithm="RS256")
            return jsonify({"token": token})
    
    return jsonify({"error": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=8080)
