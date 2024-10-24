FROM python:3.10-slim
# # Use the CUDA runtime base image
# FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt .

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

