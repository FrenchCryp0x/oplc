# Dockerfile (root)
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# deps (your requirements.txt is at root)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# app code (your code lives in /app folder in the repo)
COPY app ./app

EXPOSE 7860
ENV BACKEND_MODE=proxy PADDING=true
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","7860","--no-access-log"]
