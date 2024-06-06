from django.contrib import admin
from src.accounts.models import User
from src.configurations.models import ApplicationProperty, ApplicationPropertySection
from src.configurations.const import SECTIONS_INITIAL_DATA, SETTINGS_INITIAL_DATA


@admin.register(ApplicationPropertySection)
class ApplicationPropertySectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', 'icon', 'description')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, sec in enumerate(SECTIONS_INITIAL_DATA):
            section = ApplicationPropertySection.objects.filter(
                name=sec['name']).first()
            if not section:

                section = ApplicationPropertySection(**sec)
                section.save(force_insert=True)
            else:
                section.name = sec['name']
                section.save(force_update=True)


@admin.register(ApplicationProperty)
class ApplicationPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'title', 'value', 'updated')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, cur in enumerate(SETTINGS_INITIAL_DATA):
            setting = ApplicationProperty.objects.filter(
                name=cur['name']).first()
            section = ApplicationPropertySection.objects.filter(
                name=cur['section']).first()
            cur['section'] = section
            if not setting:
                setting = ApplicationProperty(**cur)
                setting.save(force_insert=True)
            else:
                setting.name = cur['name']
                setting.input_type = cur['input_type']
                setting.params = cur['params']
                setting.value = cur['value']
                if not setting.section:
                    setting.section = section
                setting.save(force_update=True)
