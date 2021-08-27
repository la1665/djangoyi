from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.home, name='home'),
    path('page/<int:page>', views.home, name='home'),
    path('article/<slug:slug>/', views.detail, name="detail"),
    path('category/<slug:slug>/', views.category, name="category"),
    path('category/<slug:slug>/page/<int:page>/',
         views.category, name="category"),
    path('api/', views.api, name='api'),
]
