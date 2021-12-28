from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search_result'),
    path('generate_sheet/', views.generate_sheet, name='generate_sheet'),
]
