# Usa Python 3.9 como base
FROM python:3.9

# Instala Tesseract OCR y dependencias necesarias
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Configura el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para iniciar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
