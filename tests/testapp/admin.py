from django.contrib import admin
from django.db.models import F
from django.db.models.functions import Lower

from django_admin_display import admin_display

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "name_length",
        "active_icon",
        "nickname",
        "owner_lower",
    ]

    @admin_display(boolean=True, short_description="Active")
    def active_icon(self, obj: Company) -> bool:
        return obj.is_active

    @admin_display(empty_value_display="(none)", short_description="Nickname")
    def nickname(self, obj: Company) -> None:
        return None

    @admin_display(
        admin_order_field=Lower(F("owner_name")),
        short_description="Owner (lower)",
    )
    def owner_lower(self, obj: Company) -> str:
        return obj.owner_name.lower()
