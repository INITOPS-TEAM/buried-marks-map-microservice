from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maps.views import MapPointViewSet, ArtifactCategoryViewSet

router = DefaultRouter()
router.register('points', MapPointViewSet)
router.register('categories', ArtifactCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
