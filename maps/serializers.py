from rest_framework import serializers
from .models import MapPoint, ArtifactCategory, Confirmation

class ArtifactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactCategory
        fields = ['id', 'name']

class ConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Confirmation
        fields = ['id', 'author_id', 'confirmed_at']

class MapPointSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ArtifactCategory.objects.all(),
        slug_field='name'
    )
    confirm_count = serializers.SerializerMethodField()
    confirmed_by_me = serializers.SerializerMethodField()

    class Meta:
        model = MapPoint
        fields = ['id', 'label', 'category', 'lat', 'lng', 'author_id', 'confirm_count', 'confirmed_by_me']

    def get_confirm_count(self, obj):
        return obj.confirmations.count()

    def get_confirmed_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user_id:
            return obj.confirmations.filter(author_id=request.user_id).exists()
        return False

    def get_type(self, obj):
        return "Feature"
