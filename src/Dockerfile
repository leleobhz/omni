FROM python:3-slim as build

COPY ./requirements.txt requirements.txt

RUN apt -y update && \
    apt -y install build-essential python3-dev && \
    pip3 install -r requirements.txt

FROM python:3-slim

WORKDIR /app

COPY --from=build /usr/local/lib/ /usr/local/lib/

COPY ./main.py ./stats.py ./

CMD [ "python3" , "main.py"]
