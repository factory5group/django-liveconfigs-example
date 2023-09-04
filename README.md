# Пример использования пакета LIVECONFIGS
1. Выполните клонирование репозитория в удобное для вас место
2. Выполните команды
```
 docker volume create db_data_liveconfigs
 docker volume create redis_data_liveconfigs
 docker volume create django_static_liveconfigs
 ln -s environment.example environment
 docker-compose up --build -d
 docker-compose run --rm django ./manage.py createsuperuser
```
3. Сайт будет доступен по адресу http://127.0.0.1:8080

# LIVECONFIGS
### Удобный пакет для управления конфигами на лету.

## Установка (простое использование)
1. Выполните установку пакета стандартным образом
```
 pip install
```
2. В настройках проекта:
- включите `liveconfigs` в разделе приложений
```
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    "liveconfigs",
]
```
- Добавьте настройку `LIVECONFIGS_SYNCWRITE` равную True или False
```
LIVECONFIGS_SYNCWRITE=True
```
Этот параметр отвечает за режим записи вспомогательных данных (время изменения, время последнего доступа к конкретному конфигу) в базу данных.
```
True - запись происходит синхронно
False - запись производится отложенной задачей в отдельном контейнере Celery
```
- Если вы установили значение False, вам нужно создать отдельный контейнер (пример можно найти тут) или использовать имеющийся. Также нужно настроить запуск задачи `liveconfigs.tasks.config_row_update_or_create` например так
```
CELERY_TASK_ROUTES = {
    'apps.liveconfigs.tasks.config_row_update_or_create': {'queue': 'quick', 'routing_key': 'quick'},
}
```
3. Создайте файл с конфигами в удобном месте. Например, файл `config.py` в директории `config`, созданной на уровне проекта (рядом с файлом `manage.py`).
Пример структуры файла `config.py` приведен в каталоге doc в нашем репозитории
4. Добавьте в этапы запуска вашего сервера загрузку конфигов. Пример можно найти в каталоге `doc` в файле `start`
5. Добавьте в этапы запуска вашего сервера `manage.py migrate` (или выполните их вручную).

## Просмотр и изменение конфигов
Просто загляните в админку в раздел `Config rows`

## Использование в коде
Нет ничего проще.
1. Имортируйте созданный ранее конфиг `from config import config`
2. Используйте его в коде `days = config.FirstExample.DAYS`
```
from django.http import HttpResponse
from config import config


def index(request):
    simple_body = f"""
    <p>Hello, world. You're at the index page</p>
    <p>Some data from config are here:</p>
    <p>DAYS={config.FirstExample.DAYS}</p>
    <p>FIRST_DAY_OF_WEEK={config.FirstExample.FIRST_DAY_OF_WEEK}</p>
    <p>TYPES_OF_LOADING={config.FirstExample.TYPES_OF_LOADING}</p>
    <p>USE_CALENDAR={config.FirstExample.USE_CALENDAR}</p>
    <p>SECRET_SWITCH={config.FirstExample.SECRET_SWITCH}</p>
    <p>CONSOLIDATION_GROUPS={config.FirstExample.CONSOLIDATION_GROUPS}</p>

    <p>You can change configs <a href="/admin/liveconfigs/configrow/">here</a> and reload this page for checking changes.</p>
    """
    return HttpResponse(simple_body)
```
