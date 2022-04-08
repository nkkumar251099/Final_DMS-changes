from django.db import models


# Create your models here.
class Volunteer(models.Model):
    username = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=13)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    aadhar_image_path = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)

    def __str__(self):
        return '%s, %s' % (self.username, self.email)
