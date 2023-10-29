release: python task_project/manage.py migrate && python task_project/manage.py collectstatic --noinput
web: gunicorn --pythonpath task_project task_project.wsgi