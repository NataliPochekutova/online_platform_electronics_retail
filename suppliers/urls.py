from rest_framework.routers import DefaultRouter

from suppliers.apps import SuppliersConfig
from suppliers.views import ProductViewSet, SchemeViewSet, SupplierViewSet

app_name = SuppliersConfig.name

router = DefaultRouter()
router.register("scheme", SchemeViewSet, basename="scheme")
router.register("product", ProductViewSet, basename="product")
router.register("supplier", SupplierViewSet, basename="supplier")

urlpatterns = [] + router.urls
