# Digital Attendance Sheet

An Attendance Sheet to manages employees entrance and exit

## Running

If you have a virtual environment, it's better to do it there.

Activating the virtual env.

```sh
$ pip -m venv .venv
$ source .venv/bin/activate
```

```sh
# install the requirements
$ pip install -r requirements.txt

# create an admin
$ python manage.py createsuperuser

# run the server
$ python manage.py runserver
```

Now got [http://127.0.0.1:8000](http://127.0.0.1:8000)
