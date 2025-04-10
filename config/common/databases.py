import decouple

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': decouple.config('POSTGRES_DB'),
        'USER': decouple.config('POSTGRES_USER'),
        'PASSWORD': decouple.config('POSTGRES_PASSWORD'),
        'HOST': decouple.config('POSTGRES_HOST'),
        'PORT': decouple.config('POSTGRES_PORT', cast=int),
    }
}