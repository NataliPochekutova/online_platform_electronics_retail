from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Product, Scheme, Supplier
from suppliers.serializers import (ProductSerializer, SchemeSerializer,
                                   SupplierSerializer)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class SchemeViewSet(ModelViewSet):
    serializer_class = SchemeSerializer
    queryset = Scheme.objects.all()


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("country",)
