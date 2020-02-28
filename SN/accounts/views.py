# from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
    
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError, HttpResponseNotAllowed

from .models import Profile
from .forms import ProfileForm

from django.db.models import Q

# pages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home_view(request):
    return render(request, 'home.html')
    

def login_view(request):
    Next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if Next:
            return redirect(Next)
        return redirect("/")
    return render(request, "form.html", {"form":form, "title": title})

def register_view(request): 
    # print(request.user.is_authenticated)
    Next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        # TODO check
        user.email = form.cleaned_data.get('email')
        print(f'user {user.username} email is {user.email}')
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if Next:
            return redirect(Next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

from django.contrib.sites.shortcuts import get_current_site

@login_required
def profile_view(request, slug):
    # print(f'\n\nALLOWED_HOSTS:{settings.ALLOWED_HOSTS}')
    profile = request.user.profile if request.user.profile.slug == slug \
        else get_object_or_404(Profile, slug=slug)

    context = {
        "profile": profile,
        "user": request.user,
    }
    return render(request, 'profile.html', context)

@login_required
def profile_delete(request, slug):
    if request.user.profile.slug == slug:
        username = request.user.username
        logout(request)
        user = User.objects.get(username=username)
        # TODO add html to confirm deletion
        return redirect('/') # what about logout ?????
    return HttpResponseNotAllowed
        

@login_required
def profile_update(request, slug):
    if request.user.profile.slug == slug:
        instance = Profile.objects.get(slug=slug)
        form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url)

        context = {
            "form": form,
            "theme": "Update profile",
        }

        return render(request, "profile_form.html", context)
    else:
        return HttpResponseNotAllowed

@login_required
def profile_list(request):
    queryset_list = Profile.objects.all()

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(user__username__icontains=query)#|
            # Q(content__icontains=query)|
            # Q(sender__user__first_name__icontains=query)|
            # Q(sender__user__last_name__icontains=query)|
            # Q(sender__user__username__icontains=query)|
            # Q(sender__email__icontains=query)
        ).distinct()


    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    is_paged = paginator.num_pages > 1

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "profile_list": queryset, 
        # "type": 'chat_list',
        "base_template": 'base.html',
        "page_request_var": page_request_var,
        "is_paginated": is_paged,
    }
    return render(request, "profile_list.html", context)