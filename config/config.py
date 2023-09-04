import operator

from enum import Enum

from liveconfigs import models, validators

# isort: off

# config_row_update_signal_handler begin
from django.conf import settings
from django.dispatch import receiver
from liveconfigs.signals import config_row_update_signal
from liveconfigs.tasks import config_row_update_or_create

# FIXME: Импорт приложения Celery из вашего проекта (если используете Celery)
# FIXME: Вам нужно изменить этот код, если вы используете не Celery
from celery_app import app

# isort: on


# Пример для Celery
# Реальное сохранение данных выполняет функция config_row_update_or_create
# Реализуйте отложенное сохранение удобным для вас методом
# Для Celery зарегистрируйте эту задачу в CELERY_TASK_ROUTES
# FIXME: Вам нужно изменить этот код, если вы используете не Celery
@app.task(max_retries=1, soft_time_limit=1200, time_limit=1500)
def config_row_update_or_create_proxy(config_name: str, update_fields: dict):
    config_row_update_or_create(config_name, update_fields)


@receiver(config_row_update_signal, dispatch_uid="config_row_update_signal")
def config_row_update_signal_handler(sender, config_name, update_fields, **kwargs):
    # Пример для Celery
    # При настройках для синхронного сохранения функция будет вызвана напрямую
    if settings.LIVECONFIGS_SYNCWRITE:
        config_row_update_or_create_proxy_func = config_row_update_or_create_proxy
    # При настройках для асинхронного сохранения функция будет вызвана через delay
    # FIXME: Вам нужно изменить этот код, если вы используете не Celery
    else:
        config_row_update_or_create_proxy_func = config_row_update_or_create_proxy.delay

    config_row_update_or_create_proxy_func(config_name, update_fields)


# config_row_update_signal_handler end

class ConfigTags(str, Enum):
    front = "Настройки для фронта"
    features = "Фичи"
    basic = "Основные"


class FirstExample(models.BaseConfig):
    __topic__ = "Описание первой группы настроек"
    __exported__ = [
        "DAYS",
        "FIRST_DAY_OF_WEEK",
        "TYPES_OF_LOADING",
        "USE_CALENDAR",
        "CONSOLIDATION_GROUPS",
    ]

    DAYS: int = 5
    DAYS_DESCRIPTION = "Количество рабочих дней в неделе"
    DAYS_TAGS = [ConfigTags.front, ConfigTags.basic]
    DAYS_VALIDATORS = [validators.greater_or_equal_than(1)]

    FIRST_DAY_OF_WEEK: str | None = None
    FIRST_DAY_OF_WEEK_DESCRIPTION = "Первый день недели"
    FIRST_DAY_OF_WEEK_TAGS = [ConfigTags.features]

    FUEL_PRICES: dict[str, float] = {
        "92": 50.5,
        "95": 55.8,
    }
    FUEL_PRICES_DESCRIPTION = "Стоимость различных видов топлива"
    FUEL_PRICES_TAGS = [ConfigTags.basic]
    FUEL_PRICES_VALIDATORS = [validators.dict_values_are(validators.greater_than(0))]

    USE_CALENDAR: bool = False
    USE_CALENDAR_DESCRIPTION = "Использовать производственнный календарь"
    USE_CALENDAR_TAGS = [ConfigTags.basic]

    SECRET_SWITCH: bool = False
    SECRET_SWITCH_DESCRIPTION = "Настройка не для экспорта!"
    SECRET_SWITCH_TAGS = [ConfigTags.features]

    CONSOLIDATION_GROUPS: list[list[str] | None] = []
    CONSOLIDATION_GROUPS_DESCRIPTION = "Список комбинаций"
    CONSOLIDATION_GROUPS_TAGS = [ConfigTags.features]
    CONSOLIDATION_GROUPS_VALIDATORS = [validators.list_of_lists_includes_unique_elements]
