import os
import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

load_dotenv()
main = Blueprint("main", __name__)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-v0.1"
HF_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

@main.route("/api/prompt")
def prompt():
    genre = request.args.get("genre", "general")
    tone = request.args.get("tone", "neutral")

    instruction = (f"Generate a creative writing prompt in one or two sentences. "
                   f"Genre: {genre}. Tone: {tone}.")
    payload = {"inputs": instruction}

    resp = requests.post(HF_URL, headers=HEADERS, json=payload, timeout=10)
    if resp.status_code != 200:
        return jsonify({"prompt": f"(API error {resp.status_code}) Try again."}), resp.status_code

    data = resp.json()
    # depending on format:
    if isinstance(data, list) and data:
        prompt_text = data[0].get("generated_text", "").strip()
    else:
        prompt_text = data.get("generated_text", "").strip()

    if not prompt_text:
        prompt_text = "Write about a moment that changed everything."

    return jsonify({"prompt": prompt_text})
