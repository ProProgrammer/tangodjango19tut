**10.6**

To use session based cookies you need to perform the following steps:

1. Make sure that the `MIDDLEWARE_CLASSES` list found in the `settings.py` module contains `django.contrib.sessions.middleware.SessionMiddleware`.
2. Configure your session backend. Make sure that `django.contrib.sessions` is in your `INSTALLED_APPS` in `settings.py`. If not, add it, and run the database migration command, `python manage.py migrate`
3. By default a database backend is assumed, but you might want to use a different setup (i.e. cache). See the [official Django documentation on Sessions](https://docs.djangoproject.com/en/1.9/topics/http/sessions/) for other backend configuration