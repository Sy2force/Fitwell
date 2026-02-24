import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category, Article, Comment

User = get_user_model()

def seed_luxury_content():
    print("💎 Seeding Luxury Content...")

    # 1. Create Users
    admin, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@fitwell.elite', 'is_staff': True, 'is_superuser': True}
    )
    admin.set_password('password123')
    admin.save()

    elite_user, _ = User.objects.get_or_create(
        username='elite_member',
        defaults={'email': 'member@fitwell.elite'}
    )
    elite_user.set_password('password123')
    elite_user.save()

    print("✅ Users created: admin / elite_member (password: password123)")

    # 2. Create Categories
    categories_data = [
        "Elite Training", "Haute Nutrition", "Luxury Gear", "Mindset & Zen", "Wellness Travel"
    ]
    categories = []
    for name in categories_data:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)
    
    print(f"✅ {len(categories)} Categories created")

    # 3. Create Luxury Articles
    articles_data = [
        {
            "title": "The Art of Bio-Hacking: Beyond the Ordinary",
            "content": """In the pursuit of perfection, the modern athlete requires more than just discipline—they demand innovation. Bio-hacking is not merely a trend; it is the definitive edge in elite performance. 

From cryotherapy chambers that plunge to -110°C to hyperbaric oxygen therapy sessions that revitalize cellular regeneration, the toolkit of the elite is vast and scientifically rigorous. We explore the latest protocols adopted by Olympic gold medalists and Fortune 500 CEOs alike.

True wellness is about precision. It is about understanding your genome, your microbiome, and your unique physiological signature. It is about crafting a lifestyle that is not just healthy, but optimized for greatness.""",
            "image_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=2070&auto=format&fit=crop",
            "category": "Elite Training"
        },
        {
            "title": "Molecular Gastronomy for the Athletic Palate",
            "content": """Fueling the body is an art form. Gone are the days of bland chicken and broccoli. Enter the era of high-performance nutrition where flavor profiles meet macro-nutrient precision.

We sat down with Michelin-starred chefs who are redefining post-workout recovery meals. Imagine a deconstructed wild salmon tartare infused with omega-3 rich oils, or a saffron-infused quinoa bowl designed to reduce inflammation immediately after exertion.

This is not just food; it is biochemical architecture. Every bite is calculated, every ingredient sourced from the most pristine environments on Earth. Because your body is a temple, and it deserves nothing less than the divine.""",
            "image_url": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2053&auto=format&fit=crop",
            "category": "Haute Nutrition"
        },
        {
            "title": "Sanctuaries of Silence: Top Wellness Retreats 2026",
            "content": """In a world of constant noise, silence is the ultimate luxury. We have curated a list of the most exclusive wellness retreats on the planet—places where time stands still and the soul can breathe.

First on our list is 'The Void' in the Swiss Alps, a minimalist architectural marvel suspended over a glacier. Here, digital detoxification is mandatory, and the only soundtrack is the wind.

Then there is 'Azure' in the Maldives, an underwater spa where meditation sessions are conducted with views of the coral reef. These are not vacations; they are transformative experiences designed to reset your baseline to a state of absolute calm.""",
            "image_url": "https://images.unsplash.com/photo-1544367563-12123d8965cd?q=80&w=2070&auto=format&fit=crop",
            "category": "Wellness Travel"
        },
        {
            "title": "Minimalist Design in Home Gyms",
            "content": """Your training space should inspire power, not clutter. The aesthetic of the modern home gym is shifting towards dark, moody tones, natural materials, and equipment that doubles as sculpture.

We explore the rise of walnut-wood rowing machines, leather-bound medicine balls, and black matte steel racks. Lighting plays a crucial role—think ambient, indirect strips that highlight the contours of the room and the athlete within.

A gym is no longer a garage afterthought. It is a centerpiece of the luxury home, a testament to the dedication of its owner. Design your strength.""",
            "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop",
            "category": "Luxury Gear"
        },
        {
            "title": "Cognitive Dominance: The Executive Mindset",
            "content": """Physical strength is nothing without mental fortitude. The elite performer knows that the mind must be trained with the same rigor as the body.

Cognitive dominance is the ability to maintain clarity under extreme pressure. It is about emotional regulation, focus, and the ability to visualize success before it manifests.

Techniques such as transcendental meditation, neurofeedback training, and stoic philosophy are staples in the daily routine of the ultra-successful. Master your mind, and the world will yield to your will.""",
            "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1999&auto=format&fit=crop",
            "category": "Mindset & Zen"
        }
    ]

    for data in articles_data:
        cat = Category.objects.get(name=data['category'])
        Article.objects.get_or_create(
            title=data['title'],
            defaults={
                'content': data['content'],
                'author': admin,
                'category': cat,
                'image_url': data['image_url'],
                'is_published': True
            }
        )
    
    print(f"✅ {len(articles_data)} Luxury Articles created")

    print("✨ Database seeded successfully with Luxury content!")

if __name__ == '__main__':
    seed_luxury_content()
