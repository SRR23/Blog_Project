from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm, ProfilePictureUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .decorator import not_logged_in_required
from django.contrib.auth.decorators import login_required
from .models import User
# Create your views here.

@never_cache
@not_logged_in_required
def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registration sucessful, Please login")
            return redirect('login')

    context = {
        "form": form
    }
    return render(request, 'registration.html', context)


@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Sorry, You haven't registered yet")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)

@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('profile')


def view_user_information(request, username):
    account = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect("profile")

    context = {
        "account": account,
    }
    return render(request, "user_information.html", context)
