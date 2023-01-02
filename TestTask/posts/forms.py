from django import forms
from django.forms import ModelForm
from .models import Posts

# class PostForms(forms.Form):
#     title = forms.CharField(max_length=100)
#     image = forms.ImageField(upload_to='images', default=None)
#     content = forms.TextField(blank=True)


class PostForms(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image', 'content']


def handler_view(request):
    form = PostForms(request.POST, request.FILES)
    if form.is_valid():
        form.save()
