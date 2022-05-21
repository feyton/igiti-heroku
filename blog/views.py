from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import BlogPost

# Create your views here.


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = BlogPost.objects.filter(published=True)
