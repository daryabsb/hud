from django.db import models
from src.accounts.models import User, Company
from django.conf import settings
from src.core.modules import upload_file_path


class CompanyLetterheadOption(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="company_letterhead_options"
    )
    name = models.CharField(
        max_length=30, default='Company Letterhead Options')
    font_family = models.CharField(
        max_length=30, default=settings.DEFAULT_FONT_FAMILY)
    unicode_font = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    unicode_text_header_size = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_UNICODE_HEADER_TEXT_SIZE)
    text_header_size = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_HEADER_TEXT_SIZE)
    unicode_text_content_size = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_UNICODE_CONTENT_TEXT_SIZE)
    text_content_size = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_CONTENT_TEXT_SIZE)
    table_text_content_size = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_TABLE_TEXT_SIZE)

    font_family = models.CharField(max_length=30, default='helvetica')
    font_family = models.CharField(max_length=30, default='helvetica')
    font_family = models.CharField(max_length=30, default='helvetica')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
