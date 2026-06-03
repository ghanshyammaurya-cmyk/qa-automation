from flask import Flask, request, jsonify
import jwt
import requests

app = Flask(__name__)

# ===== CONFIGURATION =====
IDP_JWKS_URL = "https://your-idp.com/.well-known/jwks.json"
ISSUER = "https://your-idp.com/"
AUDIENCE = "your-client-id"

# Cache JWKS
jwks = requests.get(IDP_JWKS_URL).json()


def verify_token(token):
    try:
        unverified_header = jwt.get_unverified_header(token)

        key = next(
            key for key in jwks["keys"]
            if key["kid"] == unverified_header["kid"]
        )

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        decoded = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER
        )

        return decoded

    except Exception as e:
        print("Token validation failed:", str(e))
        return None


# ===== MIDDLEWARE =====
@app.before_request
def sso_middleware():
    if request.path == "/health":
        return

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing SSO token"}), 401

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    if not user:
        return jsonify({"error": "Invalid or expired token"}), 401

    request.user = user


# ===== PROTECTED API =====
@app.route("/secure-data")
def secure_data():
    return jsonify({
        "message": "SSO Authentication Successful",
        "user": request.user["email"]
    })


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
