from rest_framework import viewsets
from .models import MapPoint, ArtifactCategory
from .serializers import MapPointSerializer, ArtifactCategorySerializer
from .permissions import IsEditor, IsAdmin, HasMapAccess

class ArtifactCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArtifactCategory.objects.all()
    serializer_class = ArtifactCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]
        return [HasMapAccess()]

class MapPointViewSet(viewsets.ModelViewSet):
    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer
    http_method_names = ['get', 'post', 'delete']

    # FOR DEBUGGING
    def create(self, request, *args, **kwargs):
        print("BODY:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        print("ERRORS:", serializer.errors)
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [HasMapAccess()]
        if self.action == 'create':
            return [IsEditor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [HasMapAccess()]
