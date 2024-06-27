from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=120)
    massage = models.CharField(max_length=255)

    def __str__(self):
        return self.name
