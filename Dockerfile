# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install ffmpeg and opus
RUN apt-get update && apt-get install -y ffmpeg libopus0

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "main.py"]
