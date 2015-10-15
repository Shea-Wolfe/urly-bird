from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from .models import Bookmark

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

class all_bookmarks(ListView):
    '''Generic ListView that will show the 20 most recent bookmarks.
    Incorperates pagination for viewing older bookmarks.'''
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/newbookmarks.html'

    def get_queryset(self):
        return Bookmark.objects.all().order_by('-timestamp')

class user_page(ListView):
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/'
    
    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.user.bookmark_set.all()
