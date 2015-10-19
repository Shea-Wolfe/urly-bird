from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from .models import Bookmark, Click
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookmarkForm, EditBookmarkForm
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from django.db import models
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
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
            return redirect('home_page', pk=request.user.username)
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
        if request.method == 'POST':
            form = EditBookmarkForm(request.POST)
            if form.is_valid():
                bookmark = Bookmark.objects.get(pk=bookmark_id)
                bookmark.title = request.POST['title']
                bookmark.comment = request.POST['comment']
                bookmark.save()
                return redirect('home_page', pk=request.user.username)
        else:
            form = EditBookmarkForm()
        return render(request, 'crisco/edit_bookmark.html', {'form':form,'bookmark':bookmark_id})

        return redirect('edit_form', pk=bookmark_id)

    else:
        messages.add_message(request, messages.WARNING,
                             "You can't edit what is not yours!")
        return redirect('recent')


def new_click(request, short_url):
    bookmark = get_object_or_404(Bookmark, shorturl=short_url)
    try:
        click = Click(bookmark=bookmark, clicker=user, timestamp=datetime.now())
    except:
        click = Click(bookmark=bookmark, timestamp=datetime.now())
    click.save()
    return redirect(bookmark.longurl)

class BookmarkInfo(ListView):
    paginate_by = 20
    context_object_name = 'clicks'
    template_name = 'crisco/bookmarkinfo.html'

    def get_queryset(self):
        then = datetime.now() - timedelta(days=30)
        self.bookmark = get_object_or_404(Bookmark, shorturl=self.kwargs['pk'])
        self.clicks = Click.objects.filter(bookmark=self.bookmark, timestamp__gte=then)
        return self.clicks.order_by('timestamp')

@login_required
def pie_chart(request, short_url):
    then = datetime.now() - timedelta(days=30)
    bookmark = get_object_or_404(Bookmark, shorturl=short_url)
    anon_clicks = bookmark.click_set.filter(clicker=None).all().count()
    total_clicks = bookmark.click_set.all().count()
    try:
        anon_clicks = 100*(anon_clicks/total_clicks)
    except:
        messages.add_message(request, messages.ERROR, "No Clicks!")
        return redirect('home_page', pk=request.user.username)
    total_clicks = 100-anon_clicks
    f = plt.figure(1, figsize=(6,6))
    ax = plt.axes([0.1, 0.1, 0.8, 0.8])
    labels = 'Anon Clicks', 'User Clicks'
    fracs = [anon_clicks,total_clicks]
    explode=(0, 0.05)
    plt.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.title('Usage Data.', bbox={'facecolor':'0.8', 'pad':5})

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(f)
    return response

@login_required
def bar_chart(request, username):
    if request.user.username == username:
        then = datetime.now() - timedelta(days=30)
        user = get_object_or_404(User, username=username)
        bookmarks = user.bookmark_set.all()
        clicks = [bookmark.click_set.filter(timestamp__gte=then).count() for bookmark in bookmarks]
        bookmarks = [bookmark.title for bookmark in bookmarks]
        f = plt.figure(figsize=(10,8))
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.bar([x for x in range(len(bookmarks))],clicks)
        plt.title('Clicks by Bookmark This Month')
        plt.xticks([x for x in range(len(bookmarks))],bookmarks, rotation=60)
        canvas = FigureCanvasAgg(f)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        plt.close(f)
        return response
    else:
        messages.add_message(request, messages.ERROR, "Creator Only!")
        return redirect('recent')

@login_required
def all_time(request, username):
    if request.user.username == username:
        then = datetime.now() - timedelta(days=30)
        user = get_object_or_404(User, username=username)
        bookmarks = user.bookmark_set.all()
        clicks = [bookmark.click_set.all().count() for bookmark in bookmarks]
        bookmarks = [bookmark.title for bookmark in bookmarks]
        f = plt.figure(figsize=(10,8))
        plt.gcf().subplots_adjust(bottom=0.25)
        plt.bar([x for x in range(len(bookmarks))],clicks)
        plt.title('Clicks by Bookmark All Time')
        plt.xticks([x for x in range(len(bookmarks))],bookmarks, rotation=60)
        canvas = FigureCanvasAgg(f)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        plt.close(f)
        return response
    else:
        messages.add_message(request, messages.ERROR, "Creator Only!")
        return redirect('recent')
