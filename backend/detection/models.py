from django.db import models

# Create your models here.

class DetectionResult(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    status = models.CharField(max_length=20)  # AUTHENTIC or MANIPULATED
    score = models.FloatField()
    manipulation_percentage = models.FloatField()
    authenticity_percentage = models.FloatField()
    request_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file_name} - {self.status} ({self.manipulation_percentage}%)"
