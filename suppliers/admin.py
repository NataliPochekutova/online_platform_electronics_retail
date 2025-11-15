from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Scheme, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели поставщик"""

    list_display = (
        "id",
        "name",
        "email",
        "country",
        "city",
        "address",
        "level",
        "created_at",
    )
    list_filter = ("city", "name")
    search_fields = (
        "city",
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели продукт"""

    list_display = ("id", "name", "model_product", "release_date", "created_at")
    list_filter = ("name",)
    search_fields = (
        "name",
        "model_product",
    )

    @admin.register(Scheme)
    class SchemeAdmin(admin.ModelAdmin):
        """Класс для настройки отображения модели заказ"""

        list_display = ("id", "product", "supplier_link", "debt", "created_at")
        list_filter = ("supplier__city",)
        actions = ["clear_debt"]

        def supplier_link(self, obj):
            url = f"/admin/suppliers/supplier/{obj.supplier.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

        supplier_link.short_description = "Поставщик"

        def clear_debt(self, request, queryset):
            for scheme in queryset:
                scheme.debt = 0
                scheme.save()
            self.message_user(request, "Задолженность очищена для выбранных схем.")

        clear_debt.short_description = "Очистить задолженность"
