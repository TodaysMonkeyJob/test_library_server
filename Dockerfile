FROM python:3.8-slim
# set work directory

ENV WORKDIR /opt/src
WORKDIR ${WORKDIR}

#RUN apt-get add postgresql-dev gcc python3-dev musl-dev
# install dependencies

COPY requirements.txt ${WORKDIR}

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && pip install --upgrade pip setuptools wheel \
    && pip install -Ur requirements.txt

# copy project
COPY app ${WORKDIR}/app/
COPY config.py ${WORKDIR}/config.py
COPY wsgi.py ${WORKDIR}/wsgi.py

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 wsgi