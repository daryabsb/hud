from django.db import models


class AppTable(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AppTableColumn(models.Model):
    app = models.ForeignKey("AppTable", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)
    is_related = models.BooleanField(default=False)
    related_value = models.CharField(max_length=50, null=True, blank=True)
    searchable = models.BooleanField(default=False)
    orderable = models.BooleanField(default=True)

    def __str__(self):
        return self.title
