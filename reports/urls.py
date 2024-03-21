from django.urls import path
from . import views

urlpatterns = [
    path('report/<int:id>/', views.reports, name='reports')
]