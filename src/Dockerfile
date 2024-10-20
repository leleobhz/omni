FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./main.py ./stats.py ./

CMD [ "python3" , "main.py"]
