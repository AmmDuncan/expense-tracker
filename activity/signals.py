from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
from .models import Activity, Budget
from django.db.models import Sum


def cash_balance_signal(sender, instance, **kwargs):
    user = instance.user
    current_month = timezone.datetime(year=instance.date.year,
                                      month=instance.date.month,
                                      day=1)
    last_month = current_month - timedelta(weeks=4)
    prev_balance = 0
    try:
        prev_budget = Budget.objects.prefetch_related('activities').get(
            date=last_month, user=user)
        prev_balance = prev_budget.balance
    except Budget.DoesNotExist:
        prev_budget = None

    budget = Budget.objects.prefetch_related('activities') \
        .get_or_create(date=current_month, user=user)[0]

    expenses = 0
    if budget.activities.filter(type='expense')\
            .aggregate(Sum('amount'))\
            .get('amount__sum'):
        expenses = budget.activities.filter(type='expense')\
            .aggregate(Sum('amount'))\
            .get('amount__sum')
    income = 0
    if budget.activities.filter(type='income')\
            .aggregate(Sum('amount'))\
            .get('amount__sum'):
        income = budget.activities.filter(type='income')\
            .aggregate(Sum('amount'))\
            .get('amount__sum')

    if budget.income:
        budget.balance = (budget.income -
                          budget.savings -
                          expenses + income + prev_balance)
    else:
        budget.balance = 0 - expenses + income - budget.savings + prev_balance

    budget.save()


@receiver(post_save, sender=Activity)
def cash_balance_save_signal(sender, instance, **kwargs):
    cash_balance_signal(sender, instance, **kwargs)


@receiver(post_delete, sender=Activity)
def cash_balance_delete_signal(sender, instance, **kwargs):
    cash_balance_signal(sender, instance, **kwargs)
