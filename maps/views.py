"""Views for the maps application."""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from .models import MapPoint, ArtifactCategory, Confirmation
from .serializers import MapPointSerializer, ArtifactCategorySerializer
from .permissions import IsEditor, IsAdmin, HasMapAccess

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint."""
    return Response({"status": "ok"}, status=status.HTTP_200_OK)

class ArtifactCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for artifact categories."""

    queryset = ArtifactCategory.objects.all()
    serializer_class = ArtifactCategorySerializer

    def get_permissions(self):
        """Return permissions based on action."""
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]
        return [HasMapAccess()]

class MapPointViewSet(viewsets.ModelViewSet):
    """ViewSet for map points."""

    queryset = MapPoint.objects.all()
    serializer_class = MapPointSerializer
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        """Return permissions based on action."""
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
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        """Delete marker and its image from S3."""
        marker = self.get_object()
        if marker.image:
            marker.image.delete(save=False)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post', 'delete'], url_path='confirm')
    def confirm(self, request, **kwargs):
        """Confirm or unconfirm a marker."""
        marker = self.get_object()

        if marker.author_id == request.user_id:
            return Response(
                {"error": "Cannot confirm your own marker."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            _, created = Confirmation.objects.get_or_create(
                marker=marker,
                author_id=request.user_id
            )
            if not created:
                return Response(
                    {"error": "Already confirmed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_201_CREATED)

        Confirmation.objects.filter(
            marker=marker,
            author_id=request.user_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='image', parser_classes=[MultiPartParser])
    def upload_image(self, request, **kwargs):
        """Upload image for a marker."""
        marker = self.get_object()
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        marker.image = request.FILES['image']
        marker.save()
        return Response({"image_url": marker.image.url}, status=status.HTTP_200_OK)
