from django.contrib import admin

from .models import Article, Category, IP

def article_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
article_published.short_description = 'انتشار مقالات انتخاب شده'

def article_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "پیش نویس شد."
    else:
        message_bit = "پیش نویس شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
article_draft.short_description = 'پیش نویس مقالات انتخاب شده'

def category_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
category_published.short_description = 'انتشار دسته بندی های انتخاب شده'

def category_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = "پیش نویس شد."
    else:
        message_bit = "پیش نویس شدند."
    modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
category_draft.short_description = 'پیش نویس دسته بندی های انتخاب شده'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_tag', 'slug','author', 'jpublish', 'status', 'is_special', 'category_to_str')
    list_display_links = ('title',)
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    actions = [article_published, article_draft]


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_display_links = ('title',)
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = [category_published, category_draft]


admin.site.register(Category, CategoryAdmin)

admin.site.register(IP)
