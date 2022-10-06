# pull official base image
FROM python:3.10.0-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN mkdir /app/staticfiles
RUN mkdir /app/static

RUN pip install -r requirements.txt

# copy project
COPY . /app/