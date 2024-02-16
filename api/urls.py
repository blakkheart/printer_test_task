from django.urls import path
from api.views import simple_view, get_all_checks

urlpatterns = [
    path('create_checks/', simple_view),
    path('checks/', get_all_checks),
]
