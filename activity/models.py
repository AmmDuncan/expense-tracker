from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum


# Create your models here.
from django.db.models import ForeignKey


class Budget(models.Model):
    income = models.FloatField("monthly income", default=0, blank=True)
    savings = models.FloatField("monthly savings", default=0, blank=True,)
    date = models.DateField()
    balance = models.FloatField(blank=True, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def total_expenses(self):
        return self.activities.filter(type='expense')\
            .aggregate(Sum('amount'))\
            .get('amount__sum')

    def total_income(self):
        incomes = 0
        if len(self.activities.filter(type='income')) > 0:
            incomes = self.activities.filter(type='income') \
                .aggregate(Sum('amount')) \
                .get('amount__sum')
        return incomes + self.income

    def __str__(self):
        return f"{self.date.strftime('%B')} budget of {self.user.username}"


class Activity(models.Model):
    TYPE_CHOICES = (
        ("expense", 'Expense'),
        ("income", 'Income')
    )
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    budget = ForeignKey(Budget, on_delete=models.CASCADE, related_name='activities')
    amount = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')

    def __str__(self):
        return self.title


class Expense(models.Model):
    pass