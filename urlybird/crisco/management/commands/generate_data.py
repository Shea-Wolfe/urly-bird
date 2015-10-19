from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crisco.models import Bookmark, Click


def generate_users():
    from faker import Faker
    fake = Faker()
    user_list = [x for x in {fake.user_name() for _ in range(9000)}]
    count = 0
    for _ in range(100):
        user = User.objects.create_user(user_list[count],password='password',email=fake.email())
        user.save()
        count += 1

def generate_bookmarks():
    from faker import Faker
    import random
    fake = Faker()
    count = 1
    for _ in range(300):
        bookmark = Bookmark(title='bookmark{}'.format(count),
                            comment='Comment{}'.format(count),
                            longurl=fake.url(),
                            modified=fake.date_time_this_year(),
                            user=random.choice(User.objects.all()))
        bookmark.generate_short()
        bookmark.save()
        count += 1

def generate_clicks():
    from faker import Faker
    import random
    fake = Faker()
    for _ in range(5000):
        click = Click(timestamp=fake.date_time_this_year(),clicker=random.choice([random.choice(User.objects.all()),random.choice(User.objects.all()),None]),bookmark=random.choice(Bookmark.objects.all()))
        click.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        generate_users()
        generate_bookmarks()
        generate_clicks()
