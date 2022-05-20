from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from blog.models import Article
from . import mixins


class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        
        else:
            return Article.objects.filter(author=self.request.user)
        

class ArticleCreate(LoginRequiredMixin,mixins.FormValidMixin, mixins.FieldsMixin, CreateView):
    model = Article
    fields = ["author", "title", "slug", "category", "description", "img", "publish", "status"]
    template_name = "registration/article-create-update.html"


class ArticleUpdate(mixins.AuthorAccessMixin, mixins.FormValidMixin, mixins.FieldsMixin, UpdateView):
    model = Article
    fields = ["author", "title", "slug", "category", "description", "img", "publish", "status"]
    template_name = "registration/article-create-update.html"


class ArticleDelete(mixins.SuperUserAccessMixin, DeleteView):
    model = Article
    success_url= reverse_lazy('account:home')
    template_name = "registration/article_confirm_delete.html"