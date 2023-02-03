<h1 align="center">TODOList</h1>

## Данный проект представляет собой backend-часть для сайта планирования задач.


### 1. Установка зависимостей.
``` 
pip install -r requirements.txt
```

### 2. Создать свой .env файл в корне проекта.

### 3. Заполнить .env файл:
```xml
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localost
DB_PORT=5432
SECRET_KEY='django-insecure-1tu5ogl_y)*9gxl26hly^ag=%**e1d(r+$%=h4bdtgqg=#06rm'
DEBUG=True
```


### 4. Выполнить миграции.
```sh
python ./manage.py migrate 
```

### 5. Запустить сервер.
```sh
python ./manage.py runserver
```
