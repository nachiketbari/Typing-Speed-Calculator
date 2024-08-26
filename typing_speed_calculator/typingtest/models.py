from django.db import models

# Create your models here.

class TypingTestResult(models.Model):
    user = models.CharField(max_length=100)
    wpm = models.FloatField()
    accuracy = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

