from django.urls import path, include

from budget.views import TestView


app_name='budget'
urlpatterns=[
        path('',TestView.as_view(), name='test'),
    ]