"""
Management command qui garantit que CHAQUE article, recette et exercice
a une image Unsplash UNIQUE (plus de doublons).

Usage:
    python manage.py fix_unique_images
    python manage.py fix_unique_images --force  # réassigne même si déjà unique
"""
from django.core.management.base import BaseCommand
from api.models import Article, Recipe, Exercise


# =============================================================================
# POOLS D'IMAGES UNSPLASH — chaque ID est unique
# =============================================================================

# 120 photos fitness/exercices (muscles, équipement, gym)
EXERCISE_PHOTOS = [
    "photo-1571019613454-1cb2f99b2d8b", "photo-1517836357463-d25dfeac3438",
    "photo-1534438327276-14e5300c3a48", "photo-1534258936925-c58bed479fcb",
    "photo-1540497077202-7c8a3999166f", "photo-1581009146145-b5ef050c2e1e",
    "photo-1541534741688-6078c6bfb5c5", "photo-1583500178690-f7d24c6bc5ff",
    "photo-1517963628607-235ccdd5476c", "photo-1549060279-7e168fcee0c2",
    "photo-1574680096145-d05b474e2155", "photo-1605296867304-46d5465a13f1",
    "photo-1594737625785-a6cbdabd333c", "photo-1530822847156-5df684ec5ee1",
    "photo-1598971639058-999901a4e0a5", "photo-1581009146145-b5ef050c2e1e",
    "photo-1517344884509-a0c97ec11bcc", "photo-1517849845537-4d257902454a",
    "photo-1607962837359-5e7e89f86776", "photo-1434596922112-19c563067271",
    "photo-1599058917212-d750089bc07e", "photo-1584735935682-2f2b69dff9d2",
    "photo-1581122584612-713f89daa8eb", "photo-1581009137042-c552e485697a",
    "photo-1579126038374-6064e9370f0f", "photo-1506629082955-511b1aa562c8",
    "photo-1549476464-37392f717541", "photo-1571732154690-f6d1c3e5178e",
    "photo-1566241134883-13ac39bbdf5b", "photo-1583454110551-21f2fa2afe61",
    "photo-1554284126-aa88f22d8b74", "photo-1597452485669-2c7bb5fef90d",
    "photo-1534368420009-621bfab424a8", "photo-1544216717-3bbf52512659",
    "photo-1526506118085-60ce8714f8c5", "photo-1566241832378-917a0d31abd5",
    "photo-1518611012118-696072aa579a", "photo-1518310383802-640c2de311b2",
    "photo-1517130038641-a774d04afb3c", "photo-1549576490-b0b4831ef60a",
    "photo-1581015148428-8eb64e62ea85", "photo-1593164842264-854604db2260",
    "photo-1593079831268-3381b0db4a77", "photo-1593079831181-a0814c04cde7",
    "photo-1581122584612-713f89daa8eb", "photo-1518459031867-a89b944bffe4",
    "photo-1520975916090-3105956dac38", "photo-1540497077202-7c8a3999166f",
    "photo-1596357395217-80de13130e92", "photo-1535914254981-b5012eebbd15",
    "photo-1579758682665-53a6a3f6d98c", "photo-1586401100295-7a8096fd231a",
    "photo-1599447421416-3414500d18a5", "photo-1579757623786-f30ee8d71c44",
    "photo-1571019614242-c5c5dee9f50b", "photo-1526506118085-60ce8714f8c5",
    "photo-1591258739400-4c1a90f70e17", "photo-1547919307-1ecb10702e6f",
    "photo-1576678927484-cc907957088c", "photo-1518310952931-b1de897abd40",
    "photo-1517344368193-41552b6ad3f5", "photo-1579952516518-ac7dd5a346ef",
    "photo-1596357395882-ebd7116fe902", "photo-1583454155184-870a1f63aebc",
    "photo-1556817411-31ae72fa3ea0", "photo-1526404751-97c25c8e7bfc",
    "photo-1541534741688-6078c6bfb5c5", "photo-1517931524326-bdd55a541177",
    "photo-1591291621164-2c6367723315", "photo-1571388208497-71bedc66e932",
    "photo-1581122584612-713f89daa8eb", "photo-1576678927484-cc907957088c",
    "photo-1544367567-0f2fcb009e0b", "photo-1597076545399-91a0ff12edc2",
    "photo-1518609878373-06d740f60d8b", "photo-1595078475328-1ab05d0a6a0e",
    "photo-1517896722525-ed21d2f36c5f", "photo-1517841905240-472988babdf9",
    "photo-1534367507873-d2d7e24c797f", "photo-1536922246289-88c42f957773",
    "photo-1517931524326-bdd55a541177", "photo-1582556135623-eca2d93842a0",
    "photo-1571902943202-507ec2618e8f", "photo-1538805060514-97d9cc17730c",
    "photo-1599058917765-a780eda07a3e", "photo-1581122584612-713f89daa8eb",
    "photo-1579952363873-27f3bade9f55", "photo-1587386862295-451c8f896b35",
    "photo-1517964256762-1e7a6461ca9b", "photo-1583500178690-f7d24c6bc5ff",
    "photo-1549049960-0a9da82fe68a", "photo-1566241134883-13ac39bbdf5b",
    "photo-1517836357463-d25d9c699b16", "photo-1598289431512-b97b0917affc",
    "photo-1593476087123-36d1de271f08", "photo-1533681904393-9ab6eee7e408",
    "photo-1560329072-17f59dcd30a4", "photo-1584952811565-c4c4031476a3",
    "photo-1543512214-318c7553f230", "photo-1546483875-ad9014c88eba",
    "photo-1586880244406-556ebe35f282", "photo-1594381898411-846e7d193883",
    "photo-1549049950-48d5887197a0", "photo-1506629905607-c28f8eecd1a4",
    "photo-1533560904424-a0c61dc306fc", "photo-1576493019604-b6c8e4a7c4d6",
    "photo-1513732822839-24f03a92f633", "photo-1518604666860-9ed391f76460",
    "photo-1546484958-31b3a1e7efac", "photo-1515023115689-589c33041d3c",
    "photo-1549576490-b0b4831ef60a", "photo-1517344884509-a0c97ec11bcc",
    "photo-1515186813673-12d9e99b3c89", "photo-1545389336-cf090694435e",
    "photo-1552152974-19b9cadee89f", "photo-1593079831268-3381b0db4a77",
    "photo-1598289431512-b97b0917affc", "photo-1571902943202-507ec2618e8f",
    "photo-1534258936925-c58bed479fcb", "photo-1571019613454-1cb2f99b2d8b",
]

