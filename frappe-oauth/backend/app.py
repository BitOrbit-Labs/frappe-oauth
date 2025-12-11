from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

FRAPPE_URL = os.getenv("FRAPPE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")

@app.route("/login")
def login():
    state = os.urandom(8).hex()
    authorize_url = f"{FRAPPE_URL}/api/method/frappe.integrations.oauth2.authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={state}"
    return redirect(authorize_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code found in callback"

    token_url = f"{FRAPPE_URL}/api/method/frappe.integrations.oauth2.get_token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    token_response = requests.post(token_url, data=data)

    return token_response.json()

@app.route("/items")
def items():
    access_token = request.args.get("access_token")
    if not access_token:
        return "Error: access_token missing", 400

    api_url = f"{FRAPPE_URL}/api/resource/Item?limit_page_length=5"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(api_url, headers=headers)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(debug=True)
