from rest_framework import serializers
from .models import MapPoint, ArtifactCategory

class ArtifactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactCategory
        fields = ['id', 'name']

class MapPointSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    latitude = serializers.DecimalField(decimal_places=12, max_digits=20, write_only=True)
    longitude = serializers.DecimalField(decimal_places=12, max_digits=20, write_only=True)

    class Meta:
            model = MapPoint
            fields = ['id', 'name', 'category', 'type', 'geometry', 'latitude', 'longitude', 'user_id', 'created_at']

    def get_type(self, obj):
        return "Feature"

    def get_geometry(self, obj):
        return {
            "type": "Point",
            "coordinates": [float(obj.longitude), float(obj.latitude)]
        }
