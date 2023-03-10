from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Posts, Profile, Comments
from .forms import PostForms, CommentForm
from django.views.generic import DetailView, ListView, UpdateView, View, CreateView


class PostsListView(ListView):
    model = Posts
    template_name = 'posts/home.html'
    context_object_name = 'posts'


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
        user = request.user

        comments = post.comments.all()
        print(comments)

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            print('!!!!!!!!!!!!!!')
            # post = form.cleaned_data['post']
            owner = user
            content = form.cleaned_data['content']

            comment = Comments.objects.create(
                content=content, owner=owner, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class PostUpdateView(UpdateView):
    model = Posts
    fields = [
        'title', 'content', 'image'
    ]
    template_name = 'posts/edit.html'
    context_object_name = 'post'
    success_url = '/'


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


class Newpost(View):
    model = Posts
    template_name = 'posts/newpost.html'
    context_object_name = 'post'
    fields = ['title', 'image', 'content']

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'form': PostForms(), 'user': user}
        return render(request, self.template_name, context)
    #
    def post(self, request, *args, **kwargs):
        user = request.user
        form = PostForms(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            form.save()
            return redirect('/')
        else:
            print("error")


class CommentsDetailView(DetailView):
    model = Comments
    template_name = 'posts/addcomment_pk.html'
    context_object_name = 'com'



