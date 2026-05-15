import os
import fitz
import soundfile as sf

from flask import Flask, render_template, request, send_file

from kokoro import KPipeline

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER

# inicia pipeline
pipeline = KPipeline(lang_code="p")


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

    filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filename)

    # Open the PDF and extract text
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    # limita texto inicialmente
    text = text[:500]

    # gera áudio
    generator = pipeline(text, voice="af_heart")

    output_path = os.path.join(app.config["GENERATED_FOLDER"], "output.wav")

    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(output_path, audio, 24000)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
