FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
  libjpeg-dev \
  zlib1g-dev \
  libpng-dev \
  build-essential

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "src.facial_recognition.app:app", "--bind", "0.0.0.0:7860"]
