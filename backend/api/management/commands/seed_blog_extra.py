"""
Ajoute 6 articles de blog fitness suppl\u00e9mentaires et nettoie les articles
dev hors-sujet (Django, PostgreSQL) qui n'ont pas leur place sur un site sport.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from api.models import User, Article, Category, Tag


class Command(BaseCommand):
    help = "Ajoute 6 articles fitness premium + supprime les articles dev hors-sujet"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Seeding extra blog articles..."))

        # 1. Supprimer les articles dev hors-sujet
        deleted = Article.objects.filter(
            slug__in=[
                "decouvrir-django-rest-framework",
                "pourquoi-adopter-postgresql-en-production",
            ]
        ).delete()
        self.stdout.write(f"  Suppressions dev: {deleted[0]}")

        # 2. Tags fitness (remplacer les tags dev)
        Tag.objects.filter(
            name__in=["api", "django", "postgresql", "python", "search", "base-de-donnees", "production", "feedback"]
        ).delete()
        fitness_tags_data = [
            "d\u00e9butant", "avanc\u00e9", "cardio", "muscu", "perte-de-poids",
            "prise-de-masse", "nutrition", "sommeil", "motivation", "r\u00e9cup\u00e9ration",
            "course", "yoga", "mobilit\u00e9", "habitudes", "mental",
        ]
        tags = {}
        for name in fitness_tags_data:
            t, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            tags[name] = t

        # 3. Auteur
        author, _ = User.objects.get_or_create(
            username="coach_fitwell",
            defaults={"email": "coach@fitwell.com"},
        )

        # 4. Cat\u00e9gories (existent d\u00e9j\u00e0)
        cats = {c.name: c for c in Category.objects.all()}

        # 5. Articles \u00e0 cr\u00e9er
        articles = [
            {
                "title": "HIIT vs Cardio Long : Lequel Choisir ?",
                "category": "Cardio & Endurance",
                "image": "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?q=80&w=1600&auto=format&fit=crop",
                "tags": ["cardio", "perte-de-poids", "d\u00e9butant"],
                "content": """
                <h2>HIIT ou Cardio Long : la guerre est-elle vraiment justifi\u00e9e ?</h2>
                <p>Si tu es perdu entre les pros du HIIT qui jurent que tout le reste est d\u00e9pass\u00e9 et les amoureux de la course longue qui te traitent de fou, ce guide est pour toi. La v\u00e9rit\u00e9 ? Les deux fonctionnent. Mais pas pour les m\u00eames raisons.</p>

                <h3>Le HIIT : court, brutal, efficace</h3>
                <p>Le High Intensity Interval Training alterne des phases d'effort tr\u00e8s intense (80-95\u202f% de ta fr\u00e9quence cardiaque max) avec des phases de r\u00e9cup\u00e9ration courte. Une s\u00e9ance dure entre 15 et 25\u202fminutes.</p>
                <p><strong>Avantages :</strong></p>
                <ul>
                    <li>Br\u00fble beaucoup de calories en peu de temps</li>
                    <li>Effet "afterburn" (EPOC) : ton corps continue de br\u00fbler des calories pendant 24h</li>
                    <li>Am\u00e9liore la VO2max rapidement</li>
                    <li>Id\u00e9al quand tu manques de temps</li>
                </ul>
                <p><strong>Inconv\u00e9nients :</strong></p>
                <ul>
                    <li>Tr\u00e8s exigeant pour le syst\u00e8me nerveux</li>
                    <li>Risque de blessure si la technique est mauvaise</li>
                    <li>Pas adapt\u00e9 aux d\u00e9butants complets</li>
                </ul>

                <h3>Le cardio long : doux, durable, sous-estim\u00e9</h3>
                <p>Une course \u00e0 60-70\u202f% de ta FC max pendant 45 \u00e0 90\u202fminutes. Vieux jeu ? Pas du tout. C'est ce que font les coureurs de fond, les cyclistes pros, les nageurs olympiques pour b\u00e2tir leur base.</p>
                <p><strong>Avantages :</strong></p>
                <ul>
                    <li>D\u00e9veloppe l'endurance fondamentale</li>
                    <li>Am\u00e9liore l'efficacit\u00e9 m\u00e9tabolique (br\u00fbler les graisses)</li>
                    <li>Faible stress sur le corps : tu peux le faire 4-5\u202ffois par semaine</li>
                    <li>Excellent pour la sant\u00e9 cardiaque \u00e0 long terme</li>
                </ul>

                <h3>Verdict : combine les deux</h3>
                <p>Les meilleurs r\u00e9sultats viennent d'un m\u00e9lange. Une semaine type pourrait ressembler \u00e0 :</p>
                <ul>
                    <li>2\u202fs\u00e9ances de cardio long (45-60 min)</li>
                    <li>1\u202fs\u00e9ance de HIIT (20 min)</li>
                    <li>1\u202fs\u00e9ance de muscu</li>
                    <li>Repos actif (marche, yoga)</li>
                </ul>
                <p>Si tu d\u00e9bbutes : commence par 4 semaines de cardio long uniquement, puis introduis le HIIT progressivement. Ton corps te remerciera.</p>
                """,
            },
            {
                "title": "Apprendre \u00e0 Courir : Plan 30 Jours pour D\u00e9butants",
                "category": "Cardio & Endurance",
                "image": "https://images.unsplash.com/photo-1571008887538-b36bb32f4571?q=80&w=1600&auto=format&fit=crop",
                "tags": ["course", "d\u00e9butant", "cardio"],
                "content": """
                <h2>Tu veux te mettre \u00e0 la course ? Voici le plan qui marche.</h2>
                <p>Courir, c'est gratuit, c'est efficace, et tu peux le faire partout. Mais attention : 80\u202f% des d\u00e9butants se blessent dans les 6\u202fpremiers mois \u00e0 cause d'erreurs \u00e9vitables. Suis ce plan progressif et tu tiendras dans la dur\u00e9e.</p>

                <h3>R\u00e8gle d'or : marche-course</h3>
                <p>Personne ne te demande de courir 30\u202fminutes d\u00e8s le premier jour. La m\u00e9thode marche-course est ce qui fonctionne le mieux pour les d\u00e9butants.</p>

                <h3>Semaine 1 : 3 sorties de 20 minutes</h3>
                <p>Alterne 1\u202fminute de course / 2\u202fminutes de marche. R\u00e9p\u00e8te 7\u202ffois. Compte aussi 5\u202fminutes de marche d'\u00e9chauffement avant et 5\u202fminutes de retour au calme apr\u00e8s.</p>

                <h3>Semaine 2 : 3 sorties de 25 minutes</h3>
                <p>Alterne 2\u202fminutes de course / 2\u202fminutes de marche. R\u00e9p\u00e8te 6\u202ffois.</p>

                <h3>Semaine 3 : 3 sorties de 30 minutes</h3>
                <p>Alterne 3\u202fminutes de course / 2\u202fminutes de marche. R\u00e9p\u00e8te 6\u202ffois.</p>

                <h3>Semaine 4 : 3 sorties de 30 minutes</h3>
                <p>Alterne 5\u202fminutes de course / 1\u202fminute de marche. R\u00e9p\u00e8te 5\u202ffois.</p>

                <h3>Les 5 erreurs qui te blesseront</h3>
                <ol>
                    <li><strong>Aller trop vite :</strong> Si tu ne peux pas tenir une conversation en courant, tu vas trop vite. Ralentis.</li>
                    <li><strong>Sauter l'\u00e9chauffement :</strong> 5\u202fminutes de marche rapide + quelques mouvements articulaires, c'est non n\u00e9gociable.</li>
                    <li><strong>Mauvaises chaussures :</strong> Va dans un magasin sp\u00e9cialis\u00e9 qui analyse ta foul\u00e9e. \u00c7a vaut l'investissement.</li>
                    <li><strong>Trop courir trop vite :</strong> N'augmente jamais ton volume hebdomadaire de plus de 10\u202f% par semaine.</li>
                    <li><strong>Ignorer la douleur :</strong> Une g\u00eane qui dure plus de 3\u202fjours\u202f? Repos, glace, et consultation si \u00e7a persiste.</li>
                </ol>

                <h3>Ton corps va changer</h3>
                <p>D\u00e8s la 3e\u202fsemaine, tu vas sentir : meilleur sommeil, plus d'\u00e9nergie en journ\u00e9e, esprit plus clair. La course n'est pas qu'une activit\u00e9 physique, c'est une m\u00e9ditation en mouvement.</p>
                """,
            },
            {
                "title": "5 Habitudes Matinales Qui Changent Tout",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1600&auto=format&fit=crop",
                "tags": ["habitudes", "motivation", "mental"],
                "content": """
                <h2>Comment tu commences ta journ\u00e9e d\u00e9termine comment tu la termines.</h2>
                <p>Les 90\u202fpremi\u00e8res minutes apr\u00e8s ton r\u00e9veil sont les plus pr\u00e9cieuses de la journ\u00e9e. Voici 5\u202fhabitudes simples qui, accumul\u00e9es, vont transformer ta vie.</p>

                <h3>1. Lumi\u00e8re du soleil dans les 30 minutes</h3>
                <p>D\u00e8s le r\u00e9veil, expose ton visage \u00e0 la lumi\u00e8re naturelle pendant au moins 5\u202fminutes. Pas \u00e0 travers une fen\u00eatre : sors. Cela r\u00e8gle ton horloge biologique, augmente le cortisol matinal (le bon, celui qui te r\u00e9veille), et programme ton sommeil pour le soir.</p>
                <p><strong>R\u00e9sultat :</strong> Tu t'endormiras plus facilement le soir et te r\u00e9veilleras naturellement plus t\u00f4t.</p>

                <h3>2. Hydratation avant la caf\u00e9ine</h3>
                <p>Apr\u00e8s 7-8h de sommeil, tu es d\u00e9shydrat\u00e9. Bois 500\u202fmL d'eau (avec une pinc\u00e9e de sel et un demi-citron, optionnel) avant ton caf\u00e9. \u00c7a r\u00e9veille ton syst\u00e8me digestif et r\u00e9hydrate ton cerveau.</p>

                <h3>3. Mouvement 5 minutes</h3>
                <p>Pas une s\u00e9ance d'1h. Juste 5\u202fminutes : 20\u202fpompes, 30\u202fsquats, 1\u202fminute de planche, ou simplement quelques \u00e9tirements. \u00c7a active ta circulation et r\u00e9veille ton syst\u00e8me nerveux.</p>

                <h3>4. Pas de t\u00e9l\u00e9phone pendant 1 heure</h3>
                <p>L'erreur n\u00b01 du XXIe\u202fsi\u00e8cle : v\u00e9rifier les notifs d\u00e8s le r\u00e9veil. Tu donnes le contr\u00f4le de tes \u00e9motions \u00e0 des e-mails, des r\u00e9seaux sociaux, des news. Garde la premi\u00e8re heure pour toi.</p>

                <h3>5. Liste 3 priorit\u00e9s</h3>
                <p>Avant d'ouvrir ton ordinateur, \u00e9cris sur papier les 3\u202fchoses les plus importantes \u00e0 accomplir aujourd'hui. Si tu fais ces 3\u202fchoses, ta journ\u00e9e est r\u00e9ussie, peu importe le reste.</p>

                <h3>Routine type (45 minutes)</h3>
                <ul>
                    <li>R\u00e9veil \u2192 verre d'eau (1 min)</li>
                    <li>Sortir prendre la lumi\u00e8re (5 min)</li>
                    <li>Mouvement (5 min)</li>
                    <li>Douche froide finale (3 min)</li>
                    <li>Petit-d\u00e9j sain + lecture/journaling (20 min)</li>
                    <li>Liste des 3 priorit\u00e9s (2 min)</li>
                </ul>
                <p>Commence par UNE seule habitude. Ajoute-en une nouvelle chaque semaine. En 5\u202fsemaines, ta vie aura chang\u00e9.</p>
                """,
            },
            {
                "title": "Le Je\u00fbne Intermittent : Mythe ou R\u00e9alit\u00e9 ?",
                "category": "Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=1600&auto=format&fit=crop",
                "tags": ["nutrition", "perte-de-poids", "habitudes"],
                "content": """
                <h2>Le je\u00fbne intermittent : la m\u00e9thode qui divise.</h2>
                <p>Star d'Instagram, ador\u00e9 par les biohackers, controvers\u00e9 chez les nutritionnistes. Que dit vraiment la science ?</p>

                <h3>Qu'est-ce que c'est ?</h3>
                <p>Le je\u00fbne intermittent (IF) consiste \u00e0 alterner des p\u00e9riodes de prise alimentaire et des p\u00e9riodes de je\u00fbne. La forme la plus populaire est le 16/8 : tu manges sur une fen\u00eatre de 8\u202fheures (par exemple 12h-20h) et tu je\u00fbnes les 16\u202fautres heures.</p>

                <h3>Ce que la science valide</h3>
                <ul>
                    <li><strong>Perte de poids :</strong> En r\u00e9duisant la fen\u00eatre alimentaire, beaucoup de gens mangent naturellement moins. \u00c7a marche pour la perte de gras chez la majorit\u00e9.</li>
                    <li><strong>Sensibilit\u00e9 \u00e0 l'insuline :</strong> Am\u00e9lior\u00e9e, ce qui aide \u00e0 pr\u00e9venir le diab\u00e8te de type\u202f2.</li>
                    <li><strong>Autophagie :</strong> Apr\u00e8s 16h de je\u00fbne, tes cellules nettoient leurs d\u00e9chets. Effet anti-vieillissement document\u00e9.</li>
                    <li><strong>Simplification :</strong> Moins de repas \u00e0 pr\u00e9parer = moins de d\u00e9cisions = moins de stress mental.</li>
                </ul>

                <h3>Ce que la science nuance</h3>
                <p>Le je\u00fbne intermittent n'est <strong>pas magique</strong>. Les calories totales restent le facteur principal pour la perte de poids. Si tu manges 3500\u202fcalories en 8\u202fheures, tu prends du poids.</p>

                <h3>Pour qui \u00e7a marche</h3>
                <ul>
                    <li>Les gens qui n'ont pas faim le matin (\u00e9vite de te forcer \u00e0 d\u00e9jeuner)</li>
                    <li>Ceux qui veulent perdre du gras sans compter les calories</li>
                    <li>Les actifs qui pr\u00e9f\u00e8rent moins de pr\u00e9paration</li>
                </ul>

                <h3>Pour qui \u00e7a ne marche pas (ou peu)</h3>
                <ul>
                    <li>Les femmes enceintes ou qui allaitent</li>
                    <li>Les personnes avec un historique de troubles alimentaires</li>
                    <li>Les sportifs en prise de masse (difficile d'avaler les calories)</li>
                    <li>Les diab\u00e9tiques de type\u202f1 (sans suivi m\u00e9dical)</li>
                </ul>

                <h3>Comment commencer</h3>
                <p>Ne saute pas brutalement de 3 repas \u00e0 16/8. Commence par 12/12 (manger sur 12h, je\u00fbner 12h) pendant une semaine. Puis 14/10. Puis 16/8 si tu te sens bien. Boire de l'eau, du caf\u00e9 noir et du th\u00e9 est OK pendant la fen\u00eatre de je\u00fbne.</p>

                <h3>\u00c9coute ton corps</h3>
                <p>Si tu es fatigu\u00e9, irritable, ou si tes performances sportives chutent, ce n'est peut-\u00eatre pas pour toi. La meilleure di\u00e8te est celle que tu peux tenir 10\u202fans, pas 10\u202fjours.</p>
                """,
            },
            {
                "title": "Comment Rester Motiv\u00e9 Quand Tout Va Mal",
                "category": "Mental & Mindset",
                "image": "https://images.unsplash.com/photo-1599058917765-a780eda07a3e?q=80&w=1600&auto=format&fit=crop",
                "tags": ["motivation", "mental"],
                "content": """
                <h2>La motivation est un mythe. La discipline est la r\u00e9alit\u00e9.</h2>
                <p>Tu d\u00e9marres en force le 1er\u202fjanvier, tu vas \u00e0 la salle 5\u202ffois la premi\u00e8re semaine, tu manges sain, tu dors t\u00f4t. Puis vient la 3e semaine, le froid, le stress du boulot, et l\u2019envie de tout l\u00e2cher. Voici comment tenir.</p>

                <h3>1. La motivation vient APR\u00c8S l\u2019action, pas avant</h3>
                <p>Tout le monde attend de "se sentir motiv\u00e9" pour agir. C\u2019est le mauvais ordre. Commence par 5\u202fminutes d\u2019action, et la motivation suit. Mets tes baskets. Une fois habill\u00e9, tu sortiras. Une fois dehors, tu courras.</p>

                <h3>2. R\u00e9duis tes objectifs jusqu\u2019\u00e0 ce qu\u2019ils paraissent ridicules</h3>
                <p>L\u2019objectif "je vais \u00e0 la salle 1 heure" est trop gros un mauvais jour. Remplace-le par "je vais \u00e0 la salle, je fais 1 exercice, je rentre". Tu y vas presque toujours plus longtemps. Mais m\u00eame si tu pars apr\u00e8s 10\u202fminutes, tu y \u00e9tais. C\u2019est une victoire.</p>

                <h3>3. Identifie ton "pourquoi"</h3>
                <p>"Je veux \u00eatre en forme" est trop vague. "Je veux pouvoir jouer avec mes enfants sans \u00eatre essoufl\u00e9" est concret. "Je veux mettre cette robe pour le mariage de ma s\u0153ur en juin" est puissant. Plus c\u2019est sp\u00e9cifique, plus \u00e7a tient.</p>

                <h3>4. Chaque jour rate\u00e9 doit \u00eatre suivi d\u2019un jour r\u00e9ussi</h3>
                <p>Une faiblesse ne d\u00e9truit rien. Mais deux jours rat\u00e9s de suite cr\u00e9ent un nouveau pattern. R\u00e8gle simple : <strong>jamais deux jours de suite \u00e0 ne rien faire</strong>.</p>

                <h3>5. Trouve un partenaire de responsabilit\u00e9</h3>
                <p>Un ami, un coach, un groupe en ligne. Quelqu\u2019un qui te demande "Tu y \u00e9tais aujourd\u2019hui\u202f?". L\u2019accountability divise par 3 le risque d\u2019abandonner.</p>

                <h3>6. C\u00e9l\u00e8bre les petites victoires</h3>
                <p>Tu as fait ta s\u00e9ance malgr\u00e9 la pluie\u202f? F\u00e9licite-toi, sinc\u00e8rement. Tu as r\u00e9sist\u00e9 au gros gateau\u202f? Note-le quelque part. Le cerveau apprend par r\u00e9compense, pas par punition.</p>

                <h3>La v\u00e9rit\u00e9 brutale</h3>
                <p>Personne n\u2019est motiv\u00e9 tout le temps. Pas les athl\u00e8tes pros, pas les acteurs, pas tes idoles. Ils ont juste construit des syst\u00e8mes qui les portent quand la motivation manque. Construis ton syst\u00e8me. Et fais le travail, m\u00eame quand \u00e7a t\u2019emmerde.</p>
                """,
            },
            {
                "title": "\u00c9tirements vs Mobilit\u00e9 : la Vraie Diff\u00e9rence",
                "category": "R\u00e9cup\u00e9ration",
                "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=1600&auto=format&fit=crop",
                "tags": ["mobilit\u00e9", "yoga", "r\u00e9cup\u00e9ration"],
                "content": """
                <h2>\u00c9tirement statique, dynamique, mobilit\u00e9 articulaire\u202f: lequel pour quoi ?</h2>
                <p>"Je m\u2019\u00e9tire avant le sport pour \u00e9viter les blessures" entend-on partout. La science dit l\u2019inverse. Voici ce qu\u2019il faut vraiment faire.</p>

                <h3>\u00c9tirement statique</h3>
                <p>Tu prends une position et tu la tiens 30\u202fsecondes \u00e0 1\u202fminute. Exemple : ramener sa jambe vers la poitrine et tenir.</p>
                <p><strong>Quand l\u2019utiliser :</strong> APR\u00c8S l\u2019entra\u00eenement ou en s\u00e9ance d\u00e9di\u00e9e. JAMAIS avant : \u00e7a r\u00e9duit la force de 5-10\u202f% pendant les heures suivantes.</p>

                <h3>\u00c9tirement dynamique</h3>
                <p>Mouvements contr\u00f4l\u00e9s qui am\u00e8nent les articulations \u00e0 leur amplitude maximale, sans \u00e0-coups. Exemples\u202f: balancers de jambes, cercles de bras, fentes marche.</p>
                <p><strong>Quand l\u2019utiliser :</strong> AVANT l\u2019entra\u00eenement comme \u00e9chauffement. Pr\u00e9pare le syst\u00e8me nerveux et augmente la temp\u00e9rature musculaire.</p>

                <h3>Mobilit\u00e9 articulaire</h3>
                <p>Travail actif sur l\u2019amplitude de chaque articulation, en douceur. Diff\u00e9rent de la souplesse passive : tu d\u00e9veloppes le contr\u00f4le sur toute la zone de mouvement.</p>
                <p><strong>Quand l\u2019utiliser :</strong> Tous les jours, m\u00eame courte session de 10\u202fminutes. C\u2019est ce qui pr\u00e9vient le mieux les blessures \u00e0 long terme.</p>

                <h3>Programme mobilit\u00e9 quotidienne (10 minutes)</h3>
                <ol>
                    <li>Cercles de cou : 10x dans chaque sens (1 min)</li>
                    <li>Cercles d\u2019\u00e9paules : 10x avant, 10x arri\u00e8re (1 min)</li>
                    <li>Cat-cow (chat-vache) : 10 r\u00e9p\u00e9titions lentes (1 min)</li>
                    <li>Hip circles : 10 dans chaque sens, chaque jambe (2 min)</li>
                    <li>World\u2019s greatest stretch : 5 par c\u00f4t\u00e9 (2 min)</li>
                    <li>Squat profond pos\u00e9 : tenir 1 minute (1 min)</li>
                    <li>Down dog vers cobra : 10 transitions (2 min)</li>
                </ol>

                <h3>Le mythe de la souplesse</h3>
                <p>\u00catre tr\u00e8s souple n\u2019est pas un objectif en soi. Une souplesse excessive sans contr\u00f4le musculaire = instabilit\u00e9 articulaire = blessures. L\u2019objectif est l\u2019amplitude FONCTIONNELLE, pas le grand \u00e9cart.</p>

                <h3>R\u00e8gles simples</h3>
                <ul>
                    <li><strong>Avant le sport :</strong> dynamique, jamais statique</li>
                    <li><strong>Apr\u00e8s le sport :</strong> statique court, retour au calme</li>
                    <li><strong>Tous les jours :</strong> mobilit\u00e9 articulaire 10 min</li>
                    <li><strong>1\u202ffois/semaine :</strong> s\u00e9ance d\u00e9di\u00e9e de 30\u202fmin (yoga, pilates)</li>
                </ul>
                <p>Ton corps n\u2019est pas une voiture. Il a besoin d\u2019entretien quotidien, pas juste d\u2019une r\u00e9vision tous les 6\u202fmois.</p>
                """,
            },
        ]

        created_count = 0
        for data in articles:
            cat = cats.get(data["category"])
            if not cat:
                self.stdout.write(self.style.WARNING(f"  Skipped {data['title']} - cat not found"))
                continue
            slug = slugify(data["title"])
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": data["title"],
                    "author": author,
                    "category": cat,
                    "content": data["content"].strip(),
                    "image": data["image"],
                    "is_published": True,
                },
            )
            # Tags
            article_tags = [tags[t] for t in data["tags"] if t in tags]
            article.tags.set(article_tags)
            article.save()
            if created:
                created_count += 1
                self.stdout.write(f"  + {data['title']}")
            else:
                self.stdout.write(f"  = {data['title']} (existait)")

        total = Article.objects.count()
        self.stdout.write(self.style.SUCCESS(f"\nDone. {created_count} new articles. Total: {total}"))
