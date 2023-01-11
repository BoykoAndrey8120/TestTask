from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('', views.PostsListView.as_view(), name='home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('newpost', views.newpost, name='newpost'),
    # path('addcomment', views.addcomment),
    # path('addcomment', views.addcomment, name='addcomment'),
    path('addcomment/<slug:slug>/<int:pk>', views.CommentsDetailView.as_view(), name='addcomment_pk'),
    path('addcomment', views.CommentsView.as_view(), name='addcomment'),

    # path('users', views.users, name="users")
]