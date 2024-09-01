# Use an official Python runtime as a parent image
FROM python:3.10-slim
# Use the official NVIDIA CUDA base image
FROM nvidia/cuda:11.0.3-base-ubuntu20.04

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Set environment variables for CUDA
ENV CUDA_VISIBLE_DEVICES=0

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
