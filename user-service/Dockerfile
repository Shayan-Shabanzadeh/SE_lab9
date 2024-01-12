FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# Expose the port on which your application will run
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
