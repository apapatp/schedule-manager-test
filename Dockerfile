# Pull the base image
FROM python:3.11-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
&& apt-get install gcc postgresql postgresql-contrib libpq-dev python3-dev netcat-traditional -y \
&& apt-get clean

# Set the working directory in the container
WORKDIR /home/django

# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt


# copy project
COPY . .
