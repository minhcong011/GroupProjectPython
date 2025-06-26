from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username