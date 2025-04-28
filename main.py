from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import os
import subprocess
import zipfile

# Folder inside your workspace to store the model
MODEL_DIR = "MachineTranslation_model"
MODEL_ZIP = os.path.join(MODEL_DIR)
MODEL_FILE = "model.safetensors"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)

def download_folder_from_drive(folder_id, model_dir):
    # Skip download if folder already exists and is not empty
    if os.path.exists(model_dir) and os.listdir(model_dir):
        print(f"Folder '{model_dir}' already exists and is not empty. Skipping download.")
        return

    print("Downloading folder from Google Drive...")
    try:
        subprocess.run([
            "gdown",
            "--folder",
            f"https://drive.google.com/drive/folders/{folder_id}",
            "-O",
            model_dir
        ], check=True)
        print("Download completed successfully.")
        
    except subprocess.CalledProcessError as e:
        print("Download failed:", e)

# Example usage:
FOLDER_ID = "1NHgXBwCpJ91g3mFXWpEotzj6tb-s7shZ"
download_folder_from_drive(FOLDER_ID, MODEL_DIR)




# Function to download model from Google Drive
def download_model_from_drive(file_id):
    if not os.path.exists(MODEL_DIR) or not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        os.makedirs(MODEL_DIR, exist_ok=True)  # Automatically create folder if it doesn't exist
        subprocess.run([
            "gdown",
            f"https://drive.google.com/uc?id={file_id}",
            "-O", MODEL_PATH
            ])
        print("Download complete.")
    else:
        print("Model already exists, skipping download.")

# Trigger the download before the app starts
download_model_from_drive("10NfQb8r4r3YWRd2Q8l47hOw90Sj8Lj9m")

# Initialize FastAPI app
app = FastAPI()

# Load the saved model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

# Set up directory
templates = Jinja2Templates(directory=".")

# Pydantic model for input validation
class TranslationRequest(BaseModel):
    text: str

# Translation function
def translate_text(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", max_length=120, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=120, num_beams=4, early_stopping=True)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

# Route for index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("web_app.html", {"request": request})

# API route for translation
@app.post("/translate")
async def translate(request: TranslationRequest):
    translation = translate_text(request.text)
    return {"translation": translation}