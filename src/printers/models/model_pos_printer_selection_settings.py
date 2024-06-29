from django.db import models
from src.accounts.models import User


class PosPrinterSelectionSettings(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="pos_printer_selection_settings"
    )
    pos_printer_selection = models.ForeignKey(
        "PosPrinterSelection",
        on_delete=models.CASCADE,
        null=True,
        related_name="pos_printer_selection_settings",
    )
    paper_width = models.SmallIntegerField(default=32)
    header = models.CharField(max_length=100)
    footer = models.CharField(max_length=100)
    feed_lines = models.SmallIntegerField(default=0)
    cut_paper = models.BooleanField(default=0)
    print_bitmap = models.SmallIntegerField(default=0)
    open_cash_drawer = models.BooleanField(default=1)
    cash_drawer_command = models.CharField(max_length=100)
    header_alignment = models.SmallIntegerField(default=0)
    footer_alignment = models.SmallIntegerField(default=0)
    is_formatting_enabled = models.BooleanField(default=False)
    printer_type = models.SmallIntegerField(default=0)
    number_of_copies = models.SmallIntegerField(default=1)
    code_page = models.SmallIntegerField(default=-1)
    character_set = models.SmallIntegerField(default=-1)
    margin = models.SmallIntegerField(default=0)
    left_margin = models.FloatField(default=1)
    top_margin = models.FloatField(default=0)
    right_margin = models.FloatField(default=0)
    bottom_margin = models.FloatField(default=0)
    print_barcode = models.SmallIntegerField(default=1)
    font_name = models.CharField(max_length=100)
    font_size_percent = models.FloatField(default=100.0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "PosPrinterSelectionSettings"

    def __str__(self):
        return f"Settings for: {self.pos_printer_selection.printer_name}"
