# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

#RUN apt-get update && apt-get install -y netcat
RUN apt-get update && apt-get install -y netcat clamav clamav-daemon

WORKDIR /python-docker

# Copy the requirements file into the container and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for Flask to know which file to run
ENV FLASK_APP=main.py

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the Flask application when the container is run
# CMD ["flask", "run", "--host=0.0.0.0"]
# Start the Flask application when the container is run

#CMD sh -c 'until nc -z db 3306; do echo "Waiting for database to start up..." && sleep 1; done; flask run --host=0.0.0.0'
CMD sh -c 'service clamav-daemon start && until nc -z db 3306; do echo "Waiting for database to start up..." && sleep 1; done; flask run --host=0.0.0.0'
