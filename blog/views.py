from email import contentmanager
from multiprocessing import context
from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from .models import Article, Category


# def home(request, page=1):
#     articles_list = Article.published_objects.published().order_by('-publish')
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)

#     context = {
#         "articles": articles, }

#     return render(request, "blog/home.html", context)

class ArticleList(ListView):
    queryset = Article.published_objects.published()
    template_name = "blog/home.html"
    context_object_name = "articles"
    paginate_by = 2


# def detail(request, slug):
#     context = {
#         "article": get_object_or_404(Article.published_objects.published(), slug=slug),
#     }
#     return render(request, "blog/detail.html", context)

class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.published_objects.published(), slug=slug)
    template_name = "blog/detail.html"


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = Article.published_objects.published().filter(category=category)
#     paginator = Paginator(articles_list, 3)
#     articles = paginator.get_page(page)
#     context = {
#         "category": category,
#         "articles": articles,
#     }
#     return render(request, "blog/category.html", context)

class CategoryList(ListView):
    paginate_by = 3
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