# your_app_name/management/commands/run_celery_worker.py

from django.core.management.base import BaseCommand
from subprocess import call


class Command(BaseCommand):
    help = 'Starts a Celery worker alongside the Django development server.'

    def handle(self, *args, **options):
        call(["celery", "-A", "src", "worker", "--loglevel=info", "--pool=solo"])
