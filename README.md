<h1 align="center">TODOList</h1>

## Данный проект представляет собой backend-часть для сайта планирования задач.


### 1. Установка зависимостей.
``` 
pip install -r requirements.txt
```

### 2. Создать свой .env файл в корне проекта.

### 3. Заполнить .env файл:
```xml
DB_NAME=todolist
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localost
SECRET_KEY=123qwe
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
### 6. Запуск всех образов.
```sh
docker-compose up --build -d
```