from django.contrib.auth import views
from django.urls import path
from . import views as v

app_name = 'account'

urlpatterns = [
    path('', v.ArticleList.as_view(), name='home'),
    path('article/create', v.ArticleCreate.as_view(), name='article-create'),
    path('article/update/<int:pk>', v.ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', v.ArticleDelete.as_view(), name='article-delete'),
    path('profile/', v.Profile.as_view(), name='profile'),

]