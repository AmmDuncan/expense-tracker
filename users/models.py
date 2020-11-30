from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    CURRENCY_CHOICES = (
        ('', 'Choose...'),
        ('$', 'Dollary ($)'),
        ('GH¢', 'Ghana Cedi (GH¢)')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)

    def __str__(self):
        return self.user.username