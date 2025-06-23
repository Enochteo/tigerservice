from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='org_logos/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])



class Event(models.Model):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    event_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to="images/events")
    registered_students = models.ManyToManyField(User, through="student.Registration", related_name="registered_events")
    registration_open = models.BooleanField(default=True)
    def __str__(self):
        return self.title
