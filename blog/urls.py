from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.home, name='home_page'),
    path('article/<slug:slug>/', views.detail, name="detail"),
    path('api/', views.api, name='api'),
]
