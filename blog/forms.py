from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = [
        #     'name',
        #     'email',
        #     'text',
        # ]
        exclude = ['post']
        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'text': 'Your comment'
        }