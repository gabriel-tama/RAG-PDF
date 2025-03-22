FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y tesseract-ocr

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 poppler-utils  -y

# Copy the requirements
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



RUN pip install "unstructured[pdf]"


# Copy the application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]