from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from datetime import datetime, timedelta

from account.models import User
from .models import Article, Category, ArticleHit
from account.mixins import AuthorAccessMixin


class ArticleList(ListView):
    queryset = Article.published_objects.published()
    template_name = "blog/home.html"
    context_object_name = "articles"
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_month = datetime.today() - timedelta(days=30)
        context['popular_articles'] = Article.published_objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))
            ).order_by('-count', '-publish')[:5]
        return context



class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article =  get_object_or_404(Article.published_objects.published(), slug=slug)
        
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article
    template_name = "blog/detail.html"


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)
    template_name = "blog/detail.html"


class CategoryList(ListView):
    paginate_by = 4
    template_name = "blog/category.html"
    context_object_name = "articles"

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return Article.published_objects.published().filter(category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 2
    template_name = "blog/author_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return Article.published_objects.published().filter(author=author)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context