from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import pytesseract
from PIL import Image
import whisper
import os

app = Flask(_name_)

# Supported Indian languages and their codes
INDIAN_LANGUAGES = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Odia": "or",
    "Urdu": "ur",
}

# Function to validate target language
def validate_language(language):
    if language in INDIAN_LANGUAGES:
        return INDIAN_LANGUAGES[language]
    else:
        raise ValueError(f"Unsupported language: {language}")

# Function to translate text
def translate_text(text, target_language):
    try:
        target_code = validate_language(target_language)
        translator = Translator()
        translated = translator.translate(text, dest=target_code)
        return translated.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Function to convert audio to text
def audio_to_text(audio_file):
    try:
        model = whisper.load_model("base")  # Load Whisper model
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        return f"Audio-to-text error: {str(e)}"

# Function to extract text from an image
def image_to_text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Image-to-text error: {str(e)}"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    input_type = data.get("input_type")
    target_language = data.get("target_language")
    text = data.get("text")
    audio_file = data.get("audio_file")
    image_file = data.get("image_file")

    if input_type == "text":
        translated_text = translate_text(text, target_language)
        return jsonify({"original_text": text, "translated_text": translated_text})

    elif input_type == "audio":
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.read())
        text = audio_to_text("temp_audio.wav")
        translated_text = translate_text(text, target_language)
        return jsonify({"original_text": text, "translated_text": translated_text})

    elif input_type == "image":
        with open("temp_image.png", "wb") as f:
            f.write(image_file.read())
        text = image_to_text("temp_image.png")
        translated_text = translate_text(text, target_language)
        return jsonify({"original_text": text, "translated_text": translated_text})

    return jsonify({"error": "Invalid input type"})

if _name_ == "_main_":
    app.run(debug=True)