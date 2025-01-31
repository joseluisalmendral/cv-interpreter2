from fastapi import FastAPI, UploadFile, File
import pytesseract
from PIL import Image
import spacy
import json
from pdf2image import convert_from_bytes

app = FastAPI()

# Cargar modelo NLP de SpaCy
nlp = spacy.load("en_core_web_sm")

@app.post("/process_cv/")
async def process_cv(file: UploadFile = File(...)):
    try:
        # Leer archivo
        contents = await file.read()
        
        # Si es PDF, convertir a imagen
        if file.filename.endswith(".pdf"):
            images = convert_from_bytes(contents)
            text = " ".join([pytesseract.image_to_string(img) for img in images])
        else:
            image = Image.open(file.file)
            text = pytesseract.image_to_string(image)
        
        # Procesar texto con NLP
        doc = nlp(text)
        nombre = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
        habilidades = [token.text for token in doc if token.pos_ == "NOUN"]
        
        # Estructura de respuesta
        response = {
            "nombre": nombre,
            "texto_extraido": text,
            "habilidades_detectadas": list(set(habilidades)),
        }
        
        return response
    
    except Exception as e:
        return {"error": str(e)}

