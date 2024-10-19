# Use the latest Python runtime as a parent image
FROM python:3.12.4

# Set environment variables (optional but recommended for production)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the app using Gunicorn with eventlet for WebSocket support
CMD ["python", "app:app"]
