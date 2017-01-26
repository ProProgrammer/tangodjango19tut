**10.6 - Session Data - Notes**

To use session based cookies you need to perform the following steps:

1. Make sure that the `MIDDLEWARE_CLASSES` list found in the `settings.py` module contains `django.contrib.sessions.middleware.SessionMiddleware`.
2. Configure your session backend. Make sure that `django.contrib.sessions` is in your `INSTALLED_APPS` in `settings.py`. If not, add it, and run the database migration command, `python manage.py migrate`
3. By default a database backend is assumed, but you might want to use a different setup (i.e. cache). See the [official Django documentation on Sessions](https://docs.djangoproject.com/en/1.9/topics/http/sessions/) for other backend configuration

Once session based cookie is implemented in rango/views.py, use `python manage.py shell` to find if the visits count is updated as follows:

1. Open browser and navigate to localhost:8000/rango/
2. Run Django shell `python manage.py shell` in a different terminal (leave shell with `python manage.py runserver` as it is)
3. Import Session model in django shell `from django.contrib.sessions.models import Session`
4. Observe the session key in browser > dev tools
5. Fetch session object for your particular session using `some_session = Session.objects.get(session_key='my_session_key')`
6. See the visits count in your session object using `some_session.get_decoded()`
7. Since you are checking for `days > 0` in `visit_cookie_handler()` function, this count will not increment immediately upon page refresh
8. For testing purpose, change `days > 0` to `seconds > 0` in `visit_cookie_handler()` function and then refresh the page
9. Now fetch the session object again (as the session object must have changed with new incremented visits counter) and then see the value of visits as follows:
10. `some_session = Session.objects.get(session_key='my_session_key'); some_session.get_decoded()`
11. Don't forget to change `seconds > 0` back to `days > 0` in `visit_cookie_handler()` function.