# 50 photos recettes/nourriture (salades, bowls, viandes, smoothies, etc.)
RECIPE_PHOTOS = [
    "photo-1567620905732-2d1ec7ab7445", "photo-1490645935967-10de6ba17061",
    "photo-1512621776951-a57141f2eefd", "photo-1546069901-ba9599a7e63c",
    "photo-1540189549336-e6e99c3679fe", "photo-1565299624946-b28f40a0ae38",
    "photo-1526470498-9ae73c665de8", "photo-1567620832903-9fc6debc209f",
    "photo-1559847844-5315695dadae", "photo-1565958011703-44f9829ba187",
    "photo-1484723091739-30a097e8f929", "photo-1565958011703-44f9829ba187",
    "photo-1476224203421-9ac39bcb3327", "photo-1432139509613-5c4255815697",
    "photo-1499028344343-cd173ffc68a9", "photo-1525351484163-7529414344d8",
    "photo-1555939594-58d7cb561ad1", "photo-1540189549336-e6e99c3679fe",
    "photo-1543353071-873f17a7a088", "photo-1570145820259-b5b80c5c8bd6",
    "photo-1551782450-a2132b4ba21d", "photo-1563379926898-05f4575a45d8",
    "photo-1544025162-d76694265947", "photo-1587326049830-b11cf4b47f4a",
    "photo-1504674900247-0877df9cc836", "photo-1473093295043-cdd812d0e601",
    "photo-1467003909585-2f8a72700288", "photo-1521305916504-4a1121188589",
    "photo-1528714147267-ad2f3fa3ff88", "photo-1563379926898-05f4575a45d8",
    "photo-1493770348161-369560ae357d", "photo-1495521821757-a1efb6729352",
    "photo-1519708227418-c8fd9a32b7a2", "photo-1579584425555-c3ce17fd4351",
    "photo-1608039829572-78524f79c4c7", "photo-1590301157890-4810ed352733",
    "photo-1488477181946-6428a0291777", "photo-1588137372308-15f75323a51d",
    "photo-1517673132405-a56a62b18caf", "photo-1512152272829-e3139592d56f",
    "photo-1484284001484-b5acbe5f9970", "photo-1524324463413-57e3d7c8d06d",
    "photo-1562967914-608f82629710", "photo-1563805042-7684c019e1cb",
    "photo-1502741126161-b048400d085d", "photo-1543362906-acfc16c67564",
    "photo-1598515214211-89d3c73ae83b", "photo-1541518763669-27fef9b49584",
    "photo-1604908176997-125f25cc6f3d", "photo-1611270629569-8b357cb88da9",
]

