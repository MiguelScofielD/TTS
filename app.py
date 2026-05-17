import os
import fitz
import requests
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


from flask import Flask, render_template, request, send_file

load_dotenv()
AI_API_URL = os.getenv("AI_API_URL")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    if "pdf" not in request.files:
        return "No file selected"

    file = request.files["pdf"]

    if file.filename == "":
        return "No file selected"

    # salva pdf
    safe_name = secure_filename(file.filename)

    unique_filename = f"{uuid.uuid4()}_{safe_name}"

    filename = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

    file.save(filename)

    # extrai texto
    doc = fitz.open(filename)

    text = ""

    for page in doc:
        text += page.get_text()

    # limita texto inicialmente
    # text = text[:1000]

    # chama API IA
    response = requests.post(AI_API_URL, json={"text": text}, timeout=120)

    if response.status_code == 200:

        audio_filename = f"{uuid.uuid4()}.wav"

        output_path = os.path.join(app.config["GENERATED_FOLDER"], audio_filename)

        with open(output_path, "wb") as f:
            f.write(response.content)

        return send_file(output_path, as_attachment=True)

    return f"Error generating audio: {response.text}"


if __name__ == "__main__":
    app.run(debug=True)
