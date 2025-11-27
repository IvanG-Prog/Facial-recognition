# Facial Recognition Security System
[![Product Page](https://img.shields.io/badge/OFFICIAL_SITE-GET_CLI_HERE-3B82F6?style=for-the-badge)](https://recognitionf.netlify.app/)

This project implements a web-based **Access Control System** that verifies user identity using **Facial Recognition** powered by Machine Learning. It consists of a robust Python API (Flask) for AI processing and a decoupled JavaScript frontend.

---

##  Key Features

* **Biometric Verification:** Secure access requiring both user credentials and a biometric proof (face scan).
* **Machine Learning Pipeline:** Uses **MTCNN** (Face Detection and Alignment) and **InceptionResnetV1 (FaceNet)** (Facial Embedding Generation) via `facenet_pytorch`.
* **Production Readiness:** API is served efficiently using **Flask** and **Gunicorn** within a Dockerized environment.
* **Dependency Management:** Uses **Poetry** for isolated, reproducible dependency management.

---

## 🌐 Live Demo & Deployment

You can interact with the deployed application:

* **Frontend (Netlify):**
    https://recognitionf.netlify.app/

* **Backend API (Hugging Face Spaces / Docker):**
    The API endpoint is currently available at:
	https://huggingface.co/spaces/IvanG-Prog/facial-recognition?logs=container

---

## 💻 Installing and Running Locally

### 1. Prerequisites

Ensure you have **Python 3.9+** and **Poetry** installed.

### 2. Installation Flow

#### Install Poetry

Consult the [official Poetry installation manual](https://python-poetry.org/docs/#installation).

#### Install dependencies in the current environment

```shell
poetry install
```
### Run the Registration process

```shell
poetry run registers
```

### Run the Access process

```shell
poetry run access
```

### Run the Flask application

```shell
poetry run flask
```

This will start the Flask development server, and you can access the application at `http://127.0.0.1:5000/`.

## Linting

```shell
poetry run pylint --recursive=y .
```
