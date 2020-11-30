from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Budget, Activity
from .forms import BudgetForm, ActivityForm


# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect('activity:home')
    return render(request, 'activity/index.html')


@login_required()
def home(request):
    user = request.user
    current_month = timezone.datetime(year=timezone.now().year,
                                      month=timezone.now().month,
                                      day=1)

    budget = Budget.objects.get_or_create(date=current_month, user=user)[0]
    records = budget.activities.all().order_by('-date')
    form = ActivityForm(request)

    if request.method == 'POST':
        form = ActivityForm(request, request.POST)

        if form.is_valid():
            form.save()

            return redirect('activity:home')

    return render(request,
                  'activity/home.html',
                  {
                      'budget': budget,
                      'form': form,
                      'records': records,
                  })


@login_required()
def delete(request, id_num):
    # if request.method == 'POST':
    account_user = request.user
    Activity.objects.get(user=account_user, pk=id_num).delete()
    return redirect('activity:home')


@login_required()
def update_budget(request, id_num):
    budget = Budget.objects.get(pk=id_num)
    form = BudgetForm(instance=budget)

    if request.method == 'POST':
        form = BudgetForm(request, request.POST, instance=budget)
        if form.is_valid():
            form.save()
        return redirect('activity:home')

    return render(request, 'activity/update_budget.html', {'form': form})
