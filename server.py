import os
import sys
import argparse

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # load env vars from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response")
def get_flask_response():
    message = request.args.get("message")
    response = get_response(message)
    return response

def get_response(message):
    completion = openai.ChatCompletion.create(
        # You can switch this to `gpt-4` if you have access to that model.
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
    )
    response = completion["choices"][0]["message"]["content"]
    return response

def run_cli(message):
    response = get_response(message)
    print(response)

def main():
    parser = argparse.ArgumentParser(description="GPT-3.5 chat app")
    parser.add_argument("--mode", type=str, choices=["cli", "web"], default="web", help="Choose between CLI or web mode")
    parser.add_argument("--message", type=str, help="User message (only required for CLI mode)")

    args = parser.parse_args()

    if args.mode == "cli":
        if args.message is None:
            print("Error: message argument is required for CLI mode")
            sys.exit(1)
        run_cli(args.message)
    else:
        app.run(debug=True)

if __name__ == "__main__":
    main()

