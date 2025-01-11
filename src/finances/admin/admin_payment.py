from django.contrib import admin
from src.finances.models import Payment, PaymentType
from src.finances.utils import payment_types_initial_data
from src.accounts.models import User


# @admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

# Register your models here.


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ordinal', 'created')
    ordering = ('id', )
    list_filter = ('name', )

    @staticmethod
    def initial_data():
        for index, payment_type in enumerate(payment_types_initial_data):
            user = User.objects.get(id=payment_type['user_id'])
            if not user:
                user = User.objects.first()
            ptp = PaymentType.objects.filter(id=payment_type['id']).first()
            if not ptp:
                # ptp_user = payment_type.pop('user_id')
                ptp = PaymentType(**payment_type)
                ptp.user = user
                ptp.save(force_insert=True)
            else:
                ptp.name = payment_type['name']
                ptp.save(force_update=True)
