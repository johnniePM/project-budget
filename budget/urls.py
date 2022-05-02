from django.urls import path, include

from budget.views import EditInkomstView, IdagsView, IdagsnyainkomstenVIew, IdagsnyautgiftenVIew



app_name='budget'
urlpatterns=[
    path('', IdagsView.as_view(),name='idag-view'),
    path('ny-inkomst-idag/', IdagsnyainkomstenVIew.as_view(),name='idag-nya-in'),
    path('ny-utgift-idag/', IdagsnyautgiftenVIew.as_view(),name='idag-nya-ut'),
    path('ut/<pk>/edit', EditInkomstView.as_view(),name='edit-in-idag'),
    path('in/<pk>/edit', EditInkomstView.as_view(),name='edit-ut-idag'),
    ]