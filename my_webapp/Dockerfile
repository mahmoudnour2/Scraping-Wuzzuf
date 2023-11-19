# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Flask app files to the container
COPY app.py .
COPY requirements.txt .
COPY static /app/static
COPY templates /app/templates

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application when the container starts
CMD ["python", "app.py"]