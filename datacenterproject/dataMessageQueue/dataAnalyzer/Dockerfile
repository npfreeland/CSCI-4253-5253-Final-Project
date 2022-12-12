FROM python:3.7


RUN pip3 install --upgrade minio jsonpickle requests flask  pandas 
RUN pip3 install pika
RUN pip3 install nba_api
WORKDIR /srv
COPY    DataAnalyzer.py /srv
CMD	[ "python3", "DataAnalyzer.py" ]