from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse
from django.views.generic.edit import FormMixin

from .models import Posts, Profile, Comments
from .forms import PostForms, CommentForm
from django.views.generic import DetailView, ListView, View


class PostsListView(ListView):
    model = Posts
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = 'comments'
    #     return context
class PostDetailView(DetailView):
    model = Posts
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        # slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Posts, pk=pk)
        comments = post.comments.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Posts.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


# def home(request, pk=None):
#     all_posts = Posts.objects.all()
#     all_comments = Comments.objects.all()
#     print(all_posts)
#     context = {'post': all_posts, 'comments': all_comments }
#
#     return render(request, 'posts/home.html', context)



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(username)

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username):
                messages.info(request, 'Name taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Wrong password')
            return redirect('signup')
    else:
        return render(request, 'posts/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user != None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')
    else:
        return render(request, 'posts/signin.html')




def newpost(request, pk=None):
    print(request.method)
    if request.method == "GET":
        return render(request, 'posts/newpost.html')
    if request.method == "POST":
        form = PostForms(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save()
            return redirect('/')
        else:
            print("error")


class CommentsView(ListView):
    model = Comments
    template_name = 'posts/addcomment.html'
    context_object_name = 'comment'


class CommentsDetailView(DetailView):
    model = Comments
    template_name = 'posts/addcomment_pk.html'
    context_object_name = 'com'


    # def form_valid(self, form):
    #     post = self.get_object()
    #     myform = form.save(commit=False)
    #     myform.post = post
    #     form.save()
    #     return super(Posts, self).form_valid(form)

    # def addcomment(request, pk=None):
    # if request.method == 'GET':
    #     return render(request, 'posts/addcomment.html')
    # elif request.method == 'POST':  # /newcomment
    #     form = CommentForm(request.POST)
    #     form.instance.post_id = self.kwargs.get("post_id")
    #     id_post = Posts.pk
    #     print('!!!!!!!!!!!!!!!!')
    #     print(id_post)
    #     # if request.user.is_authenticated != True:
    #     #     print("Not authenticated")
    #     #     return (request, '/')
    #     # else:
    #     #     print(form)
    #     #     (request, '/')
    #     if form.is_valid():
    #
    #         comment = form.save(commit=False)
    #         comment.save()
    #         form.save()
    #         print('!!!!!!!!!!!!!!!!')
    #         print(id_post)
    #         return redirect('/')
    #     else:
    #         print("error")
    #         print('!!!!!!!!!!!!!!!!')
    #         print(id_post)
    #         return redirect('/')
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
