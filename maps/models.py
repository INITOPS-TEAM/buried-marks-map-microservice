from django.db import models

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

    def __str__(self):
        return self.label
