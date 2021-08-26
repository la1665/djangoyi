from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404

from .models import *
# Create your views here.


def home(request):
    context = {
        "articles": Article.objects.all().filter(status='p').order_by('-publish'),
        "category": Category.objects.all().filter(status=True)
    }
    return render(request, "blog/home.html", context)


def detail(request, slug):
    context = {
        "article": get_object_or_404(Article, slug=slug, status='p')
    }
    return render(request, "blog/detail.html", context)


def api(request):
    data = {
        "1": {
            "title": "first",
            "id": 20,
            "slug": "first_article"},

        "2": {
            "title": "second",
            "id": 30,
            "slug": "second_article"},

        "3": {
            "title": "third",
            "id": 40,
            "slug": "third_article"}

    }
    return JsonResponse(data=data)
