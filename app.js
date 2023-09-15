const forge = require('node-forge');

function generateRSAKeyPair() {
  const keys = forge.pki.rsa.generateKeyPair(2048);
  const privateKey = forge.pki.privateKeyToPem(keys.privateKey);
  const publicKey = forge.pki.publicKeyToPem(keys.publicKey);
  const kid = 'your-key-id'; // Generate a unique key ID
  const expiryTimestamp = Date.now() + 24 * 60 * 60 * 1000; // 24 hours from now

  return {
    kid,
    privateKey,
    publicKey,
    expiryTimestamp,
  };
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

// Your key generation logic here

// RESTful JWKS endpoint
app.get('/jwks', (req, res) => {
  // Filter and serve only keys that have not expired
  const currentTimestamp = Date.now();
  const validKeys = keys.filter((key) => key.expiryTimestamp > currentTimestamp);

  const jwks = {
    keys: validKeys.map((key) => ({
      kid: key.kid,
      kty: 'RSA',
      n: key.publicKey,
      // Add other key properties as needed
    })),
  };

  res.json(jwks);
});

// Authentication endpoint
app.post('/auth', (req, res) => {
  // Authentication logic here (e.g., mock authentication)

  // Generate a JWT with the appropriate key based on the kid query parameter
  const kid = req.query.kid || 'default-key-id'; // Use a default key if no kid is specified
  const selectedKey = keys.find((key) => key.kid === kid);

  if (!selectedKey || selectedKey.expiryTimestamp <= Date.now()) {
    return res.status(401).json({ error: 'Invalid or expired key' });
  }

  // Generate and sign the JWT
  const jwtPayload = {
    sub: 'userABC', // Mock user data
    // Add other JWT claims as needed
  };

  const token = generateJWT(jwtPayload, selectedKey.privateKey);

  res.json({ token });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const jwt = require('jsonwebtoken');

function generateJWT(payload, privateKey) {
  return jwt.sign(payload, privateKey, { algorithm: 'RS256' });
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Sample test using Mocha and Chai
const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('./your-express-app.js'); // Replace with the path to your Express app

chai.use(chaiHttp);

describe('Authentication', () => {
  it('should return a valid JWT', (done) => {
    chai
      .request(app)
      .post('/auth')
      .end((err, res) => {
        chai.expect(res).to.have.status(200);
        chai.expect(res.body.token).to.be.a('string');
        done();
      });
  });
});

// Add more tests as needed
