FROM python:3.10.6-buster

RUN pip install --upgrade pip

RUN apt update && apt upgrade -y && apt install pandoc -y

COPY /docs/requirements.txt /
RUN pip install -r /requirements.txt