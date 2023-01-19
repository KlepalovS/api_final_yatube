# API для проектра Yatube

## Описание
Данный проект является реализацией API для блог-платформы Yatube.

### Реализован функционал дающий возможность:
* Подписываться на пользователя.
* Просматривать, создавать новые, удалять и изменять посты.
* Просматривать и создавать группы.
* Комментировать, смотреть, удалять и обновлять комментарии.
* Фильтровать по полям.

## Установка 
Клонируем репозиторий на локальную машину:

```$ git clone https://github.com/KlepalovS/api_final_yatube.git```

 Создаем виртуальное окружение:
 
 ```$ python -m venv venv```
 
 Устанавливаем зависимости:

```$ pip install -r requirements.txt```

Создание и применение миграций:

```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем сервер:

```$ python manage.py runserver```

## Примеры запросов

Получение списка постов:

``` http://127.0.0.1:8000/api/v1/posts/ ```

Вернется ответ:

```
{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
{}
]
}
```

Получение информации о посте:

``` http://127.0.0.1:8000/api/v1/posts/{id}/ ```

Вернется ответ:

```
{
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": 0
}
```

Больше примеров запросв к API можно посмотреть после запуска проекта по адресу `http://localhost:8000/redoc/`
