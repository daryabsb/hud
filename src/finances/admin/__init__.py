from django.contrib import admin
from src.finances.models import (
    Fund, Theme, Position, Rationale, AssetClass,
    FundValue, IndexValue, Payment, PaymentType
)
from .admin_payment import PaymentAdmin

admin.site.register(Fund)
admin.site.register(Theme)
admin.site.register(Position)
admin.site.register(Rationale)
admin.site.register(AssetClass)
admin.site.register(FundValue)
admin.site.register(IndexValue)
# admin.site.register(PaymentType)
admin.site.register(Payment, PaymentAdmin)
