# CSCE3550JWKServer
JWT JWKS Server
JWT JWKS Server is a Node.js application that serves public keys with unique identifiers (kid) for verifying JSON Web Tokens (JWTs). It also implements key expiry for enhanced security and provides an authentication endpoint for issuing JWTs.

Table of Contents
Getting Started
Prerequisites
Installation
Usage
Configuration
Running the Server
Endpoints
/jwks
/auth
Testing
Contributing
License
Getting Started
Prerequisites
To run this project, you need to have the following prerequisites installed on your system:

Node.js (v14 or higher)
npm (Node Package Manager)
Installation
Clone the repository to your local machine:


git clone [https://github.com/your-username/jwt-jwks-server.git](https://github.com/rks0134/CSCE3550JWKServer.git)
Navigate to the project directory:


cd jwt-jwks-server
Install project dependencies:


npm install
Usage
Configuration
You can customize the server configuration and manage RSA key pairs in the server.js file. By default, the server generates a single RSA key pair for demonstration purposes. You should implement a more robust key management strategy in a production environment.

Running the Server
To start the server, run the following command:


npm start
The server will listen on port 8080 by default. You can configure the port in the server.js file.

Endpoints
/jwks Endpoint
The /jwks endpoint serves the public keys in JWKS (JSON Web Key Set) format. It only serves keys that have not expired.

/auth Endpoint
The /auth endpoint is used for authentication and JWT issuance. It returns an unexpired, signed JWT on a POST request. If the "expired" query parameter is present, it issues a JWT signed with the expired key pair and the expired expiry timestamp.

Testing
Basic testing is included using Mocha and Chai. You can run the tests with the following command:


npm test
Expand the test suite to cover additional scenarios and edge cases.

Contributing
Contributions to this project are welcome. If you find issues or have suggestions for improvements, please open an issue or create a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
