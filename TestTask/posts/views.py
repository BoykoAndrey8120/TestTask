from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse
from .models import Posts, Profile
from .forms import PostForms


def home(request):
    all_posts = Posts.objects.all()
    print(all_posts)
    context = {'post': all_posts }

    return render(request, 'posts/home.html', context)



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



def newpost(request):
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











