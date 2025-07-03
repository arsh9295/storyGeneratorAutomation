# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (if your app runs a server, e.g., with Gradio or Flask)
# EXPOSE 7860

# Set entrypoint and allow passing arguments
ENTRYPOINT ["python", "main.py"]
CMD []

# docker run your-image-name arg1 arg2

# docker run -v "D:/path/to/globalVariables:/app/configs" my-python-image python main.py /app/configs/globalVariables.py
# 