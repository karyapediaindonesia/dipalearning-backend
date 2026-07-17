from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProspectViewSet, StudentViewSet, EnrollmentViewSet, ProspectStatusViewSet

router = DefaultRouter()
router.register(r'prospect-statuses', ProspectStatusViewSet, basename='prospect-status')
router.register(r'prospects', ProspectViewSet, basename='prospect')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
