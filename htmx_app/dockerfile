FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTESCODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN mkdir src

WORKDIR /src
COPY . /src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build . -t htmx_chatbot
# docker run -p 8000:8000 htmx_chatbot
# ~220 MB image size