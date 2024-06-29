from django.contrib import admin
from src.printers.models import PrintStation

# Register your models here.
INITIAL_DATA = [
    {"id": 1, "name": "Default Printer"},
]


@admin.register(PrintStation)
class PrintStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, station in enumerate(INITIAL_DATA):
            pstation = PrintStation.objects.filter(id=station['id']).first()

            if not pstation:
                pstation = PrintStation.objects.create(**station)
            else:
                pstation.name = station['name']
                pstation.save(force_update=True)
