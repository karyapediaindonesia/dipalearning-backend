from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AbsenceReasonViewSet

router = DefaultRouter()
router.register(r'absence-reasons', AbsenceReasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
