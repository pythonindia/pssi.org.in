How to setup
===

 - Create a PostgreSQL 9.3 database
 - Create a file named `local_settings.py` inside the `pssi` directory. The file content looks like this -

        DEBUG=True

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'LOCAL_DBNAME',
                'USER': 'USERNAME',
                'PASSWORD': 'PASSWORD',
                'HOST': '',
                'PORT': ''
            }
        }

        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

 - Run `python manage.py syncdb` and create a superuser when prompted

 - Run `python manage.py migrate` to apply pending migrations

 - Run `python manage.py runserver`

Configuring Django-allauth
---

 - Go to `/admin/` > Sites and change the default site's(the one with ID = 1) name and display to `localhost:8000` or whatever you use to develop locally.
 - Go to `Social Applications` in admin panel and add [Github](http://django-allauth.readthedocs.org/en/latest/providers.html#github) and [Google](http://django-allauth.readthedocs.org/en/latest/providers.html#google)'s auth details

Payment Link
---

- Add `MEMBERSHIP_PAYMENT_LINK` in `local_settings.py` for testing Rs 0 payemnt. Url is `https://www.instamojo.com/pssi/test-pssi-membership/`.
