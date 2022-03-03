from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CreateUserForm
from . helpers import prepareMessageFor
# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Loggedin Successfully !")
            return redirect('menu')
        else:
            messages.warning(request, "Incorrect Username or Password!")
    return render(request, "user/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect('menu')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_full_name = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            user_email = form.cleaned_data.get('email')
            welcome_message = prepareMessageFor(user_full_name)

            try:
                messages.success(request, f"{username} registered sucessfully")
                send_mail(
                'Welcome To Food Ordering System',
                welcome_message,
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
                )
            except:
                messages.info(request, f"{username} registered sucessfully email send fail.")
            return redirect('login')
        else:
            messages.warning(request, f"Please Enter all fields correctly")

    context = {
        'form': form
    }
    return render(request, "user/register.html", context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "User Loggedout!")
    return redirect('login')
    
