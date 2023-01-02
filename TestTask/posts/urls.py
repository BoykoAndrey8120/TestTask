from django.urls import path
from . import views
# from .views import PostDetaile

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('newpost', views.newpost, name='newpost')
    # path('users', views.users, name="users")
]