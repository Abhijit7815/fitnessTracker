from django.db import models

class Person(models.Model):
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Workout(models.Model):
    name = models.CharField(max_length=100)
    workout_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='workout_images/')
    description = models.TextField()

    def __str__(self):
        return self.name
