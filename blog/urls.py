from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.userLogin,name='userLogin'),
    path('register/',views.userRegister,name='userRegister'),
    path('logout',views.userLogout,name='userLogout'),
    path('dashboard/',views.dashboard,name='userDashboard'),
    path('addpost/',views.addPost,name='addPost'),
    path('editpost/<int:id>',views.editPost,name='editPost'),
    path('deletepost/<int:id>',views.deletePost,name='deletePost'),
    ]