FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN apt -y update && \
    apt -y install gcc && \
    pip3 install -r requirements.txt && \
    apt -y purge gcc && \
    rm -rf /var/lib/apt/lists/*

COPY ./main.py ./stats.py ./

CMD [ "python3" , "main.py"]
