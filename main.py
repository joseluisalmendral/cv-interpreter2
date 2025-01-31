from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

app = FastAPI()

@app.post("/process_cv/")
async def process_cv(file: UploadFile = File(...)):
    try:
        # Leer el archivo proporcionado por el usuario
        contents = await file.read()

        # Manejar PDFs
        if file.filename.endswith(".pdf"):
            images = convert_from_bytes(contents)
            text = " ".join([pytesseract.image_to_string(img) for img in images])
        # Manejar imágenes
        else:
            image = Image.open(file.file)
            text = pytesseract.image_to_string(image)

        # Procesar texto (puedes agregar NLP aquí si lo necesitas)
        response = {"filename": file.filename, "extracted_text": text}
        return response
    except Exception as e:
        return {"error": str(e)}
