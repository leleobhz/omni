FROM python:3.9-slim-buster

# Dependencies for psutil lib to work
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./main.py ./stats.py ./

CMD [ "python3" , "main.py"]
