# Use the official Python image as the base image
FROM python:3.10.7

# Set the working directory in the container
WORKDIR /app

# Copy python script to the container
COPY app.py .

#install redis
RUN pip install redis

CMD ["python", "app.py"]
