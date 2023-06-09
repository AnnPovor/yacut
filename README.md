## Сервис по укорачиванию ссылок YaCut

Стэк: Flask, REST API

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

### Начало работы с проектом:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Чтобы запустить сервис:

В директории проекта создайте файл .env 

```python
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY = 'MY_SECRET_KEY'
````
И выполните команду:
```python
flask run
```
Проект развернется по адресу: http://127.0.0.1:5000/

# API для проекта:
Сервис обслуживает два эндпоинта:
```python
/api/id/ — POST-запрос на создание новой короткой ссылки
```
```python
/api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору
```
Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml.
Для удобной работы с документом воспользуйтесь онлайн-редактором Swagger Editor, в котором можно визуализировать спецификацию.