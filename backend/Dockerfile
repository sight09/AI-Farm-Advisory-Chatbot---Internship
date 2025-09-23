# 1. Use an official Python runtime as the base image
FROM python:3.13-slim

# 2. Set the working directory inside the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# 3. Copy the requirements.txt (or setup.py) first to leverage Docker cache
COPY requirements.txt /app/

# 4. Install any Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code into the container
COPY . /app/

# 6. Expose the port the app will run on (usually 8000 or 5000 for Flask)
EXPOSE 8000

# 7. Set the default command to run the app (flask or django, depending on your setup)
CMD ["python", "main.py", "runserver"]

