from django.db import models

# Create your models here.
class Fertilizers(models.Model):
    Fertilizer_Name = models.CharField(max_length=100)
    Best_Buyer_Link = models.URLField(max_length=100)
    Description = models.TextField(max_length=200)
    def __str__(self):
        return self.Fertilizer_Name

class WeatherPrediction(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    moisture = models.FloatField()
    soil_type = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100)
    predicted_fertilizer = models.CharField(max_length=100)
    nitrogen = models.IntegerField()
    potassium = models.IntegerField()
    phosphorous = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_type} - {self.predicted_fertilizer} ({self.created_at})"

