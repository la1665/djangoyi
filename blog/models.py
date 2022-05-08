from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html
from django.utils import timezone

from extensions.utils import jalali_converter

# my managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

# Models
class Article(models.Model):

    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
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
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس")

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
    objects = models.Manager()
    published_objects = ArticleManager()



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
