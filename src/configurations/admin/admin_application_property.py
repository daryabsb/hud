from django.contrib import admin
from src.accounts.models import User
from src.configurations.models import ApplicationProperty


INITIAL_DATA = [
    {"id": 1, "name": "Theme.mode", "value": 'dark'},
    {"id": 2, "name": "Theme.color", "value": 'pink'},
    {"id": 3, "name": "Theme.cover", "value": '1'},
    {"id": 3, "name": "Site.title", "value": 'Zeneon LLC.'},
    {"id": 3, "name": "Site.language", "value": 'en-us'},
    {"id": 3, "name": "Site.writing_direction", "value": 'left_to_right'},
    {"id": 3, "name": "Site.cover", "value": '1'},
]


@admin.register(ApplicationProperty)
class ApplicationPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'value', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    # @staticmethod
    # def initial_data():
    #     for index, cur in enumerate(INITIAL_DATA):
    #         currency = ApplicationProperty.objects.filter(name=cur['name']).first()
    #         if not currency:
    #             user = User.objects.get(email='root@root.com')
    #             currency = ApplicationProperty(**cur)
    #             currency.user = user
    #             currency.save(force_insert=True)
    #         else:
    #             currency.code = cur['code']
    #             currency.save(force_update=True)
