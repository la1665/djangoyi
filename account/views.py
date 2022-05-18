from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from blog.models import Article


class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        
        else:
            return Article.objects.filter(author=self.request.user)
        