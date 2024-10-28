# Use the official Python image from the Docker Hub
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .


# Command to run the Django development server
CMD [ "python", "./django_graphene_test/manage.py", "runserver", "0.0.0.0:8088"]

# Expose port 8088 for the application
EXPOSE 8088