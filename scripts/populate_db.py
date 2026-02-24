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
    print("Creating luxury content...")

    # Create Superuser if not exists
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@fitwell.com'}
    )
    if created:
        admin_user.set_password('password123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")
    else:
        print(f"Admin user already exists: {admin_user.username}")

    # Create Elite Users
    elite_users = []
    usernames = ['Marcus_Aurelius', 'Athena_Wellness', 'Zenith_Performance', 'Kairos_Health']
    for name in usernames:
        user, created = User.objects.get_or_create(
            username=name, 
            defaults={'email': f'{name.lower()}@fitwell.com'}
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created elite user: {name}")
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
            print(f"Created category: {data['name']}")

    # Create Articles
    articles_data = [
        {
            'title': 'The Dopamine Detox: Reclaiming Focus in a Hyper-Connected World',
            'content': """In an age of infinite distraction, attention is the ultimate currency. The modern executive is bombarded by a relentless stream of notifications, algorithmic loops, and digital noise. This fragmentation of focus is not merely an annoyance; it is a cognitive catastrophe.

To reclaim our mental sovereignty, we must engage in a rigorous protocol of dopamine fasting. This is not about asceticism, but about recalibrating our neurochemistry to appreciate the subtle, slow-burning rewards of deep work and genuine connection.

## The Protocol

1. **Digital Sunset:** Disconnect from all screens 90 minutes before sleep. The blue light suppresses melatonin, but the information overload suppresses peace.
2. **Monk Mode:** Dedicate the first 4 hours of your day to high-leverage tasks. No email. No Slack. Just pure output.
3. **Nature Immersion:** Spend at least 20 minutes daily in a green space. The fractal patterns of nature reduce cortisol and restore attention.

By stepping back from the noise, we amplify the signal. We become the architects of our own minds, rather than the passive consumers of someone else's algorithm.""",
            'category': 'Mindset',
            'author': elite_users[0],
            'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Cryotherapy & Heat Shock Proteins: The Science of Resilience',
            'content': """Comfort is the enemy of progress. The human body was forged in the crucible of adaptation, designed to thrive in response to hormetic stress. Yet, our modern lives are hermetically sealed in climate-controlled stagnation.

Enter thermal contrast therapy. By exposing the body to extreme cold (-110°C) and intense heat (90°C), we trigger a cascade of physiological responses that enhance longevity and performance.

## The Mechanism

*   **Cold Exposure:** Vasoconstriction forces blood to the core, flushing out metabolic waste. Upon rewarming, nutrient-rich blood floods the extremities. This process also activates brown adipose tissue, boosting metabolism.
*   **Heat Exposure:** Saunas induce the release of Heat Shock Proteins (HSPs), which repair damaged proteins and prevent muscle atrophy. They also mimic moderate cardiovascular exercise.

Integrating thermal stress into your weekly routine is not a luxury; it is a biological imperative for those seeking to extend their healthspan.""",
            'category': 'Recovery',
            'author': elite_users[2],
            'image_url': 'https://images.unsplash.com/photo-1544367563-12123d8965cd?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Ketosis and Cognitive Clarity: Fueling the Executive Brain',
            'content': """Glucose is a volatile fuel. It burns hot and fast, leaving you riding the rollercoaster of insulin spikes and crashes. For the elite performer, stability is key. Ketones offer a cleaner, more efficient energy source for the brain.

When the body shifts into ketosis, it metabolizes fat into ketone bodies (beta-hydroxybutyrate). These molecules can cross the blood-brain barrier and provide a sustained, jitter-free source of energy.

## Benefits for the Leader

*   **Mental Acuity:** The 'brain fog' associated with carb-heavy diets lifts, revealing a sharp, laser-like focus.
*   **Sustained Energy:** No post-lunch crash. Just consistent output from dawn to dusk.
*   **Appetite Suppression:** Freedom from the constant distraction of hunger pangs.

Transitioning to a ketogenic lifestyle requires discipline, but the reward is a mind that operates at the cutting edge of its potential.""",
            'category': 'Nutrition',
            'author': elite_users[1],
            'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'The Stoic Athlete: Training as a Meditative Practice',
            'content': """The gym is not a place to build vanity muscles; it is a temple for the reconstruction of the self. Every rep is a question: 'Can you endure?' Every set is an answer: 'I can.'

Stoicism teaches us that we have control over our actions, but not the outcomes. In training, this translates to focusing on the process—the form, the tension, the breath—rather than the weight on the bar.

## Principles of Stoic Training

1.  **Amor Fati (Love of Fate):** Embrace the pain, the fatigue, and the struggle. They are the raw materials of your transformation.
2.  **Memento Mori (Remember Death):** You have a finite number of heartbeats. Do not waste them on half-hearted efforts.
3.  **Sympatheia:** Your physical strength is meant to serve the greater good, not just your ego.

When we train with this mindset, the iron becomes a tool for spiritual growth.""",
            'category': 'Mindset',
            'author': elite_users[0],
            'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Hypertrophy for the Modern Gentleman: A Scientific Approach',
            'content': """Building a physique that commands respect requires more than just lifting heavy things. It requires an understanding of biomechanics, volume management, and progressive overload.

The 'bro-split' is dead. The modern gentleman trains with intelligence.

## Key Drivers of Growth

*   **Mechanical Tension:** The force generated by the muscle fibers. This is the primary driver of hypertrophy.
*   **Metabolic Stress:** The 'pump'—the accumulation of metabolites that signals the body to adapt.
*   **Muscle Damage:** The micro-tears that occur during eccentric loading.

We recommend a Push/Pull/Legs split, executed with surgical precision. Leave the ego at the door. Focus on the contraction.""",
            'category': 'Strength',
            'author': elite_users[2],
            'image_url': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Circadian Rhythm Optimization: Mastering Your Internal Clock',
            'content': """Your body is not a machine; it is an ecosystem governed by the rising and setting of the sun. The suprachiasmatic nucleus (SCN) in your brain orchestrates every biological process, from hormone release to digestion.

Disrupting this rhythm with late-night blue light and erratic meal times is a recipe for disaster.

## Aligning with the Sun

*   **Morning Light:** View sunlight within 30 minutes of waking. This sets your cortisol peak and anchors your sleep drive for the night.
*   **Evening Darkness:** Dim the lights after sunset. Use candlelight or red light to signal to your body that it is time to rest.
*   **Meal Timing:** Eat during the daylight hours. Late-night eating disrupts the body's repair processes.

Master your clock, and you master your energy.""",
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
            print(f"Created article: {article.title}")
            
            # Add some comments
            commenters = [u for u in elite_users if u != article_data['author']]
            for _ in range(random.randint(2, 5)):
                commenter = random.choice(commenters)
                comments_text = [
                    "Insightful perspective. This aligns perfectly with my own experience.",
                    "The science behind this is undeniable. Excellent breakdown.",
                    "I've been implementing this protocol for a month. The results are transformative.",
                    "A necessary reminder for all of us striving for excellence.",
                    "Brilliant. Precisely what I needed to read today."
                ]
                Comment.objects.create(
                    article=article,
                    user=commenter,
                    content=random.choice(comments_text)
                )

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
