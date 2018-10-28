# Todo-Manager
Todo-Manager is a web application created to manage your todos and do much more than that.
# Screenshots
[Registration](https://i.imgur.com/0dICHcw.png)
[Login](https://i.imgur.com/thIuuUA.png)
[Home](https://i.imgur.com/tw4BLTS.png)
[History](https://i.imgur.com/AqM4cjv.png)
# Features
  - Registation/ Login with email password combination
  - Users are grouped by their domain
  - First User of any domain automatically becomes admin
  - Admin has power to approve any new user registrations of the same domain
  - User can create, edit, complete and delete todos
  - Filtering of Todos based on pending, completed and created by me available
  - Email notification everytime a new registration is done or when admin approves an user
  - Logs are created for each user movement
### Tech

Toddo-Manager uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/)
* [Materialize](https://materializecss.com/)
### Installation

Todo-Manager requires [Python3](https://www.python.org/) to run.

Create a python3 virtual environment using [virtualenv](https://virtualenv.pypa.io/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

Activate your virtualenv

Upgrade your pip using `pip install --upgrade pip`

Install packages using `pip install -r requirements.txt`
```sh
(global) sachin@sachin-H81M-S ~/Todo-Manager (master) $ pip install -r requirements.txt
Requirement already satisfied: amqp==2.3.2 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 1)) (2.3.2)
Requirement already satisfied: billiard==3.5.0.4 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 2)) (3.5.0.4)
Requirement already satisfied: celery==4.2.1 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 3)) (4.2.1)
Requirement already satisfied: Django==2.1.2 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 4)) (2.1.2)
Requirement already satisfied: kombu==4.2.1 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 5)) (4.2.1)
Requirement already satisfied: pkg-resources==0.0.0 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 6)) (0.0.0)
Requirement already satisfied: pytz==2018.5 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 7)) (2018.5)
Requirement already satisfied: redis==2.10.6 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 8)) (2.10.6)
Requirement already satisfied: vine==1.1.4 in /home/sachin/.virtualenvs/global/lib/python3.5/site-packages (from -r requirements.txt (line 9)) (1.1.4)
```
Since I have already downloaded these dependencies I am getting this message, for first time user you should see the download progress of each package.

Migrate the database using `python manage.py migrate`

```sh
(global) sachin@sachin-H81M-S ~/Todo-Manager (master) $ python manage.py migrate
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions, todos
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying todos.0001_initial... OK
  Applying todos.0002_auto_20181026_0942... OK
```

Now since our database is migrated, we can run the server using `python manage.py runserver`

```sh
(global) sachin@sachin-H81M-S ~/Todo-Manager (master) $ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
October 28, 2018 - 13:55:39
Django version 2.1.2, using settings 'TodoManager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Now go to `http://localhost:8000` and register and start using the application

