# django-heroku-manual-database

This tutorial is for simple Django project with app, static files and sqlite3 database. It has manual data transfer from local database to Heroku Posgresql database. This example is only good if you gave simple website like portfolio without any other users data inputs.
You will be able to change your local database, export it and manualy import through Heroku Django admin. This is easy and safe way to avoid data loss.

## 1. Import/Export admin model

Install Django Import Export package. This packages gives you ability to import and export data from your database through Django admin.

```python
pip install django-import-export
```

Add it to `setting.py` as installed app:

```python
INSTALLED_APPS = [
    'YourDjangoApp',
    'import_export',
    # ...
]
```

Change your app's `admin.py` with Import Export package, here's example of my project:

```python
from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin

class TastAdmin(ImportExportModelAdmin):
    list_display = ('title', 'description', 'created_at', 'due_date', 'is_completed')


admin.site.register(models.Task, TastAdmin)
```

## 2. Create new branch for Heroku deployment

Create new branch where all app changes will be made to work on Heroku.

## 3. Create required files in Django project

Create `runtime.txt` in project root folder next to `manage.py` file. Check your Python version:

```python
py --version
Python 3.10.9
```

Add this to `runtime.txt` file:

```python
python-3.10.9
```

Create `Procfile` (no extensions) in root folder next to `requirements.txt`.

```python
release: python YourProjectName/manage.py migrate && python YourProjectName/manage.py collectstatic --noinput
web: gunicorn --pythonpath YourProjectName YourProjectName.wsgi
```

## 4. Install required packages

Install required packages and add them to `requirements.txt` file in root folder.

```python
pip install gunicorn django-heroku whitenoise dj-database-url

pip freeze > requirements.txt
```

## 5. Configure Django settings

Adapt `setting.py` file for deployment on Heroku. Comment out local settings and add new imports:

```python
# from . import local_settings
import django_heroku
import os
import dj_database_url
```

Comment out a secret key line

```python
# SECRET_KEY = local_settings.SECRET_KEY
```

Set `DEBUG` to `False`

```python
DEBUG = False
```

Add whitenoise package:

```python
MIDDLEWARE = [
    # ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]
```

Configure database

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}
```

Configure static files

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True
WHITENOISE_INDEX_FILE = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MIMETYPES = (
    ('application/font-woff', 'application/font-woff'),
    # Add other mimetypes as needed
)
```

Add `django_heroku` to the end of settings file. It effectively sets up the project to run smoothly on Heroku.

```python
django_heroku.settings(locals())
```

## 6. Configure secret key

Create `.env` file in project root folder next to `manage.py` file. Make sure it is in `gitignore`. Add secret key from `local_settings.py`.

```python
SECRET_KEY = 'YourSecretKeyFromLocalSettings'
```

Push all the changes to Github.

## 7. Create Heroku App

Create your Heroku app on `heroku.com` and in settings choose Buildpack as Python. Then add the same secret key from `.env` file to Heroku's Config Vars.

## 8. Add Database on Heroku app

In `heroku.com` app overview add-ons choose Heroku Postgres database.

## 9. Deploy on Heroku

On your Heroku app choose depoyment method from Github and connect your repository, choose the right branch and click on `Deploy Branch` button. The Django app should be successfully deployd on Heroku without database data.

## 10. Export your local database

Now go back to the main branch of your Django project, run server and login to Django admin. Here you can update the data as you need and when you ready, export the data to `.csv` file.

## 11. Create superuser for Heroku Django admin

In your app page on `heroku.com` click on `More` in the right corner, choose `Run console` and write there:

```python
python YourProjectName/manage.py createsuperuser
```

Then enter your user name, email and password.

## 12. Import data to Heroku app

Login to your Heroku app's Django admin and import new data from `.csv` file. Easy and safe, good luck!
