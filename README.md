## Гайдлайн для запуска проекта
Для запуска проекта необходимы python 3.12 и Docker
(так же можно использовать poetry)

проверяем версию питона 
```bash
python --version 
# должно быть больше 3.12
```

создаем виртуальное окружение 
```bash
python -m venv .venv
```
активируем окружение
```bash
.venv/Scripts/activate  # windows
source .venv/bin/activate  # unix
```
скачиваем библиотеки
```bash
pip install -r requirements.txt
```

запускаем docker-compose, должен быть запущен демон докера (проще всего с десктопной версией)
```bash
docker-compose up
```

### создайте секреты для django в .env файле в каталоге проекта
```bash
DEBUG=true # или false для работы на продакшн сервере
DJANGO_SECRET="секрет для django"

CELERY_TASK_ALWAYS_EAGER=true

# настройки редиса
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1

# найстроки для бд
POSTGRES_DB="mydatabase"
POSTGRES_USER="myuser"
POSTGRES_PASSWORD="mypassword"
POSTGRES_HOST="postgres"
POSTGRES_PORT=5432


# ! не обязательно
# настройки для smtp
EMAIL_HOST_USER="ваша почта на хосте"
EMAIL_HOST_PASSWORD="пароль для хоста"
```

Делаем миграции базы данных
```bash
python manage.py makemigrations
python manage.py migrate
```

собираем статик файлы 
```bash
python manage.py collectstatic
```


запуск приложения
```bash
python manage.py runserver
```

cli для создания админа
```bash
python manage.py createsuperuser
```
! не обязательно
запуск celery (асинхронный воркер) в отдельном терминале с активированным окружением python
```bash
celery -A config worker -B --loglevel=INFO
```