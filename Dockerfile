# Usa Python 3.9 como base
FROM python:3.9

# Asegura que Python maneje bien caracteres especiales
ENV PYTHONUTF8=1

# Instala dependencias del sistema, incluyendo Tesseract OCR y Poppler
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configura el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Actualiza pip y setuptools antes de instalar dependencias
RUN pip install --upgrade pip setuptools

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para iniciar la API con Uvicorn y 2 workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
