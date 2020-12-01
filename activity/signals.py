from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.dispatch import receiver
from .utils import set_balance
from .models import Activity, Budget
from django.db.models import Sum


def cash_balance_signal(sender, instance, **kwargs):
    user = instance.user
    current_month = timezone.datetime(year=instance.date.year,
                                      month=instance.date.month,
                                      day=1)
    set_balance(current_month, user)


@receiver(post_save, sender=Activity)
def activity_save_signal(sender, instance, **kwargs):
    cash_balance_signal(sender, instance, **kwargs)


@receiver(post_delete, sender=Activity)
def activity_delete_signal(sender, instance, **kwargs):
    cash_balance_signal(sender, instance, **kwargs)
