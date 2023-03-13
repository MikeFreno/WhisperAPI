# Use the official Python image as a parent image.
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && apt-get install -y ffmpeg

# Copy the application code into the container
COPY . .

# Expose the port that the application will listen on
EXPOSE 8080

CMD ["python", "app.py"]