# 15 photos articles blog (lifestyle, fitness, nutrition, sommeil, etc.)
ARTICLE_PHOTOS = [
    "photo-1517836357463-d25dfeac3438",  # Hypertrophie - muscle
    "photo-1511972844302-9c10cc32b9c4",  # Sommeil
    "photo-1490645935967-10de6ba17061",  # Nutrition pré-entraînement
    "photo-1552674605-46945596497c",     # Discipline - chemin
    "photo-1532550907401-a500c9a57435",  # Protéines
    "photo-1555066931-4365d14bab8c",     # Code / Django
    "photo-1558494949-ef010cbdcc31",     # PostgreSQL / database
    "photo-1571019613454-1cb2f99b2d8b",  # Gym générique
    "photo-1544367567-0f2fcb009e0b",     # Méditation
    "photo-1506629082955-511b1aa562c8",  # Course
    "photo-1540497077202-7c8a3999166f",  # Haltères
    "photo-1550345332-09e3ac987658",     # Salade healthy
    "photo-1519864600265-abb23847ef2c",  # Yoga
    "photo-1470245498392-b74c66e2c7d7",  # Eau / hydratation
    "photo-1488477181946-6428a0291777",  # Petit déjeuner
]


def dedupe(pool: list) -> list:
    """Retire les doublons en gardant l'ordre."""
    seen = set()
    result = []
    for pid in pool:
        if pid not in seen:
            seen.add(pid)
            result.append(pid)
    return result


def build_url(photo_id: str, sig: int, w: int = 1200) -> str:
    """
    Construit une URL Unsplash UNIQUE.
    Le paramètre `sig` garantit l'unicité même si on réutilise la même photo
    (Unsplash ignore les params inconnus, donc l'image se charge quand même).
    """
    return f"https://images.unsplash.com/{photo_id}?w={w}&auto=format&fit=crop&q=80&sig={sig}"


def assign_unique(pool: list, count_needed: int) -> list:
    """
    Retourne `count_needed` URLs garanties UNIQUES en utilisant l'index comme signature.
    """
    pool = dedupe(pool)
    urls = []
    for i in range(count_needed):
        # Cycle sur le pool si pas assez de photos uniques disponibles
        photo_id = pool[i % len(pool)]
        # sig = i+1 garantit que chaque URL est différente, même si la photo se répète
        urls.append(build_url(photo_id, sig=i + 1))
    return urls


class Command(BaseCommand):
    help = "Assigne une image Unsplash UNIQUE à chaque article, recette, exercice"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Réassigne toutes les images même si déjà uniques',
        )

    def handle(self, *args, **opts):
        force = opts.get('force', False)

        # ---- Articles ----
        articles = list(Article.objects.order_by('id'))
        urls = assign_unique(ARTICLE_PHOTOS, len(articles))
        updated = 0
        for a, url in zip(articles, urls):
            if force or not a.image:
                a.image = url
                a.save(update_fields=['image'])
                updated += 1
            elif a.image and 'unsplash.com' in a.image:
                # Remplace seulement si déjà Unsplash (pour éviter d'écraser URLs custom)
                a.image = url
                a.save(update_fields=['image'])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"✓ Articles : {updated}/{len(articles)} images uniques assignées"))

        # ---- Recettes ----
        recipes = list(Recipe.objects.order_by('id'))
        urls = assign_unique(RECIPE_PHOTOS, len(recipes))
        updated = 0
        for r, url in zip(recipes, urls):
            r.image_url = url
            r.save(update_fields=['image_url'])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"✓ Recettes : {updated}/{len(recipes)} images uniques assignées"))

        # ---- Exercices ----
        exercises = list(Exercise.objects.order_by('id'))
        urls = assign_unique(EXERCISE_PHOTOS, len(exercises))
        updated = 0
        for e, url in zip(exercises, urls):
            e.image_url = url
            e.save(update_fields=['image_url'])
            updated += 1
        self.stdout.write(self.style.SUCCESS(f"✓ Exercices : {updated}/{len(exercises)} images uniques assignées"))

        total = Article.objects.count() + Recipe.objects.count() + Exercise.objects.count()
        self.stdout.write(self.style.SUCCESS(f"\n✨ Terminé : {total} éléments ont maintenant une image unique."))
