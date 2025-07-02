from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    teacher = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.CharField(max_length=200)
    sessions = models.IntegerField(default=0)  # Tổng số buổi
    curriculum = models.TextField(blank=True)
    note = models.TextField(blank=True)
    participants = models.IntegerField(default=0)

    def __str__(self):
        return self.name

