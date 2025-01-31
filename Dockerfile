# Usa una imagen de Python
FROM python:3.9

# Instala Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

# Crea un directorio en el contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# Ejecuta la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
