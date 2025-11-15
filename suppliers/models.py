from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Product(models.Model):
    """Модель для товаров"""

    name = models.CharField(
        max_length=50, verbose_name="Название", help_text="Введите название товара"
    )
    model_product = models.CharField(
        max_length=200,
        verbose_name="Модель",
        help_text="Введите модель",
        blank=True,
        null=True,
    )
    release_date = models.DateField(
        verbose_name="Дата выхода",
        help_text="Введите дату выхода продукта на рынок",
        default=timezone.now,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Supplier(models.Model):
    """Модель для звеньев сети поставки"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название фирмы",
        help_text="Введите название фирмы",
    )
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Введите страну",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Введите город",
        blank=True,
        null=True,
    )
    address = models.TextField(
        verbose_name="Адрес",
        help_text="Введите адрес (улица, № дома)",
        blank=True,
        null=True,
    )

    FACTORY = "factory"
    RETAIL = "retail"
    ENTREPRENEUR = "entrepreneur"

    TYPE_CHOICES = [
        (FACTORY, "завод"),
        (RETAIL, "розничная сеть"),
        (ENTREPRENEUR, "индивидуальный предприниматель"),
    ]

    type = models.CharField(
        max_length=35,
        choices=TYPE_CHOICES,
        default=FACTORY,
        verbose_name="Тип юридического лица",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="Поставщик (предыдущий уровень)",
        help_text="Выберите поставщика-источник. Если отсутствует — оставьте пустым.",
    )

    level = models.PositiveIntegerField(
        verbose_name="Уровень в иерархии",
        editable=False,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Определяется автоматически",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Метод для автоматического определения уровня"""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Scheme(models.Model):
    """Модель для связи звеньев внутри сети"""

    node = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="schemes")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Задолженность",
        help_text="Размер задолженности перед поставщиком",
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.node.name} — {self.product.name if self.product else 'Нет продукта'}"

    class Meta:
        verbose_name = "Связь звеньев"
        verbose_name_plural = "Связи звеньев"
