from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, LevelViewSet, PackageViewSet,
    AcademicYearViewSet, AcademicPeriodViewSet, StudyClassViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
router.register(r'academic-periods', AcademicPeriodViewSet, basename='academic-period')
router.register(r'study-classes', StudyClassViewSet, basename='study-class')

urlpatterns = [
    path('', include(router.urls)),
]
