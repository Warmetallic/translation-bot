# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variables (you should set these in your Docker Compose or Docker run command)
# ENV BOT_KEY=your_bot_key
# ENV API_KEY=your_api_key

# Expose the port that your application listens on (if applicable)
# EXPOSE 80

# Run your Python application
CMD ["python", "translation_bot.py"]
