import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from blog.models import Article, Category, User

print(f"Users: {User.objects.count()}")
for u in User.objects.all():
    print(f" - {u.username} ({u.email})")

print(f"Categories: {Category.objects.count()}")
print(f"Articles: {Article.objects.count()}")
for a in Article.objects.all():
    print(f" - {a.title} (Published: {a.is_published})")
