FROM python:3.11.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /chat_proj

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
