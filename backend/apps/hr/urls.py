from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, EmployeeDocumentViewSet, JobPositionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'job-positions', JobPositionViewSet, basename='job-position')
router.register(r'documents', EmployeeDocumentViewSet, basename='employee-document')

urlpatterns = [
    path('', include(router.urls)),
]
