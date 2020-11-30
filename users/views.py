from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

from activity.decorators import anonymous_required


# Create your views here.
@anonymous_required
def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user = authenticate(username= form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)

            messages.success(request, f'Welcome, {user.get_short_name()}')
            return redirect('activity:index')

    return render(request, 'registration/register.html', {
        'form': form
    })