FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p weights && \
    curl -L "https://drive.google.com/uc?export=download&id=1yZUsW0z7jVrkxWf3DuJep1GM-0BFYhEg" -o weights/best.pt
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]