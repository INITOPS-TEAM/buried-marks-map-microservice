"""URL configuration for config project."""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maps.views import MapPointViewSet, ArtifactCategoryViewSet, health_check

router = DefaultRouter()
router.register('markers', MapPointViewSet)
router.register('categories', ArtifactCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('health/', health_check),
]
