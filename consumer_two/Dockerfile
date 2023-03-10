FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install pymongo

RUN pip3 install -r requirements.txt

RUN pip3 list > list.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
