# Start with an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application using Uvicorn
# We use 0.0.0.0 to allow traffic from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]