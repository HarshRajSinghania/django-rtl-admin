from django.contrib import admin

from django_rtl_admin import BidiSafeAdminMixin

from .models import Thing


class BidiThingAdmin(BidiSafeAdminMixin, admin.ModelAdmin):
    list_display = ("name", "name_ar", "reference", "quantity", "is_active", "upper_name")
    list_filter = ("is_active",)
    search_fields = ("name", "reference")

    @admin.display(description="Upper", ordering="name")
    def upper_name(self, obj):
        return obj.name.upper()


class PlainThingAdmin(admin.ModelAdmin):
    list_display = ("name", "reference", "is_active")


admin.site.register(Thing, BidiThingAdmin)
