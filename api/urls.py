from django.urls import path
from api.views import create_checks, get_check, get_new_cheks

urlpatterns = [
    path('create_checks/', create_checks, name='create_checks'),
    path('new_checks/', get_new_cheks, name='new_checks'),
    path('check/', get_check, name='check'),

]
