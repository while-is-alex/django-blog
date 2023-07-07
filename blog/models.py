from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Post(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=400)
    content = models.TextField(validators=[MinLengthValidator(10)])
    date = models.DateField(auto_now=True)
    image = models.ImageField(
        upload_to='images',
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='posts',
    )
    slug = models.SlugField(
        unique=True,
        default='',
        blank=True,
        # db_index=True, can be omitted, as it's set to True by default
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-details-page', args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return f'{self.name}, {self.email}'
