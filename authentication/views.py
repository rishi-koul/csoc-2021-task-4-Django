from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User


def loginView(request):
    template_name = 'authentication/login.html'

    if (request.method == 'POST') :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if (user is not None) :
            login(request, user)
            return redirect('/')
        messages.info(request, "User doesnt exist")

    return render(request, template_name)

def registerView(request):
    template_name = 'authentication/register.html'
    if (request.method == 'POST') :
        username = request.POST.get('username')
        password = request.POST.get('password')

        if (User.objects.filter(username=username).exists()) :
            messages.info(request, "Already registered")
            return render(request, template_name)

        user = User.objects.create_user(
            username=username, password=password, first_name=username, last_name="", email="")
        user.save()
        loggedIn = authenticate(username = username, password = password)
        login(request, loggedIn)
        return redirect('/')

    return render(request, template_name)

def logoutView(request):
    logout(request)
    return redirect('/')