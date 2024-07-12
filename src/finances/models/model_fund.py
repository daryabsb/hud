from django.db import models
from src.accounts.models import Country, Region


class Fund(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    market_summary = models.TextField()

    def __str__(self):
        return self.name


class Theme(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)
    target_PL = models.IntegerField()
    fund = models.ForeignKey(
        'Fund', on_delete=models.CASCADE, related_name='themes')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    asset_class = models.ForeignKey('AssetClass', on_delete=models.CASCADE)
    live = models.BooleanField()  # Entry = True, Exit = False, see Rationale

    def __str__(self):
        return '%s - %s' % (self.name, self.fund)

    @property
    def live_rationale(self):
        try:
            rationale = Rationale.objects.get(theme=self, action='Entry')
        except:
            rationale = False
        return rationale

    @property
    def closed_rationale(self):
        try:
            rationale = Rationale.objects.get(theme=self, action='Exit')
        except:
            rationale = False
        return rationale


class Position(models.Model):
    # current P&L position for a Theme
    theme = models.OneToOneField('Theme', on_delete=models.CASCADE)
    var = models.IntegerField()
    cvar = models.IntegerField()
    LTD = models.IntegerField()
    SL = models.IntegerField()

    def __str__(self):
        return 'position for theme %s ' % self.theme.name


class Rationale(models.Model):
    # Rationale for either Entry or Exit of a Theme
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE)
    action = models.CharField(max_length=10)  # Entry or Exit
    rationale = models.TextField()
    date = models.DateField()

    def __str__(self):
        return 'trade rationale for theme %s ' % self.theme.name


class AssetClass(models.Model):
    NAME_LENGTH = 50
    name = models.CharField(max_length=NAME_LENGTH)

    class Meta:
        verbose_name_plural = "Asset Classes"

    def __str__(self):
        return self.name


class FundValue(models.Model):
    fund = models.ForeignKey("Fund", on_delete=models.CASCADE)
    date = models.DateField()
    value = models.IntegerField()

    def __str__(self):
        return '%d is the value of %s at %s' % (self.value, self.fund.name, self.date)


class IndexValue(models.Model):
    date = models.DateField()
    value = models.IntegerField()

    def __str__(self):
        return '%d is the value of the index at %s' % (self.value, self.date)
