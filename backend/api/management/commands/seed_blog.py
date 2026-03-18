import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from api.models import User, Article, Category, Comment

class Command(BaseCommand):
    help = 'Seed complete blog with 25+ quality articles'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding Complete Blog...'))

        # Categories
        categories_data = [
            "Entraînement Force",
            "Nutrition Performance",
            "Mental & Mindset",
            "Récupération",
            "Bio-Hacking",
            "Cardio & Endurance"
        ]
        
        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
            if created:
                self.stdout.write(f"   ✅ {cat_name}")

        # Author
        author, _ = User.objects.get_or_create(
            username="coach_fitwell",
            defaults={'email': 'coach@fitwell.com'}
        )
        if not author.check_password("fitwell2026"):
            author.set_password("fitwell2026")
            author.save()

        # 25 Articles complets
        articles_data = [
            {
                "title": "Les 5 Piliers de l'Hypertrophie Musculaire",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1200",
                "content": "<h2>Construire du Muscle : La Science</h2><p>L'hypertrophie repose sur 5 piliers : tension mécanique progressive, stress métabolique, dommages musculaires contrôlés, fréquence optimale et récupération stratégique.</p><h3>1. Tension Mécanique</h3><p>Surcharge progressive = croissance. Augmentez poids, reps ou volume chaque semaine.</p><h3>2. Stress Métabolique</h3><p>Le pump crée un environnement anabolique. Séries de 12-15 reps avec tempo lent.</p><h3>3. Dommages Musculaires</h3><p>Micro-déchirures = réparation + croissance. 1-2 séances intenses/muscle/semaine max.</p>"
            },
            {
                "title": "Sommeil : L'Arme Secrète des Athlètes",
                "category": "Récupération",
                "image": "https://images.unsplash.com/photo-1511972844302-9c10cc32b9c4?w=1200",
                "content": "<h2>8 Heures = Performance Maximale</h2><p>LeBron James dort 12h/jour. Federer 10-12h. Le sommeil profond sécrète 70% de l'hormone de croissance quotidienne.</p><h3>Protocole Optimisation</h3><p>Température : 16-19°C. Noir total. Horaires fixes. Pas d'écrans 90min avant. Magnésium 400mg + Glycine 3g.</p><h3>Impact Mesurable</h3><p>+9% vitesse sprint, +9% précision, +11% temps réaction avec 8-10h vs 6-7h.</p>"
            },
            {
                "title": "Nutrition Pré-Entraînement : Le Timing Parfait",
                "category": "Nutrition Performance",
                "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200",
                "content": "<h2>Quoi Manger et Quand</h2><h3>3-4h Avant</h3><p>Protéines 30-40g + Glucides 50-80g + Lipides 10-15g. Ex: 200g poulet + 150g riz + légumes.</p><h3>60-90min Avant</h3><p>Glucides rapides 30-40g + Protéines 15-20g. Ex: Whey + banane + miel.</p><h3>30min Avant</h3><p>Caféine 200-400mg + Glucides simples 20-30g + Créatine 5g.</p>"
            },
            {
                "title": "La Discipline : Votre Superpouvoir",
                "category": "Mental & Mindset",
                "image": "https://images.unsplash.com/photo-1552674605-46945596497c?w=1200",
                "content": "<h2>Discipline = Liberté</h2><p>Jocko Willink : Plus vous êtes discipliné, plus vous êtes libre.</p><h3>3 Piliers</h3><p>1. Systèmes > Motivation. Routines non-négociables.</p><p>2. Petites victoires. Faites votre lit = première victoire du jour.</p><p>3. Accountability. Engagement public = +65% compliance.</p><h3>66 Jours</h3><p>Il faut 66 jours pour ancrer une habitude. Choisissez UNE habitude. Trackez. Pas d'exception.</p>"
            },
            {
                "title": "Protéines : Guide Complet",
                "category": "Nutrition Performance",
                "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=1200",
                "content": "<h2>Combien, Quand, Lesquelles</h2><h3>Dosage</h3><p>Sédentaire: 0.8g/kg. Actif: 1.6-2.2g/kg. Athlète: 2.2-3g/kg.</p><h3>Répartition</h3><p>4-5 repas de 30-40g. Synthèse protéique maximisée avec 30-40g/repas.</p><h3>Sources Tier S</h3><p>Whey isolate, œufs, poulet, poisson blanc. Digestibilité 95%+.</p>"
            },
            {
                "title": "HIIT vs LISS : Quel Cardio Choisir",
                "category": "Cardio & Endurance",
                "image": "https://images.unsplash.com/photo-1434596922112-19c563067271?w=1200",
                "content": "<h2>Haute vs Basse Intensité</h2><h3>HIIT</h3><p>Avantages: Efficace temps, brûle calories 24h après, améliore VO2max.</p><p>Inconvénients: Taxant SNC, risque surentraînement.</p><h3>LISS</h3><p>Avantages: Récupération active, faible stress, durable.</p><p>Inconvénients: Temps long, moins efficace calories.</p><h3>Recommandation</h3><p>HIIT 2-3x/semaine + LISS quotidien (marche 30min).</p>"
            },
            {
                "title": "Créatine : Le Supplément #1",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1579722820308-d74e571900a9?w=1200",
                "content": "<h2>Le Supplément le Plus Recherché</h2><h3>Bénéfices Prouvés</h3><p>+15% force, +10% masse musculaire, +20% ATP, amélioration cognitive.</p><h3>Protocole</h3><p>5g/jour, tous les jours. Pas de phase de charge nécessaire. Monohydrate = meilleur rapport qualité/prix.</p><h3>Timing</h3><p>Peu importe. Pré ou post-workout, l'important est la prise quotidienne.</p>"
            },
            {
                "title": "Squat : Technique Parfaite",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=1200",
                "content": "<h2>Le Roi des Exercices</h2><h3>Setup</h3><p>Pieds largeur épaules, orteils 15-30° extérieur. Barre haute trapèzes ou basse deltoïdes postérieurs.</p><h3>Descente</h3><p>Hanches en arrière, genoux suivent orteils. Dos neutre. Profondeur: pli hanche sous genou.</p><h3>Montée</h3><p>Poussez sol avec talons. Hanches et épaules montent ensemble. Verrouillez en haut.</p>"
            },
            {
                "title": "Développé Couché : Maximiser la Charge",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=1200",
                "content": "<h2>Technique Powerlifting</h2><h3>Arch (Cambrure)</h3><p>Omoplates serrées, cage thoracique haute. Réduit amplitude, protège épaules.</p><h3>Grip</h3><p>Largeur: index sur anneaux (81cm). Poignets droits, coudes 45°.</p><h3>Trajectoire</h3><p>Descente: vers bas pectoraux. Montée: ligne droite vers yeux. Leg drive actif.</p>"
            },
            {
                "title": "Soulevé de Terre : Puissance Totale",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1200",
                "content": "<h2>L'Exercice Ultime</h2><h3>Position Départ</h3><p>Pieds sous barre, tibias touchent barre. Hanches entre genoux et épaules. Dos neutre.</p><h3>Pull</h3><p>Tension lats, poussez sol avec jambes. Barre colle aux tibias. Hanches et épaules montent ensemble.</p><h3>Lockout</h3><p>Hanches en avant, épaules en arrière. Pas d'hyperextension lombaire.</p>"
            },
            {
                "title": "Tractions : De 0 à 20 Reps",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=1200",
                "content": "<h2>Progression Garantie</h2><h3>Phase 1: Négatifs</h3><p>Sautez en haut, descendez lentement (5sec). 3x5 reps.</p><h3>Phase 2: Bandées</h3><p>Élastique assistance. Réduisez résistance progressivement. 3x8-10.</p><h3>Phase 3: Complètes</h3><p>Poids corps. Augmentez volume. 5x5 puis 3x10 puis 3x15.</p><h3>Phase 4: Lestées</h3><p>Ajoutez poids. 3x5 avec +10kg, +20kg, etc.</p>"
            },
            {
                "title": "Jeune Intermittent : Science vs Hype",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=1200",
                "content": "<h2>16/8 : Miracle ou Mode ?</h2><h3>Bénéfices Réels</h3><p>Simplicité, contrôle appétit, autophagie, sensibilité insuline.</p><h3>Limites</h3><p>Pas magique pour perte poids. Calories totales = roi. Peut réduire performance si mal timé.</p><h3>Protocole</h3><p>Fenêtre 12h-20h. Entraînement à 16h. Premier repas post-workout. Dernier repas 19h30.</p>"
            },
            {
                "title": "Mobilité : L'Entraînement Invisible",
                "category": "Récupération",
                "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=1200",
                "content": "<h2>Prévention Blessures</h2><h3>Routine Quotidienne 15min</h3><p>Cat-Cow 10x, World's Greatest Stretch 5x/côté, 90/90 Hip Stretch 2min/côté, Shoulder Dislocations 20x.</p><h3>Pré-Workout</h3><p>Échauffement dynamique. Pas d'étirements statiques. Activation musculaire ciblée.</p><h3>Post-Workout</h3><p>Étirements statiques 30sec/muscle. Foam rolling zones tendues.</p>"
            },
            {
                "title": "Stress : L'Ennemi Invisible",
                "category": "Mental & Mindset",
                "image": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1200",
                "content": "<h2>Cortisol et Performance</h2><h3>Impact Négatif</h3><p>Catabolisme musculaire, stockage graisse abdominale, baisse testostérone, sommeil perturbé.</p><h3>Gestion</h3><p>Méditation 10min/jour, respiration 4-7-8, marche nature 30min, sommeil 8h, magnésium.</p><h3>Entraînement</h3><p>Réduisez volume si stress élevé. Privilégiez LISS vs HIIT. Deload chaque 4-6 semaines.</p>"
            },
            {
                "title": "Glucides : Ami ou Ennemi ?",
                "category": "Nutrition Performance",
                "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1200",
                "content": "<h2>La Vérité sur les Carbs</h2><h3>Rôle</h3><p>Énergie primaire muscles. Recharge glycogène. Performance haute intensité.</p><h3>Timing</h3><p>Autour entraînement = optimal. Matin = énergie journée. Soir = sommeil (si toléré).</p><h3>Quantité</h3><p>Perte gras: 1-2g/kg. Maintien: 3-4g/kg. Prise masse: 5-7g/kg.</p><h3>Sources</h3><p>Riz, patate douce, avoine, fruits, légumes. Évitez sucres raffinés hors workout.</p>"
            },
            {
                "title": "Lipides : Essentiels et Méconnus",
                "category": "Nutrition Performance",
                "image": "https://images.unsplash.com/photo-1447078806655-40579c2520d6?w=1200",
                "content": "<h2>Graisses Saines</h2><h3>Bénéfices</h3><p>Hormones (testostérone), absorption vitamines, satiété, inflammation.</p><h3>Quantité</h3><p>Minimum: 0.5g/kg. Optimal: 0.8-1.2g/kg. Ne descendez jamais sous 0.5g/kg.</p><h3>Sources</h3><p>Oméga-3: Saumon, sardines, noix. Mono-insaturés: Huile olive, avocat, amandes. Saturés: Œufs, viande, coco (modération).</p>"
            },
            {
                "title": "Hydratation : Plus que de l'Eau",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=1200",
                "content": "<h2>Électrolytes et Performance</h2><h3>Besoins</h3><p>Base: 35ml/kg. Entraînement: +500-1000ml/h. Chaleur: +50%.</p><h3>Électrolytes</h3><p>Sodium: 3-5g/jour. Potassium: 3-4g. Magnésium: 400mg. Ajoutez pincée sel à l'eau.</p><h3>Timing</h3><p>500ml au réveil. 250ml toutes les 2h. 500ml pré-workout. 250ml toutes les 15min pendant.</p>"
            },
            {
                "title": "Progression Linéaire : Le Meilleur Programme Débutant",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1200",
                "content": "<h2>Starting Strength Simplifié</h2><h3>Programme</h3><p>3x/semaine. A: Squat 3x5, Bench 3x5, Deadlift 1x5. B: Squat 3x5, Press 3x5, Row 3x5.</p><h3>Progression</h3><p>+2.5kg chaque séance membres supérieurs. +5kg jambes. Si échec 3x, deload 10%.</p><h3>Durée</h3><p>3-6 mois. Gains garantis: +40kg squat, +30kg bench, +60kg deadlift.</p>"
            },
            {
                "title": "PPL : Push Pull Legs pour Intermédiaires",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=1200",
                "content": "<h2>Split Optimal Fréquence</h2><h3>Structure</h3><p>Push: Pecs/Épaules/Triceps. Pull: Dos/Biceps. Legs: Jambes/Abs. 6x/semaine ou 3x/semaine.</p><h3>Exemple Push</h3><p>Bench 4x6, Incline DB 3x10, Shoulder Press 3x8, Lateral Raise 3x12, Tricep Pushdown 3x12.</p><h3>Volume</h3><p>10-20 sets/muscle/semaine. Augmentez progressivement.</p>"
            },
            {
                "title": "Periodisation : Planifier vos Gains",
                "category": "Entraînement Force",
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1200",
                "content": "<h2>Cycles d'Entraînement</h2><h3>Linéaire</h3><p>Semaine 1-4: 4x12 (hypertrophie). 5-8: 4x8 (force). 9-12: 5x5 (force max). 13: Deload.</p><h3>Ondulatoire</h3><p>Lundi: Lourd 5x5. Mercredi: Modéré 4x8. Vendredi: Léger 3x12. Varie stimulus.</p><h3>Bloc</h3><p>4 semaines accumulation (volume). 4 semaines intensification (charge). 1 semaine réalisation (test max).</p>"
            },
            {
                "title": "Caféine : Ergogène Légal",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200",
                "content": "<h2>Performance +3-5%</h2><h3>Dosage</h3><p>3-6mg/kg. Pour 80kg: 240-480mg. Commencez bas, augmentez si toléré.</p><h3>Timing</h3><p>30-60min pré-workout. Demi-vie 5h. Pas après 14h si sommeil sensible.</p><h3>Tolérance</h3><p>Cycle 2 semaines on, 1 semaine off. Ou réservez jours importants.</p>"
            },
            {
                "title": "Respiration : Technique Wim Hof",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1200",
                "content": "<h2>Oxygénation Maximale</h2><h3>Protocole</h3><p>30 respirations profondes rapides. Expiration complète, retention 1-2min. Inspiration profonde, retention 15sec. Répétez 3 rounds.</p><h3>Bénéfices</h3><p>Réduction stress, boost énergie, système immunitaire, focus mental.</p><h3>Timing</h3><p>Matin à jeun ou pré-méditation. Jamais dans l'eau (risque évanouissement).</p>"
            },
            {
                "title": "Douche Froide : Adaptation au Stress",
                "category": "Récupération",
                "image": "https://images.unsplash.com/photo-1620335182689-f3c0e6be3a8f?w=1200",
                "content": "<h2>Hormesis et Résilience</h2><h3>Protocole</h3><p>Commencez 30sec froid fin douche. Augmentez 15sec/semaine jusqu'à 2-3min.</p><h3>Bénéfices</h3><p>Réduction inflammation, boost dopamine, récupération musculaire, discipline mentale.</p><h3>Timing</h3><p>Matin: éveil. Post-workout: récupération (mais peut réduire hypertrophie si immédiat).</p>"
            },
            {
                "title": "Visualisation : Entraînement Mental",
                "category": "Mental & Mindset",
                "image": "https://images.unsplash.com/photo-1499728603263-13726abce5fd?w=1200",
                "content": "<h2>Préparation Psychologique</h2><h3>Technique</h3><p>5-10min pré-workout. Yeux fermés. Visualisez chaque rep, chaque série. Sentez le poids, la contraction.</p><h3>Science</h3><p>Activation mêmes zones cérébrales que mouvement réel. Améliore connexion neuromusculaire.</p><h3>Application</h3><p>Avant PR, visualisez succès. Avant compétition, rejouez performance parfaite.</p>"
            },
            {
                "title": "Objectifs SMART : Planification Stratégique",
                "category": "Mental & Mindset",
                "image": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1200",
                "content": "<h2>De Rêve à Réalité</h2><h3>SMART</h3><p>Spécifique: Squat 140kg. Mesurable: +2.5kg/semaine. Atteignable: Actuellement 100kg. Pertinent: Objectif force. Temporel: 16 semaines.</p><h3>Mauvais</h3><p>'Devenir fort'. Vague, non mesurable.</p><h3>Bon</h3><p>'Squat 3x5 à 140kg d'ici 16 semaines en progressant 2.5kg/semaine'.</p><h3>Tracking</h3><p>Carnet entraînement. Photos mensuelles. Mesures corporelles. Tests force.</p>"
            }
        ]

        for data in articles_data:
            cat = categories.get(data["category"])
            article, created = Article.objects.get_or_create(
                title=data["title"],
                defaults={
                    "author": author,
                    "category": cat,
                    "content": data["content"],
                    "image": data["image"],
                    "is_published": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"   ✅ {data['title']}"))
            else:
                article.content = data["content"]
                article.image = data["image"]
                article.category = cat
                article.save()
                self.stdout.write(f"   🔄 {data['title']}")

        self.stdout.write(self.style.SUCCESS(f'\n✅ Blog Complete! {len(articles_data)} articles'))
