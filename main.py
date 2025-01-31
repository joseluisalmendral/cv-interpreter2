from fastapi import FastAPI, File, UploadFile, HTTPException
import pytesseract
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_bytes
import os

app = FastAPI()

# Lista predefinida de habilidades comunes
SKILL_KEYWORDS = ['gcp',
 'kafka',
 'apache kafka',
 'iso27001',
 'estadistica descriptiva',
 'cloud computing',
 'big data',
 'comunicacion efectiva',
 'excel',
 'analisis de datos',
 'Estado no completado',
 'airflow',
 'gdpr',
 'statistics',
 'cloud platforms',
 'sistemas de seguridad',
 'analisis crítico',
 'big data tools',
 'data lakes',
 'analisis critico',
 'visualizacion',
 'tensorflow',
 'python',
 'trabajoenequipo',
 'deep learning',
 'data visualization',
 'datalakes',
 'data analysis',
 'powerbi',
 'machine learning',
 'spark',
 'auditoria de datos',
 'google cloud',
 'análisis de datos',
 'visualización de datos',
 'aws',
 'comunicación',
 'keras',
 'iso 27001',
 'gestion de riesgos',
 'docker',
 'seguridad',
 'trabajo en equipo',
 'visualizacion de datos',
 'nosql',
 'analisiscritico',
 'analisis predictivo',
 'comunicación efectiva',
 'visualización',
 'etl processes',
 'analisis',
 'data warehousing',
 'bigdata',
 'datawarehouses',
 'pytorch',
 'bi',
 'análisis predictivo',
 'kubernetes',
 'hadoop',
 'estadística descriptiva',
 'tableau',
 'comunicacion',
 'sql',
 'análisis crítico',
 'apachespark',
 'azure',
 'r',
 'data mining',
 'gestión de riesgos',
 'auditoría de datos',
 'seguridad de sistemas',
 'elt',
 'data warehouses',
 'etl',
 'nlp',
 'apache spark']

@app.get("/")
async def root():
    return {"message": "Esto funciona"}

@app.get("/check_poppler/")
async def check_poppler():
    poppler_check = os.system("which pdftoppm")
    if poppler_check == 0:
        return {"message": "Poppler está instalado y disponible"}
    else:
        return {"error": "Poppler no está instalado o no está en PATH"}

@app.post("/process_cv/")
async def process_cv(file: UploadFile = File(...)):
    try:
        # Verifica el tipo de archivo soportado
        if not (file.filename.endswith(".pdf") or file.filename.endswith((".jpg", ".jpeg", ".png"))):
            raise HTTPException(status_code=400, detail="Formato de archivo no soportado. Solo se aceptan PDFs e imágenes (.jpg, .jpeg, .png).")

        # Leer el contenido del archivo
        contents = await file.read()

        # Procesar PDFs
        if file.filename.endswith(".pdf"):
            try:
                images = convert_from_bytes(contents)
                text = " ".join([pytesseract.image_to_string(img) for img in images])
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")
        # Procesar imágenes
        else:
            try:
                image = Image.open(file.file)
                text = pytesseract.image_to_string(image)
            except UnidentifiedImageError:
                raise HTTPException(status_code=400, detail="No se pudo identificar la imagen proporcionada.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

        # Extraer habilidades del texto
        skills_detected = [skill.lower() for skill in SKILL_KEYWORDS if skill.lower() in text.lower()]

        # Retornar texto extraído y habilidades detectadas
        return {
            "filename": file.filename,
            "extracted_text": text,
            "skills_detected": list(set(skills_detected)),  # Eliminar duplicados
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}
