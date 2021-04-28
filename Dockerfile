FROM python:3.8
# set work directory
WORKDIR .
#RUN apt-get add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r ./requirements.txt
# copy project
EXPOSE 5000
COPY app .

#CMD ["flask", "run"]
CMD gunicorn --bind 0.0.0.0:5000 wsgi
