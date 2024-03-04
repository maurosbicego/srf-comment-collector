FROM python:3.9.13-slim-buster

WORKDIR /collector
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY settings-docker.py settings.py

CMD [ "python3", "main.py"]