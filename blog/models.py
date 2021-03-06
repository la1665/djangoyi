from ipaddress import ip_address
from account.models import User
from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment

from extensions.utils import jalali_converter

# my managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

# Models
class IP(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی-پی")


class Article(models.Model):

    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت خورده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=128, verbose_name="عنوان")
    category = models.ManyToManyField(
        'Category', verbose_name="دسته بندی", related_name="articles")
    description = models.TextField(verbose_name="توضیحات")
    img = models.ImageField(upload_to="Images", verbose_name="عکس")
    publish = models.DateTimeField(
        default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IP, through='ArticleHit', blank=True, related_name="hits", verbose_name="بازدید ها")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width='60' height='60' style='border-radius: 5px;' src='{}'>".format(self.img.url))
    thumbnail_tag.short_description = "عکس"
    
    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"

    def get_absolute_url(self):
        return reverse("account:home")


    objects = models.Manager()
    published_objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IP, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    position = models.IntegerField(verbose_name="موقعیت")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()
