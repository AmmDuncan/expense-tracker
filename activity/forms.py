from django import forms
from .models import Budget, Activity
from django.utils import timezone
from datetime import date
from django.db.models import Sum
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Column


class ActivityForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'min': '0.1', 'step': '0.01'}))
    # type = forms.ChoiceField()

    class Meta:
        model = Activity
        fields = ['title', 'amount', 'type']
        labels = {
            'title': 'Transaction'
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-12'),
            ),
            Row(
                Column('amount', css_class='col-12'),
            ),
            Row(
                Column('type', css_class='col-12'),
            ),
            Submit('submit', 'Add', css_class='btn-success')
        )
        self.fields['title'].widget.attrs['autofocus'] = ''

    def save(self, commit=True):
        instance = super().save(commit=False)
        current_month = timezone.datetime(year=instance.date.year,
                                          month=instance.date.month,
                                          day=1)
        instance.user = self.request.user
        budget = Budget.objects.get_or_create(date=current_month, user=instance.user)[0]
        instance.budget = budget

        if commit:
            instance.save()
        return instance


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ['income', 'savings']

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def save(self, commit=True):
        print('saving budget')
        instance = super().save(commit=False)
        if not instance.date:
            instance.date = date(year=timezone.now().year,
                                 month=timezone.now().month,
                                 day=1)
        if not instance.user:
            instance.user = self.request.user

        expenses = 0
        if instance.activities.all().filter(type='expense')\
                .aggregate(Sum('amount'))\
                .get('amount__sum'):
            expenses = instance.activities.all().filter(type='expense')\
                .aggregate(Sum('amount'))\
                .get('amount__sum')

        income = 0
        if instance.activities.all().filter(type='income')\
                .aggregate(Sum('amount'))\
                .get('amount__sum'):
            income = instance.activities.all().filter(type='income')\
                .aggregate(Sum('amount'))\
                .get('amount__sum')

        instance.balance = (instance.income -
                            instance.savings -
                            expenses + income)
        if commit:
            instance.save()
        return instance
