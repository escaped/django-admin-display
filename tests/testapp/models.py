from django.db import models

from django_admin_display import admin_display


class Company(models.Model):
    name = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    @admin_display(short_description="Company owner", admin_order_field="owner_name")
    def owner(self) -> str:
        return self.owner_name

    @property
    @admin_display(short_description="Name length")
    def name_length(self) -> int:
        return len(self.name)
