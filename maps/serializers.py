from rest_framework import serializers
from .models import MapPoint, ArtifactCategory

class ArtifactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactCategory
        fields = ['id', 'name']

class MapPointSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ArtifactCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = MapPoint
        fields = ['id', 'label', 'category', 'lat', 'lng', 'author_id']

    def get_type(self, obj):
        return "Feature"
