from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering            = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name       = models.CharField(max_length=50, unique=True)
    slug       = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):

    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('published', 'Published'),
    ]

    author   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='blogs'
    )
    tags     = models.ManyToManyField(Tag, blank=True, related_name='blogs')

    title     = models.CharField(max_length=255)
    slug      = models.SlugField(unique=True, blank=True, max_length=300)
    content   = models.TextField()
    excerpt   = models.CharField(max_length=160, blank=True, default='')
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views     = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Auto generate slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug      = base_slug
            counter   = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug    = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        # Auto generate excerpt
        if not self.excerpt and self.content:
            self.excerpt = self.content[:157] + '...' if len(self.content) > 157 else self.content

        # Auto calculate read time
        word_count    = len(self.content.split())
        self.read_time = max(1, word_count // 200)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title