from django.db import models
from src.accounts.models import User, Company
from django.conf import settings
from src.core.modules import upload_file_path
from django.db.models import Case, When, Value, F

from decimal import Decimal

def get_measures(size, side):
    page_sizes = {
        "A6": {
            "width": 105,
            "height": 148,
        },
        "A5": {
            "width": 148,
            "height": 210,
        },
        "A4": {
            "width": 210,
            "height": 297,
        },
        "A3": {
            "width": 297,
            "height": 420,
        },
        "A2": {
            "width": 420,
            "height": 594,
        },
        "A1": {
            "width": 594,
            "height": 841,
        },
    }
    return page_sizes[size][side]

class CompanyLetterheadOption(models.Model):
    PAGE_SIZES = (
        ("A6", "A4"),
        ("A5", "A4"),
        ("A4", "A4"),
        ("A3", "A4"),
        ("A2", "A4"),
        ("A1", "A4"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="company_letterhead_options"
    )
    name = models.CharField(
        max_length=30, default='Company Letterhead Options')
    paper_format = models.CharField(max_length=30, default="A4", choices=PAGE_SIZES)
    paper_width = models.PositiveSmallIntegerField(default=get_measures("A4","width"))
    paper_height = models.PositiveSmallIntegerField(default=get_measures("A4","height"))
    top_margin = models.PositiveSmallIntegerField(default=10)
    bottom_margin = models.PositiveSmallIntegerField(default=10)
    left_margin = models.PositiveSmallIntegerField(default=10)
    right_margin = models.PositiveSmallIntegerField(default=10)

    inner_width = models.GeneratedField(
        expression=F("paper_width") - F("left_margin") - F("left_margin"),
        output_field= models.PositiveSmallIntegerField(default=0),
        db_persist=True
        )
    inner_height = models.GeneratedField(
        expression=F("paper_height") - F("left_margin") - F("left_margin"),
        output_field= models.PositiveSmallIntegerField(default=0),
        db_persist=True
        )

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

    def get_measures(paper_format):
        return page_sizes.get(paper_format.upper(), "Invalid paper format")