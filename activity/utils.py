from django.db.models import Sum
from .models import Budget, Expense
from datetime import datetime


def get_previous_month_budget_date(current_month):
    prev = datetime(month=current_month.month - 1,
                    year=current_month.year, day=1) \
        if current_month.month != 1 else \
        datetime(year=current_month.year - 1, month=12, day=1)
    return prev


def get_prev_month_budget_balance(current_month, user):
    prev_month_date = get_previous_month_budget_date(current_month)
    prev_balance = 0
    try:
        prev_budget = Budget.objects.prefetch_related('activities').get(
            date=prev_month_date, user=user)
        prev_balance = prev_budget.balance
    except Budget.DoesNotExist:
        prev_budget = None

    return prev_balance


def set_balance(current_month, user):
    prev_balance = get_prev_month_budget_balance(current_month, user)

    budget = Budget.objects.prefetch_related('activities') \
        .get_or_create(date=current_month, user=user)[0]

    expenses = 0
    if budget.activities.filter(type='expense') \
            .aggregate(Sum('amount')) \
            .get('amount__sum'):
        expenses = budget.activities.filter(type='expense') \
            .aggregate(Sum('amount')) \
            .get('amount__sum')
    income = 0
    if budget.activities.filter(type='income') \
            .aggregate(Sum('amount')) \
            .get('amount__sum'):
        income = budget.activities.filter(type='income') \
            .aggregate(Sum('amount')) \
            .get('amount__sum')

    if budget.income:
        budget.balance = (budget.income -
                          budget.savings -
                          expenses + income + prev_balance)
    else:
        budget.balance = 0 - expenses + income - budget.savings + prev_balance

    budget.save()