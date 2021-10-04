
## Installation
```sh
git clone https://github.com/QFests/QFest.git
cd BookLibrary
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 ./run.py
```

Press CTRL+C to terminate the server.  
use `deactive` to quit the virtual environment.

Python 3 is recommend, meanwhile this project is compatible with python 2.

### Run with Docker

You can run this project with docker by running the following commands:
```sh
docker build -t qfest:latest .

docker run -ti -v `pwd`:/app -p 4000:4000 qfest:latest
```

By adding the `-v` above, you can make changes in the local files and they will
be reflected inside the docker container. If you want to run it in
"production" mode, skip the above `-v` option.

## Dependencies

- [Flask](https://github.com/mitsuhiko/flask)
- [SQLAlchemy](https://github.com/zzzeek/sqlalchemy)
- [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
- [Flask-Login](https://github.com/maxcountryman/flask-login)
- [Flask-WTF](https://github.com/lepture/flask-wtf)
- [Bootstrap](http://getbootstrap.com/)
- [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap)
- [Markdown](https://pythonhosted.org/Markdown/)
- [Flask-PageDown](https://github.com/miguelgrinberg/Flask-PageDown)
- [Flask-Uploads](https://packages.python.org/Flask-Uploads/)
- [Bootstrap File Input](https://github.com/kartik-v/bootstrap-file-input)

