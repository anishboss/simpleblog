from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Post

from .forms import RegisterForm,LoginForm,PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'blog/index.html',context)

def userLogin(request):
    if request.method=="POST":
            fm = LoginForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return redirect('/')
    else:
        fm = LoginForm()
    context = {'form':fm}
    return render(request,'blog/login.html',context)

def userRegister(request):

    if request.method =="POST":
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            messages.success(request,"Account Created Sucessfully")
            user = fm.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)          
    else:
        fm = RegisterForm()
    return render(request,'blog/register.html',{'form':fm})

def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return redirect('/')

def addPost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                description = fm.cleaned_data['description']
                pt = Post(title=title,description=description)
                pt.save()
                messages.success(request,"Post added Sucessfully")
                fm= PostForm()
        else:
            fm = PostForm()
        return render(request,'blog/addpost.html',{'form':fm})
    else:
        return redirect('/login/')

def editPost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            post = Post.objects.get(pk=id)
            form = PostForm(instance=post,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect("/dashboard/")
        else:
            post = Post.objects.get(pk=id)
            form = PostForm(instance=post)
        return render(request,'blog/editpost.html',{'form':form})
    else:
        return redirect('/login/')

def deletePost(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=id)
        post.delete()
        return redirect('/dashboard/')
    else:
        return redirect('/login/')


