from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('posts', views.PostsView.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.PostDetailsView.as_view(), name='post-details-page'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later')
]