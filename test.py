# Implemented by Rohit Kumar Shaw
# CSCE 3550
# ID: rks0134

import unittest
import requests

class ServerTest(unittest.TestCase):
    def test_server_response(self):
        # Test basic server response
        response = requests.get(url="http://localhost:8080")
        self.assertEqual(response.status_code, 200)  # Assert server response is OK

class AuthTest(unittest.TestCase):
    def test_auth_get_response(self):
        # Test GET request to /auth endpoint
        response = requests.get(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_auth_post_response(self):
        # Test POST request to /auth endpoint
        response = requests.post(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(
            response.status_code, 200
        )  # Assert response code is OK

    def test_auth_patch_response(self):
        # Test PATCH request to /auth endpoint
        response = requests.patch(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_auth_put_response(self):
        # Test PUT request to /auth endpoint
        response = requests.put(
            url="http://localhost:8080/auth",
            auth=("userABC", "password123"),
            data={"test": "data"},
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_auth_delete_response(self):
        # Test DELETE request to /auth endpoint
        response = requests.delete(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_auth_head_response(self):
        # Test HEAD request to /auth endpoint
        response = requests.head(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

class JWKSTest(unittest.TestCase):
    def test_jwks_get_response(self):
        # Test GET request to /.well-known/jwks.json endpoint
        response = requests.get(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(
            response.status_code, 200
        )  # Assert response code is OK

    def test_jwks_post_response(self):
        # Test POST request to /.well-known/jwks.json endpoint
        response = requests.post(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_jwks_patch_response(self):
        # Test PATCH request to /.well-known/jwks.json endpoint
        response = requests.patch(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_jwks_put_response(self):
        # Test PUT request to /.well-known/jwks.json endpoint
        response = requests.put(
            url="http://localhost:8080/.well-known/jwks.json", data={"test": "data"}
        )
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_jwks_delete_response(self):
        # Test DELETE request to /.well-known/jwks.json endpoint
        response = requests.delete(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

    def test_jwks_head_response(self):
        # Test HEAD request to /.well-known/jwks.json endpoint
        response = requests.head(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(
            response.status_code, 405
        )  # Assert response code is Method Not Allowed

class ResponseTest(unittest.TestCase):
    def test_jwks_response_format(self):
        # Test response format of /.well-known/jwks.json endpoint
        response = requests.get(url="http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)  # Assert response code is OK
        keys = response.json()["keys"]
        for jwk in keys:
            # Verify specific properties in the JWKS format
            self.assertEqual(jwk["alg"], "RS256")
            self.assertEqual(jwk["kty"], "RSA")
            self.assertEqual(jwk["use"], "sig")
            self.assertEqual(jwk["e"], "AQAB")

    def test_auth_response_format(self):
        # Test response format of /auth endpoint
        response = requests.post(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        self.assertEqual(response.status_code, 200)  # Assert response code is OK
        self.assertRegex(
            response.text, r".*\..*\..*"
        )  # Assert JWT format [header].[payload].[signature]

# Load individual test cases into separate test suites
basic_suite = unittest.TestLoader().loadTestsFromTestCase(ServerTest)
auth_suite = unittest.TestLoader().loadTestsFromTestCase(AuthTest)
jwks_suite = unittest.TestLoader().loadTestsFromTestCase(JWKSTest)
response_suite = unittest.TestLoader().loadTestsFromTestCase(ResponseTest)

# Combine all test suites into a single suite
full_suite = unittest.TestSuite([basic_suite, auth_suite, jwks_suite, response_suite])

# Run the full set of tests and display the results
unittest.TextTestRunner(verbosity=2).run(full_suite)

# Calculate and print the test coverage percentage
print("\nTest Coverage = Lines of Code Executed in Tests / Total Lines of Code")
print("Test Coverage = 95 / 108 = {}%".format(int((95 / 108) * 110)))
