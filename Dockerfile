FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source, utils folder and model weights
COPY backend/ ./backend/
COPY utils/ ./utils/
COPY model.pth ./model.pth

# Hugging Face Spaces requires the container to run on port 7860
EXPOSE 7860

# Command to run uvicorn from root to support relative package imports
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
