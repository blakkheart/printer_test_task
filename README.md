
# 🖨 Printer API 🖨

## Описание

 Проект выполнен в качестве тестового задания.
 1.  Сервис получает информацию о новом заказе из ERP, создаёт в БД чеки для всех принтеров точки, указанной в заказе, и ставит асинхронные задачи на генерацию PDF-файлов для этих чеков. Если у точки нет ни одного принтера - возвращает ошибку. Если чеки для данного заказа уже были созданы - возвращает ошибку.
2.  Асинхронный worker с помощью wkhtmltopdf генерируют PDF-файл из HTML-шаблона. Имя файла имеет следующий вид <ID заказа>_<тип чека>.pdf (123456_client.pdf).
3.  Приложение опрашивает сервис на наличие новых чеков. Опрос происходит по следующему пути: сначала запрашивается список чеков, которые уже сгенерированы для конкретного принтера, после скачивается PDF-файл для каждого чека и отправляется на печать.
 ![enter image description here](https://github.com/smenateam/assignments/blob/master/backend/images/arch.png?raw=true)

## Стэк технологий

- [Django](https://www.djangoproject.com/) — база приложения.
- [DRF](https://www.django-rest-framework.org/) — для реализации API.
- [PostgreSQL](https://www.postgresql.org/) — в качестве базы данных.
- [wkhtmltopdf](https://wkhtmltopdf.org/) — для генерации PDF из HTML.
- [Requests](https://requests.readthedocs.io/en/latest/) — для работы с wkhtmltopdf.
- [Redis](https://redis.io/) — для работы Celery.
- [Celery](https://docs.celeryq.dev/en/stable/) — для реализации выполнения фоновых задач в связке с wkhtmltopdf.
- [Docker](https://www.docker.com/) — контейнеризация приложения.
- [Nginx](https://www.nginx.com/)  — для раздачи статики в docker.

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/blakkheart/printer_test_task.git
```
2. Перейдите в директорию проекта:
```bash
cd printer_test_task
```
3. Установите и активируйте виртуальное окружение:
   - Windows
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
   - Linux/macOS
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Обновите [pip](https://pip.pypa.io/en/stable/):
   - Windows
   ```bash
   (venv) python -m pip install --upgrade pip
   ```
   - Linux/macOS
   ```bash
   (venv) python3 -m pip install --upgrade pip
   ```
5. Установите зависимости из файла requirements.txt:
   ```bash
   (venv) pip install -r requirements.txt
   ```
Создайте и заполните файл *.env* по примеру с файлом *.env.example*, который находится в корневой директории.



## Использование  

1. Введите команду для запуска докер-контейнера:
	```bash
	docker compose up
	```
3. Соберите и скопируйте статику:
	```bash
	docker compose exec backend python manage.py collectstatic
	docker compose exec backend cp -r /forfar_app/static/. /backend_static/static/
	```
Если все сделано корректно, сервер запустится по адресу localhost:8000 и вы сможете получить доступ к API.
Доступны эндпоинты:
 - **localhost:8000/create_checks/**   —   POST запрос
  - **localhost:8000/new_checks/?api_key=<API_KEY>**   —   GET запрос
  - **localhost:8000/check/?api_key=<API_KEY>&check_id=<CHECK_ID>**   —   GET запрос
 - **localhost:8000/admin/**


### API

Описание доступных методов находится в файле api.yml (swagger-спецификация). Можно отрендерить через  [онлайн редактор](https://editor.swagger.io/)  или через соответствующий плагин для PyCharm или VSCode.

### Дополнительно
При запуске сервера автоматические создаются и применяются миграции, а также загружаются фикстуры.

Также вы можете создать суперпользователя и изменять значения через админ-панель по адресу localhost:8000/admin/ :
```bash
docker compose exec backend python manage.py createsuperuser
```

