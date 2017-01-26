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


**10.7 - Browser-Length and Persistent Sessions**

When using cookies, you can use Django's session framework to set cookies as either _browser-length sessions_ or _persistent sessions_

1. browser-length session expires when a user closes their browser
2. persistent sessions can last over several browser instances - expiring at a time of your choice. This could be half an hour or even as far as month in future.

By default browser length sessions are disabled. You can enable them by modifying your Django project's `settings.py` module. Add the variable `SESSION_EXPIRE_AT_BROWSER_CLOSE`, setting it to `True`

Alternativaly, persistent sessions are enabled by default, with `SESSION_EXPIRE_AT_BROWSER_CLOSE` either set to `False` or not being present in your project's `settings.py` module.

Persistent sessions have an additional setting, `SESSION_COOKIE_AGE`, which allows you to specify the age for which a cookie can live. This value should be an integer, representing the number of seconds the cookie can live for.
Eg: a value of `1209600` would mean your website's cookie expires after a two week (14-day) period.


**10.8 Clearing the Sessions Database**

1. If you database backend for Django sessions, this can be done with `python manage.py clearsessions`
2. Should run as a Cron job to ensure app's performance doesn't degrade as we experience more and more users.