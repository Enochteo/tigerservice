from django.db import models
from django.contrib.auth.models import User
from organization.models import Event  # Import existing Event model

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} registered for {self.event.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    g_number = models.CharField(max_length=9, null=True, unique=True, blank=True)

