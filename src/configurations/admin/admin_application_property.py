from django.contrib import admin
from src.accounts.models import User
from src.configurations.models import ApplicationProperty, ApplicationPropertySection
from src.configurations.const import INITIAL_DATA


@admin.register(ApplicationPropertySection)
class ApplicationPropertySectionAdmin(admin.ModelAdmin):
    pass


@admin.register(ApplicationProperty)
class ApplicationPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'value', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    # @staticmethod
    # def initial_data():
    #     for index, cur in enumerate(INITIAL_DATA):
    #         setting = ApplicationProperty.objects.get(name=cur['name'])
    #         if not setting:
    #             setting = ApplicationProperty(**cur)
    #             setting.save(force_insert=True)
    #         else:
    #             setting.name = cur['name']
    #             setting.save(force_update=True)
