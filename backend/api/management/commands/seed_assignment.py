"""
Seed minimal conforme au cahier des charges du projet final Django.

Crée :
- 2 utilisateurs (alice, bob)
- 2 articles avec tags
- 2 commentaires par article (avec tags)

Idempotent : peut être relancé sans dupliquer.
"""
from django.core.management.base import BaseCommand
from api.models import User, Article, Comment, Tag, Category


# Données de seed conformes à la spec : 2 users, 2 articles, 2 comments/article
USERS = [
    {"username": "alice", "email": "alice@example.com", "password": "alicepass123"},
    {"username": "bob", "email": "bob@example.com", "password": "bobpass123"},
]

ARTICLES = [
    {
        "title": "Découvrir Django REST Framework",
        "content": (
            "Django REST Framework est une boîte à outils puissante pour construire "
            "des APIs Web. Cet article présente les concepts clés : sérializers, "
            "viewsets, routers et permissions."
        ),
        "author_username": "alice",
        "tags": ["python", "django", "api"],
    },
    {
        "title": "Pourquoi adopter PostgreSQL en production",
        "content": (
            "PostgreSQL offre une fiabilité, des performances et des fonctionnalités "
            "avancées (JSONB, full-text search, transactions) qui en font un choix "
            "idéal pour les applications Django sérieuses."
        ),
        "author_username": "bob",
        "tags": ["postgresql", "base-de-donnees", "production"],
    },
]

COMMENTS = {
    "Découvrir Django REST Framework": [
        {"author": "bob", "content": "Excellent rappel sur les viewsets, merci !", "tags": ["python", "feedback"]},
        {"author": "alice", "content": "Je rajouterai un mot sur les Throttles dans une v2.", "tags": ["api"]},
    ],
    "Pourquoi adopter PostgreSQL en production": [
        {"author": "alice", "content": "Le full-text search PostgreSQL est sous-estimé.", "tags": ["postgresql", "search"]},
        {"author": "bob", "content": "À combiner avec pgbouncer pour les charges élevées.", "tags": ["production"]},
    ],
}


class Command(BaseCommand):
    help = "Seed minimal conforme au cahier des charges (2 users, 2 articles, 2 comments/article)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding assignment data..."))

        # Catégorie par défaut (optionnelle, l'article peut s'en passer)
        default_cat, _ = Category.objects.get_or_create(name="Général")

        # 1. Utilisateurs
        users = {}
        for u in USERS:
            user, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            if created or not user.has_usable_password():
                user.set_password(u["password"])
                user.save()
                self.stdout.write(f"  + user créé : {user.username}")
            else:
                self.stdout.write(f"  = user existant : {user.username}")
            users[u["username"]] = user

        # 2. Articles avec tags
        articles_by_title = {}
        for a in ARTICLES:
            article, created = Article.objects.get_or_create(
                title=a["title"],
                defaults={
                    "author": users[a["author_username"]],
                    "category": default_cat,
                    "content": a["content"],
                },
            )
            # Tags : list comprehension pour récupérer/créer en lot
            tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in a["tags"]]
            article.tags.set(tag_objs)
            articles_by_title[a["title"]] = article
            verb = "créé" if created else "existant"
            self.stdout.write(f"  + article {verb} : {article.title} (tags: {a['tags']})")

        # 3. Commentaires avec tags (2 par article)
        for title, comments in COMMENTS.items():
            article = articles_by_title[title]
            for c in comments:
                comment, created = Comment.objects.get_or_create(
                    article=article,
                    author=users[c["author"]],
                    content=c["content"],
                )
                tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in c["tags"]]
                comment.tags.set(tag_objs)
                if created:
                    self.stdout.write(f"    > comment de {c['author']} sur '{title[:30]}...' (tags: {c['tags']})")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nOK : {User.objects.count()} users, "
                f"{Article.objects.count()} articles, "
                f"{Comment.objects.count()} comments, "
                f"{Tag.objects.count()} tags."
            )
        )
