from django.db import models
import uuid

def marker_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'markers/{uuid.uuid4()}.{ext}'


class ArtifactCategory(models.Model):

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class MapPoint(models.Model):
    label = models.CharField(max_length=255)
    category = models.ForeignKey(ArtifactCategory, on_delete=models.CASCADE)
    lat = models.DecimalField(decimal_places=18, max_digits=20, default=0.0)
    lng = models.DecimalField(decimal_places=18, max_digits=20, default=0.0)
    author_id = models.IntegerField()
    image = models.ImageField(upload_to=marker_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.label

class Confirmation(models.Model):
    marker = models.ForeignKey(MapPoint, on_delete=models.CASCADE, related_name='confirmations')
    author_id = models.IntegerField()
    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['marker', 'author_id']]
