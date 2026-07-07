FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gdown
COPY . .
RUN gdown --id 1yZUsW0z7jVrkxWf3DuJep1GM-0BFYhEg -0 weights/best.pt
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]