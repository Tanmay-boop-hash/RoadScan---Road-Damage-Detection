FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gdown
COPY . .
RUN gdown 1yZUsW0z7jVrkxWf3DuJep1GM-0BFYhEg -O weights/best.pt
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]