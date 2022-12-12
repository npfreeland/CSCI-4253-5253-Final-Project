FROM python:3.7


RUN pip3 install --upgrade minio jsonpickle requests flask  pandas 
RUN pip3 install pika
RUN pip3 install nba_api
RUN pip3 install matplotlib
RUN pip3 install joblib
RUN pip3 install scikit-learn
WORKDIR /srv/model
COPY    trained_models /srv/model
COPY model.py /srv/model
CMD	[ "python3", "model.py" ]