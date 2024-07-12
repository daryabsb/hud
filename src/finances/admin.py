from django.contrib import admin

# Register your models here.
from src.finances.models import Fund, Theme, Position, Rationale, AssetClass, FundValue, IndexValue


admin.site.register(Fund)
admin.site.register(Theme)
admin.site.register(Position)
admin.site.register(Rationale)
admin.site.register(AssetClass)
admin.site.register(FundValue)
admin.site.register(IndexValue)
