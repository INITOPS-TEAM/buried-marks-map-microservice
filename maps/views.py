from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import MapPoint, ArtifactCategory, Confirmation
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

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [HasMapAccess()]
        if self.action == 'create':
            return [IsEditor()]
        if self.action == 'destroy':
            return [IsAdmin()]
        if self.action == 'confirm':
            return [HasMapAccess()]
        return [HasMapAccess()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post', 'delete'], url_path='confirm')
    def confirm(self, request, pk=None):
        marker = self.get_object()

        if marker.author_id == request.user_id:
            return Response(
                {"error": "Cannot confirm your own marker."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            confirmation, created = Confirmation.objects.get_or_create(
                marker=marker,
                author_id=request.user_id
            )
            if not created:
                return Response(
                    {"error:" "Already confirmed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            Confirmation.objects.filter(
                marker=marker,
                author_id=request.user_id
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='image', parser_classes=[MultiPartParser])
    def upload_image(self, request, pk=None):
        marker = self.get_object()
        if 'image' not in request.FILES:
            return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)
        marker.image = request.FILES['image']
        marker.save()
        return Response({"image_url": marker.image.url}, status=status.HTTP_200_OK)
