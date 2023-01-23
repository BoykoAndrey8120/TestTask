from django.forms import ModelForm
from .models import Posts, Comments


class PostForms(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image', 'content']


def handler_view(request):
    form = PostForms(request.POST, request.FILES)
    if form.is_valid():
        form.save()


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

        def handler_view(request):
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()

