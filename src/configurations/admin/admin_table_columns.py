from django.contrib import admin
from src.accounts.models import User
from src.configurations.models import AppTable, AppTableColumn
from src.configurations.const import APP_TABLES, APP_TABLES_COLUMNS


@admin.register(AppTable)
class AppTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for app in APP_TABLES:
            app_name = AppTable.objects.filter(
                name=app).first()
            if not app_name:

                app_name = AppTable(name=app)
                app_name.save(force_insert=True)
            else:
                app_name.name = app
                app_name.save(force_update=True)


@admin.register(AppTableColumn)
class AppTableColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'name', 'title', 'is_enabled',
                    'is_related', 'related_value')
    ordering = ('id', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, col in enumerate(APP_TABLES_COLUMNS):
            column = AppTableColumn.objects.filter(
                name=col['name']).first()
            if not column:
                app_name = AppTable.objects.filter(name=col['app']).first()
                col['app'] = app_name

                column = AppTableColumn(**col)
                column.save(force_insert=True)
            else:
                column.is_enabled = col['is_enabled']
                column.save(force_update=True)
