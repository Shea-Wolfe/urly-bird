from django.forms import ModelForm
# from django.contrib.auth.models import User

from .models import Bookmark

# Create the form class.


class BookmarkForm(ModelForm):

    class Meta:
        model = Bookmark
        fields = ('title', 'longurl', 'comment')

class EditBookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title','comment')
