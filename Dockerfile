FROM python:3.8.10-slim-buster

WORKDIR /app
ENV FLASK_APP main

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]