FROM python:3.8


RUN pip3 install --upgrade minio redis jsonpickle requests flask
WORKDIR /srv/rest
COPY    rest-server.py /srv/rest
COPY static /srv/rest/static
COPY templates /srv/rest/templates
CMD	[ "python3", "rest-server.py" ]