from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, FeeCategoryViewSet

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'fee-categories', FeeCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
