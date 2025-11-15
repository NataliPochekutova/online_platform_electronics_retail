from rest_framework import serializers

from suppliers.models import Product, Scheme, Supplier


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = "__all__"


class SchemeSerializer(serializers.ModelSerializer):
    debt = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Scheme
        fields = "__all__"
