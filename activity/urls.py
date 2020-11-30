from django.urls import path
from .views import index, home, delete, update_budget

app_name = 'activity'

urlpatterns = [
    path('delete/<int:id_num>', delete, name='delete'),
    path('update/budget/<int:id_num>', update_budget, name='update-name'),
    path('home/', home, name='home'),
    path('', index, name='index'),
]