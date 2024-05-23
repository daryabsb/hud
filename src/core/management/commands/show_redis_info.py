# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.7 (default, Apr 15 2020, 05:09:04) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: .\src\base\management\commands\show_redis_info.py
# Compiled at: 2022-05-13 11:14:26
# Size of source mod 2**32: 340 bytes
import json
from django.core.management.base import BaseCommand
from src.tools.redis_utils import celery_worker_redis, celery_result_redis


class Command(BaseCommand):

    def handle(self, *args, **options):
        main()


def main():
    info = celery_worker_redis.get_info()
    print(json.dumps(info, indent=4))
