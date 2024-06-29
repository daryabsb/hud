from django.db import models


class PrintStationPosPrinterSelection(models.Model):
    print_station = models.ForeignKey("PrintStation", on_delete=models.CASCADE)
    pos_printer_selection = models.ForeignKey(
        "PosPrinterSelection", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["print_station", "pos_printer_selection"],
                name="unique_printer_pos_printer_selection",
            )
        ]

    def __str__(self):
        return f"{self.print_station.name} - {self.pos_printer_selection}"
