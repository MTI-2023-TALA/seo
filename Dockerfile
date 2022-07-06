FROM python:3.8.13-alpine3.16

WORKDIR /app
ENV FLASK_APP main

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
