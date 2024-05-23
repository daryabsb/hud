# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.7 (default, Apr 15 2020, 05:09:04) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: .\mysite\base\management\commands\flush_redis.py
# Compiled at: 2023-03-30 16:24:40
# Size of source mod 2**32: 413 bytes
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'flush redis data'

    def handle(self, *args, **options):
        from django_redis import get_redis_connection
        get_redis_connection('default').flushall()
        print('[*]Flush all')
