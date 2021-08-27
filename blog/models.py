from enum import auto
from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from extensions.utils import jalali_converter

# my managers


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

# Create your models here.


class Article(models.Model):

    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شده'),
    )

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
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)

    def category_published(self):
        return self.category.filter(status=True)

    objects = ArticleManager()

    jpublish.short_description = "زمان انتشار"


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="وضعیت نمایش")
    position = models.IntegerField(verbose_name="موقعیت")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title
