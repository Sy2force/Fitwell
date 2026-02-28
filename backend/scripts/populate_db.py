import os
import sys
import django
import random
from datetime import datetime, timedelta

# Add project root to sys.path
sys.path.append(os.getcwd())

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category, Article, Comment

User = get_user_model()

def populate():
    print("Initializing System Protocol: Content Injection...")

    # Create Superuser if not exists
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@fitwell.system'}
    )
    if created:
        admin_user.set_password('password123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.level = 99
        admin_user.health_score = 100
        admin_user.save()
        print(f"Admin Access Granted: {admin_user.username}")
    else:
        print(f"Admin Detected: {admin_user.username}")

    # Create Elite Users (Athletes)
    elite_users = []
    usernames = ['Apex_Predator', 'Velocity_X', 'Iron_Titan', 'Neuro_Hacker']
    for name in usernames:
        user, created = User.objects.get_or_create(
            username=name, 
            defaults={'email': f'{name.lower()}@fitwell.net'}
        )
        if created:
            user.set_password('password123')
            user.level = random.randint(5, 50)
            user.xp = random.randint(1000, 50000)
            user.health_score = random.randint(85, 99)
            user.save()
            print(f"Athlete Registered: {name}")
        elite_users.append(user)

    # Create Categories
    categories_data = [
        {'name': 'Bio-Hacking', 'description': 'Optimizing human performance through science and technology.'},
        {'name': 'Mindset', 'description': 'Stoic philosophy and mental resilience for the modern leader.'},
        {'name': 'Nutrition', 'description': 'Precision fueling for cognitive and physical excellence.'},
        {'name': 'Recovery', 'description': 'Advanced protocols for regeneration and longevity.'},
        {'name': 'Strength', 'description': 'Functional hypertrophy and aesthetic power.'}
    ]

    categories = {}
    for data in categories_data:
        cat, created = Category.objects.get_or_create(name=data['name'])
        categories[data['name']] = cat
        if created:
            print(f"Sector Established: {data['name']}")

    # Create Articles
    articles_data = [
        {
            'title': 'The Dopamine Protocol: Reclaiming Focus in a Hyper-Connected World',
            'content': """Attention is the currency of the elite. In an era of algorithmic distraction, the ability to focus is a superpower. The modern operator is bombarded by a relentless stream of digital noise. This fragmentation of focus is not merely an annoyance; it is a tactical disadvantage.

To reclaim mental sovereignty, we must engage in a rigorous protocol of dopamine regulation. This is not about asceticism, but about recalibrating neurochemistry to value the high-yield rewards of deep work and genuine connection over cheap digital hits.

## The Protocol

1. **Digital Sunset:** Sever all connections 90 minutes pre-sleep. Blue light suppresses melatonin; information overload suppresses recovery.
2. **Deep Work Blocks:** Dedicate the first 4 hours of the operational window to high-leverage tasks. No comms. No slack. Pure output.
3. **Environmental Exposure:** Mandatory 20-minute immersion in organic environments daily. Reduces cortisol, restores cognitive baseline.

By controlling the input, we maximize the output. We become architects of our cognition.""",
            'category': 'Mindset',
            'author': elite_users[0],
            'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Thermal Contrast Therapy: Engineering Resilience',
            'content': """Comfort is the enemy of adaptation. The human organism was forged in the crucible of stress, designed to thrive in response to hormetic challenges. Modern life is a cage of climate-controlled stagnation.

Enter thermal contrast therapy. By exposing the physiology to extreme cold (-110°C) and intense heat (90°C), we trigger a cascade of survival responses that enhance longevity and operational capacity.

## The Mechanism

*   **Cryo-Exposure:** Vasoconstriction forces blood to the core, flushing metabolic waste. Rewarming floods extremities with nutrient-rich blood. Activates brown adipose tissue for metabolic upregulation.
*   **Hyperthermic Conditioning:** Saunas induce Heat Shock Proteins (HSPs), repairing cellular damage and preventing atrophy. Mimics cardiovascular load.

Integrating thermal stress is not a luxury; it is biological maintenance for the high-performance machine.""",
            'category': 'Recovery',
            'author': elite_users[2],
            'image_url': 'https://images.unsplash.com/photo-1544367563-12123d8965cd?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Ketogenic Adaptation: Fueling the Executive Processor',
            'content': """Glucose is volatile. It burns hot and fast, creating insulin volatility. For the elite operator, stability is paramount. Ketones offer a superior, clean-burning fuel source for the brain.

Shifting metabolic substrate from glucose to ketones (beta-hydroxybutyrate) unlocks a state of cognitive precision.

## Performance Metrics

*   **Cognitive Clarity:** Elimination of 'brain fog'. Sharp, sustained focus.
*   **Endurance:** Consistent energy output from dawn to dusk. No post-meal crash.
*   **Autonomy:** Freedom from the hunger loop.

Transitioning requires discipline. The reward is a mind that operates at the theoretical limit.""",
            'category': 'Nutrition',
            'author': elite_users[1],
            'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Iron Philosophy: Training as a Meditative Discipline',
            'content': """The gym is not for vanity. It is a forge for the will. Every rep asks: 'Can you endure?' Every set answers: 'I can.'

We apply Stoic principles to physical training. Control the controllables: form, tension, breath. Accept the resistance.

## The Code

1.  **Amor Fati:** Love the struggle. Pain is the raw material of growth.
2.  **Memento Mori:** Time is finite. Do not waste a single heartbeat on mediocrity.
3.  **Sympatheia:** Strength is for service, not status.

When we train with this intent, the iron becomes a tool for total self-mastery.""",
            'category': 'Mindset',
            'author': elite_users[0],
            'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Hypertrophy Science: The Modern Approach',
            'content': """Building a physique that commands respect requires more than effort. It requires physics. Biomechanics, volume management, progressive overload.

The old methods are obsolete. We train with data.

## Growth Vectors

*   **Mechanical Tension:** The primary driver. Force generation across the muscle fiber.
*   **Metabolic Stress:** The accumulation of metabolites signaling adaptation.
*   **Eccentric Damage:** Controlled micro-trauma for reconstruction.

Execute with surgical precision. Leave the ego. Focus on the contraction.""",
            'category': 'Strength',
            'author': elite_users[2],
            'image_url': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Circadian Synchronization: Mastering the Biological Clock',
            'content': """You are not a machine; you are an ecosystem synchronized to the solar cycle. The suprachiasmatic nucleus (SCN) orchestrates hormonal output, digestion, and repair.

Disrupting this rhythm with artificial light and erratic fueling is sabotage.

## Alignment Strategy

*   **First Light:** Ocular exposure to sunlight within 30 minutes of wake. Sets the cortisol peak and anchors the sleep drive.
*   **Digital Twilight:** Dim lights post-sunset. Red spectrum only. Signal the recovery phase.
*   **Nutrient Timing:** Feed during daylight. Fast during darkness.

Master the clock. Master the energy.""",
            'category': 'Bio-Hacking',
            'author': elite_users[3],
            'image_url': 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?q=80&w=2000&auto=format&fit=crop'
        }
    ]

    for article_data in articles_data:
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'content': article_data['content'],
                'category': categories[article_data['category']],
                'author': article_data['author'],
                'image_url': article_data['image_url'],
                'is_published': True
            }
        )
        if created:
            print(f"Data Uploaded: {article.title}")
            
            # Add some comments
            commenters = [u for u in elite_users if u != article_data['author']]
            for _ in range(random.randint(2, 5)):
                commenter = random.choice(commenters)
                comments_text = [
                    "Data confirms this hypothesis. Executing protocol.",
                    "Optimized efficiency observed.",
                    "This aligns with current field metrics.",
                    "Critical intel. Acknowledged.",
                    "Performance increased by 15% following this methodology."
                ]
                Comment.objects.create(
                    article=article,
                    user=commenter,
                    content=random.choice(comments_text)
                )

    print("System Population Complete. All systems operational.")

if __name__ == '__main__':
    populate()
