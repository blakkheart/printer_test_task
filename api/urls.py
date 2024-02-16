from django.urls import path
from api.views import simple_view

urlpatterns = [
    path('', simple_view),
]
