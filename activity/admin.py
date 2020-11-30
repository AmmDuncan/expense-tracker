from django.contrib import admin
from .models import Activity, Budget
from .forms import ActivityForm, BudgetForm


# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    form = ActivityForm
    add_form = ActivityForm
    model = Activity


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    add_form = BudgetForm
    model = Budget
    list_display = ['__str__',
                    'income' ,
                    'total_expenses',
                    'total_income',
                    'balance']
