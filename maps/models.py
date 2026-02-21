from django.db import models

class ArtifactCategory(models.Model):

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class MapPoint(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ArtifactCategory, on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=12, max_digits=20)
    longitude = models.DecimalField(decimal_places=12, max_digits=20)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
