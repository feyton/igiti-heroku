from autoslug import AutoSlugField
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forestry:category', kwargs={'pk': self.id})


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facebook = models.CharField(
        _('author facebook'), max_length=255, blank=True)
    twitter = models.CharField(_('author twitter'), max_length=255, blank=True)
    telephone = models.CharField(_('telephone'), max_length=13, blank=True)
    image = CloudinaryField(blank=True, null=True)
    bio = models.TextField(_('author biography'), blank=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        return str(full_name)

    def get_author_name(self):
        return self.user.first_name

    # def get_absolute_url(self):
    #     return reverse('author:detail', kwargs={'user': self.user.id})


class BlogPostQueryset(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def draft(self):
        return self.filter(published=False)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)
    image = CloudinaryField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    content = models.TextField(_('text'))
    published = models.BooleanField(_('published'), default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    pub_date = models.DateTimeField(_('publish date'), blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, blank=True, null=True, default=1, related_name='posts')

    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    objects = BlogPostQueryset.as_manager()

    class Meta:
        # This class help to specify the plural and structure in admin section
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['-pub_date']

    @property
    def imgURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def save(self, *args, **kwargs):
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()
        elif not self.published and self.pub_date is not None:
            self.pub_date = None
        if not self.summary and self.description:
            self.summary = self.description[:60]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('forestry:detail', kwargs={'slug': self.slug})

    def get_author(self):
        if self.author:
            return self.author.get_author_name()

    def get_bio(self):
        if self.author and self.author.bio:
            if len(self.author.bio) > 200:
                return '%s...' % self.author.bio
            return self.author.bio

    def get_author_image(self):
        if self.author.image:
            return self.author.image.url


class Comment(models.Model):
    full_name = models.CharField(_("full name"), max_length=255)
    email = models.EmailField(_('Email'), max_length=255)
    message = models.TextField(_("Comment"))
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["approved", "-created_on"]

    def __str__(self):
        return self.full_name
