from rest_framework import serializers
from .models import BlogPost


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'summary', 'content', 'published',
                  'imgURL', 'author', 'category', 'slug', 'image')
