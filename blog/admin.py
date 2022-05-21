from django.contrib import admin
from .models import Category, BlogPost, Author, Tag, Comment


admin.site.register(BlogPost)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
