from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crisco.models import Bookmark


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
    for _ in range(100):
        bookmark = Bookmark(title='bookmark{}'.format(count),
                            comment='Comment{}'.format(count),
                            longurl=fake.url(),
                            modified=fake.date_time_this_year(),
                            user=random.choice(User.objects.all()))
        bookmark.generate_short()
        bookmark.save()
        count += 1

class Command(BaseCommand):
    def handle(self, *args, **options):
        generate_users()
