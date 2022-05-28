from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .models import User
from .forms import ProfileForm, SignupForm
from . import mixins
from .tokens import account_activation_token
from blog.models import Article


class ArticleList(mixins.AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        
        else:
            return Article.objects.filter(author=self.request.user)
        

class ArticleCreate(mixins.AuthorsAccessMixin, mixins.FormValidMixin, mixins.FieldsMixin, CreateView):
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


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")



class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت.'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_b64encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد.<a href="/login">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('اکانت شما با موفقیت فعال شد.<a href="/login">ورود</a>')
    else:
        return HttpResponse('لینک منقضی شده است.دوباره امتحان کنید.<a href="/register">امتحان دوباره</a>')
        