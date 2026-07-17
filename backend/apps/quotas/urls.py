from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentQuotaViewSet, QuotaTransactionViewSet

router = DefaultRouter()
router.register(r'student-quotas', StudentQuotaViewSet, basename='studentquota')
router.register(r'quota-transactions', QuotaTransactionViewSet, basename='quotatransaction')

urlpatterns = [
    path('', include(router.urls)),
]
