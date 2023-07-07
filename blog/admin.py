from django.contrib import admin
from .models import Post, Author, Tag, Comment

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
    )


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': (
            'title',
        ),
    }
    list_filter = (
        'author',
        'tags',
        'date',
    )
    list_display = (
        'title',
        'author',
        'date',
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'post',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
