import csv
import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filename=os.path.join(settings.CSV_FILES_DIR, 'load_data.log')
)

logger = logging.getLogger(__name__)


TABLES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': Title.genre.through,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_csv_file(file_name):
    csv_file = file_name + '.csv'
    csv_path = os.path.join(settings.CSV_FILES_DIR, csv_file)
    try:
        with (open(csv_path, encoding='utf-8')) as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        logger.error(f'Файл {csv_file} не найден.')
        return


def change_foreign_values(data_csv):
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file_name, class_name):
    table_not_loaded = f'Таблица {class_name.__qualname__} не загружена.'
    table_loaded = f'Таблица {class_name.__qualname__} загружена.'
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            logger.error(
                f'Ошибка в загружаемых данных. {error}. {table_not_loaded}'
            )
            break
    logger.info(table_loaded)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for key, value in TABLES.items():
            logger.info(f'Загрузка таблицы {value.__qualname__}')
            load_csv(key, value)
