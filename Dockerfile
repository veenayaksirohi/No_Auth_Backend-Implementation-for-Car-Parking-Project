# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size
# --upgrade pip ensures latest pip is used
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# (Make sure Dockerfile is in the same directory as app.py, run.py etc.)
COPY . .

# Make port 5000 available to the world outside this container
# (Flask default port, change if your run.py uses a different one)
EXPOSE 5000

# Define environment variables (can be overridden by docker-compose)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0 # Listen on all interfaces within the container

# Command to run the application using the entrypoint script (run.py)
CMD ["flask", "run"]
# Alternatively, if run.py uses app.run():
# CMD ["python", "run.py"]