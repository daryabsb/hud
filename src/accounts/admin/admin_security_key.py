from django.contrib import admin
from src.accounts.models import User
from src.accounts.models import SecurityKey
from src.configurations.const import SECURITY_KEY_INITIAL_DATA


@admin.register(SecurityKey)
class SecurityKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'user')
    ordering = ('created', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, sec in enumerate(SECURITY_KEY_INITIAL_DATA):
            security = SecurityKey.objects.filter(name=sec['name']).first()
            if not security:
                user = User.objects.first()
                sec['user'] = user
                security = SecurityKey(**sec)
                security.save(force_insert=True)
            else:
                security.name = sec['name']
                security.save(force_update=True)
