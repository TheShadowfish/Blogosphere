# Описание проекта

Приложение, в котором пользователи могут писать посты и комментировать их.

## Требования
- Python 3.10
- Django 5.1.2
- DRF 3.15.2
- PostgreSQL 17

## 4. при необходимости загрузить тестовые данные в БД python3 manage.py loaddata data/testdata.json


## Установка

1. Склонируйте репозиторий:
    ```bash
    git clone 
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd blogoshere
    ```

3. Активируйте Poetry и установите зависимости с помощью Poetry:
    ```bash
    poetry shell
    poetry install
    ```

4. Скопируйте .env.sample в .env и настройте переменные окружения в файле .env.
    ```bash
    cp .env.sample .env
    ```

5. Войдите в Postrges, 
   cоздайте базу данных соответствующую POSTGRES_DB=<имя вашей базы данных>, (например blogoshere) 
   ```bash
    createdb -h localhost -U postgres blogosphere
   ```
  

6. выполните миграции базы данных:
    ```bash
    poetry run python manage.py migrate
    ```

6. Создайте суперпользователя для доступа к админке:
    ```bash
    poetry run python manage.py createsuperuser
    ```
   или же можете воспользоваться командой `csu`, обязательно указав в файле .env ADMIN_PASSWORD:
    ```bash
    poetry run python manage.py csu
    ```

7. Запустите сервер:
    ```bash
    poetry run python manage.py runserver
    ```
8. При необходимости загрузите тестовые данные из папки data:
    ```bash
    poetry run python manage.py loaddata data/testdata.json
    ```

   
## Документация API
Автогенерируемая документация доступна по следующим URL:
- Swagger: http://localhost:8000/docs/
- ReDoc: http://localhost:8000/redoc/



==============================================================================================================


