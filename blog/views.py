from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm
from .models import Post


class HomeView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class PostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'
    ordering = ['-date']


class PostDetailsView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        return render(
            request,
            'blog/post-details.html',
            {
                'post': post,
                'tags': post.tags.all(),
                'form': CommentForm(),
                'comments': post.comments.all().order_by('-id'),
                'saved': self.is_stored_post(request, post.id),
            }
        )

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if form.is_valid():
            # commit=False doesn't hit the database, but only creates a new comment, so we can modify it before saving
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(
                reverse(
                    'post-details-page',
                    args=[slug],
                )
            )

        return render(
            request,
            'blog/post-details.html',
            {
                'post': post,
                'tags': post.tags.all(),
                'form': form,
                'comments': post.comments.all().order_by('-id'),
                'saved': self.is_stored_post(request, post.id),
            }
        )


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None or len(stored_posts) == 0:
            posts = []
            has_posts = False
        else:
            # __in modifier checks for all posts that match the ids in stored_posts
            posts = Post.objects.filter(id__in=stored_posts)
            has_posts = True

        return render(
            request,
            'blog/stored-posts.html',
            {
                'read_later': posts,
                'has_posts': has_posts,
            }
        )

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        # if there aren't any previous stored_posts, the list is created
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST['post_id'])

        # if the current post_id is not already in stored_posts, it's added to that list
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        post = Post.objects.get(id=post_id)

        return HttpResponseRedirect(f'/posts/{post.slug}')
