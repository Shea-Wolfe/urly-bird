from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,password=user.password)
            login(request,user)
            return redirect('home_page', request.user.pk)

    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})

    def start(request):
        if user.is_authenticated():
            redirect('home', request.user.pk)
        else:
            redirect('all')
