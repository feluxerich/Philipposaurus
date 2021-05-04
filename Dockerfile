FROM python:3.8.0-slim

WORKDIR /philipposaurus

COPY ./philipposaurus /philipposaurus
COPY requirements.txt /philipposaurus

RUN apt upgrade

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python /philipposaurus/main.py