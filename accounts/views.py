from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, ': That username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, ': That email is already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(
                        request, ': You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, ': Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, ': Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('register')


class Change_Password(TemplateView):
    template_name = "accounts/password_change.html"

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)
            messages.success(request, "Password Changed Successfully")
            return redirect("/")
        else:
            for err in form.errors.values():
                messages.error(request, err)
            return redirect("/change_password")


    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {"form": form})
