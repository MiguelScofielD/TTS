# 1. PDF to Audio AI

Convert PDF documents into audio using self-hosted AI text-to-speech models.

## 2. Self-Hosted AI

This project uses local AI text-to-speech models instead of external paid APIs.

The audio generation pipeline runs using Kokoro TTS and PyTorch.

## 3. Features

- Upload PDF files
- Extract text from PDFs
- Convert text into speech using Kokoro TTS
- Generate downloadable audio files
- Self-hosted AI pipeline

## 4. Technologies

- Flask
- Bootstrap
- PyMuPDF
- Kokoro TTS
- PyTorch

## 5. Installation

```bash
python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

```
---

## 6. Rodar projeto

```md id="m8z3jq"
## Run

```bash
python app.py

```
---

## 7. Como funciona

Aqui fica MUITO interessante:

```md id="c7v2lr"
## Pipeline

1. User uploads a PDF
2. PyMuPDF extracts the text
3. Kokoro TTS generates speech
4. Flask returns the generated audio
```

## 8. Future Improvements

- MP3 support
- Audio player
- Smart chunking
- Multiple voices
- User authentication

