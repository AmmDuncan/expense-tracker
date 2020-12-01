from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from .utils import get_prev_month_budget_balance
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
    page_num = request.GET.get('page')
    prev_balance = get_prev_month_budget_balance(current_month, user)
    budget = Budget.objects.get_or_create(date=current_month, user=user,
                                          balance=prev_balance)[0]
    records = budget.activities.all().order_by('-date')
    paginator = Paginator(records, 10)

    try:
        records = paginator.page(page_num)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

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
                      'paginator': paginator,
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
