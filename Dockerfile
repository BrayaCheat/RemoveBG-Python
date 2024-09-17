# Use the official Python 3.9 slim image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /remove-bg

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the application will run on
EXPOSE 5000

# Command to run the application using gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app"]

