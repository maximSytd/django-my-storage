from .paths import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',  # Имя базы данных
        'USER': 'myuser',      # Пользователь
        'PASSWORD': 'mypassword',  # Пароль
        'HOST': 'localhost',   # Хост (указываем localhost, так как PostgreSQL работает в Docker)
        'PORT': '5432',        # Порт
    }
}