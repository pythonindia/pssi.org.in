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

 - Run `python manage.py syncdb`
 - Run `python manage.py runserver`
