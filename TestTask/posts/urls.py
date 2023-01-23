from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('', views.PostsListView.as_view(), name='home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('post/edit/<int:pk>', views.PostUpdateView.as_view(), name='edit'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('newpost', views.Newpost.as_view(), name='newpost'),
    path('addcomment/<slug:slug>/<int:pk>', views.CommentsDetailView.as_view(), name='addcomment_pk'),

]