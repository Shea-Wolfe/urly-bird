from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, UpdateView
from .models import Bookmark, Click
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookmarkForm
from datetime import datetime

# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,
                                password=request.POST['password1'])
            login(request, user)
            return redirect('home_page', request.user.username)

    else:
        form = UserCreationForm()
    return render(request, 'crisco/register.html', {'form': form})


def start(request):
    if request.user.is_authenticated():
        return redirect('home_page', request.user.username)
    else:
        return redirect('recent')


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
        self.user = get_object_or_404(User, username=self.kwargs['pk'])
        return self.user.bookmark_set.all().order_by('-modified')


class HomePage(ListView):
    '''Generic ListView that will show the 20 most recent bookmarks a user posted.
       Seperated from UserPage to allow for edit/delete with minimal processing.'''
    paginate_by = 20
    context_object_name = 'bookmarks'
    template_name = 'crisco/homepage.html'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['pk'])
        return self.user.bookmark_set.all().order_by('-modified')


@login_required
def add_bookmark(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.generate_short()
            bookmark.modified = datetime.now()
            bookmark.save()
            return redirect('recent')
    else:
        form = BookmarkForm()
    return render(request, 'crisco/add_bookmark.html',
                  {'form': form})


@login_required
def delete_bookmark(request, bookmark_id):
    if Bookmark.objects.get(pk=bookmark_id).user == request.user:
        Bookmark.objects.get(pk=bookmark_id).delete()
        messages.add_message(request, messages.SUCCESS, "Bookmark deleted!")
        return redirect('home_page', pk=request.user.username)
    else:
        messages.add_message(
            request, messages.ERROR, "You can't delete what is not yours!")
        return redirect('recent')


@login_required
def edit_bookmark(request, bookmark_id):
    if Bookmark.objects.get(pk=bookmark_id).user == request.user:
        redirect('edit_form', pk=bookmark_id)
    else:
        messages.add_message(request, messages.WARNING,
                             "You can't edit what is not yours!")
        return redirect('recent')


class EditBookmark(UpdateView):
    model = Bookmark
    template_name_suffix = '_update_form'
    field = ['title', 'comment']
    success_url = "{% url 'home_page' request.user.username %}"

def new_click(request, short_url):
    bookmark = get_object_or_404(Bookmark, shorturl=short_url)
    try:
        user = request.user
    except:
        click = Click(bookmark=bookmark, timestamp=datetime.now())
    else:
        click = Click(bookmark=bookmark, clicker=user, timestamp=datetime.now())
    click.save()
    return redirect(bookmark.longurl)
