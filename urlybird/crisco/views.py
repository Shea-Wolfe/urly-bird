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
    return render(request, 'crisco/register.html', {'form':form})

    def start(request):
        if user.is_authenticated():
            redirect('home', request.user.pk)
        else:
            redirect('all')

class AllBookmarks(ListView):
    '''Generic ListView that will show the 20 most recent bookmarks.
    Incorperates pagination for viewing older bookmarks.'''
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/newbookmarks.html'

    def get_queryset(self):
        preload = Bookmark.objects.all().select_related('user')
        return preload.order_by('-modified')

class UserPage(ListView):
    '''Generic ListView that will show the 20 most recent bookmarks a user posted.'''
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/userpage.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        self.user.bookmark_set.all().order_by('-modified')


class HomePage(ListView):
    '''Generic ListView that will show the 20 most recent bookmarks a user posted.
       Seperated from UserPage to allow for edit/delete with minimal processing.'''
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/homepage.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        self.user.bookmark_set.all().order_by('-modified')
