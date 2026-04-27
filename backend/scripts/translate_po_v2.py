"""
Parser .po robuste qui g\u00e8re les msgid multi-lignes et applique les traductions
manquantes en utilisant un dictionnaire FR\u2192EN \u00e9tendu.
"""
import re
from pathlib import Path


TRANSLATIONS = {
    # Pages About
    "\u00c0 propos de nous": "About us",
    "Le sport accessible.": "Accessible fitness.",
    "Pour de vrai.": "For real.",
    "Nos valeurs": "Our values",
    "Honn\u00eatet\u00e9 radicale": "Radical honesty",
    "Simplicit\u00e9": "Simplicity",
    "Long terme": "Long term",
    "Inclusivit\u00e9": "Inclusivity",
    "Ce qui nous diff\u00e9rencie": "What sets us apart",
    "Du contenu cr\u00e9\u00e9 par des gens qui pratiquent": "Content created by people who actually train",
    "Tu progresses \u00e0 ton rythme": "You progress at your own pace",
    "Une plateforme \u00e9volutive": "An evolving platform",
    "Open source dans l'esprit": "Open source in spirit",
    "Notre promesse": "Our promise",
    "On ne te promet pas de te transformer.": "We don't promise to transform you.",
    "On te donne les outils pour le faire toi-m\u00eame.": "We give you the tools to do it yourself.",
    "Notre mission": "Our mission",
    "Notre histoire": "Our story",
    "Le sport n'est pas une punition.": "Sport is not a punishment.",
    "C'est un cadeau que tu te fais.": "It's a gift you give yourself.",

    # Home
    "Apprends": "Learn",
    "\u00e0 bouger": "to move",
    "Bouge mieux.": "Move better.",
    "Mange bien.": "Eat well.",
    "Vis plus fort.": "Live stronger.",
    "Personne en pleine s\u00e9ance de sport": "Person during a workout session",
    "Des chiffres, mais surtout des r\u00e9sultats concrets": "Numbers that translate into real results",
    "Exercices expliqu\u00e9s": "Explained exercises",
    "Technique, muscles cibl\u00e9s, niveau": "Technique, target muscles, level",
    "Recettes saines": "Healthy recipes",
    "Simples, rapides, d\u00e9licieuses": "Simple, fast, delicious",
    "Articles conseils": "Advice articles",
    "Nutrition, motivation, progression": "Nutrition, motivation, progress",
    "Accessible partout": "Available everywhere",
    "Sur ton t\u00e9l\u00e9phone, ton ordi, o\u00f9 tu veux": "On your phone, your computer, anywhere",
    "Ce que FitWell t'apporte": "What FitWell brings you",
    "Bouger avec intelligence": "Move smart",
    "Voir les exercices \u2192": "View exercises \u2192",
    "Manger pour se nourrir": "Eat to nourish",
    "Voir les recettes \u2192": "View recipes \u2192",
    "Comprendre son corps": "Understand your body",
    "Lire les articles \u2192": "Read articles \u2192",
    "Nos conseils de base": "Our core advice",
    "4 habitudes": "4 habits",
    "Bouge 30 minutes par jour": "Move 30 minutes a day",
    "Bois 1,5 litre d'eau": "Drink 1.5 liters of water",
    "Dors 7 \u00e0 8 heures": "Sleep 7 to 8 hours",
    "Mange des vrais aliments": "Eat real foods",
    "Pourquoi FitWell est diff\u00e9rent": "Why FitWell is different",
    "Pas de publicit\u00e9s d\u00e9guis\u00e9es": "No disguised advertising",
    "Du contenu pour tous les niveaux": "Content for every level",
    "Des m\u00e9thodes bas\u00e9es sur la science": "Science-based methods",
    "Gratuit pour commencer": "Free to start",
    "Commence aujourd'hui": "Start today",
    "Ton corps te dira merci": "Your body will thank you",
    "dans 30 jours.": "in 30 days.",
    "Bienvenue sur FitWell": "Welcome to FitWell",
    "Cr\u00e9er mon compte gratuit": "Create my free account",
    "Lire nos conseils": "Read our advice",
    "Rejoindre l'aventure (gratuit)": "Join the adventure (free)",

    # Legal
    "Mentions l\u00e9gales": "Legal notice",
    "\u00c9diteur du site :": "Site publisher:",
    "FitWell \u2014 projet p\u00e9dagogique de d\u00e9veloppement web": "FitWell \u2014 educational web development project",
    "Responsable de la publication :": "Publication manager:",
    "\u00c9quipe FitWell": "FitWell team",
    "H\u00e9bergement :": "Hosting:",
    "Render.com (San Francisco, \u00c9tats-Unis)": "Render.com (San Francisco, USA)",
    "Contact :": "Contact:",
    "Donn\u00e9es personnelles & RGPD": "Personal data & GDPR",
    "Donn\u00e9es collect\u00e9es :": "Data collected:",
    "Identifiants de connexion (nom d'utilisateur, email)": "Login credentials (username, email)",
    "Informations de profil que tu choisis de fournir (\u00e2ge, poids, objectif sportif)": "Profile information you choose to provide (age, weight, fitness goal)",
    "Historique de tes sessions d'entra\u00eenement": "Your training session history",
    "Adresse IP et type de navigateur (s\u00e9curit\u00e9, statistiques anonymes)": "IP address and browser type (security, anonymous statistics)",
    "Tes droits :": "Your rights:",
    "Acc\u00e8s \u00e0 tes donn\u00e9es : visibles dans ton profil \u00e0 tout moment": "Data access: visible in your profile at any time",
    "Rectification : tu peux modifier ton profil quand tu veux": "Rectification: you can edit your profile anytime",
    "Suppression : bouton 'Supprimer mon compte' dans les param\u00e8tres": "Deletion: 'Delete my account' button in settings",
    "Portabilit\u00e9 : tes donn\u00e9es peuvent t'\u00eatre envoy\u00e9es sur demande": "Portability: your data can be sent to you on request",
    "Aucune revente, aucun partage commercial.": "No reselling, no commercial sharing.",
    "Tes donn\u00e9es restent priv\u00e9es et ne sont jamais c\u00e9d\u00e9es \u00e0 des tiers.": "Your data remains private and is never given to third parties.",
    "Conform\u00e9ment au R\u00e8glement G\u00e9n\u00e9ral sur la Protection des Donn\u00e9es (RGPD), FitWell collecte uniquement les informations strictement n\u00e9cessaires au fonctionnement du service.": "In accordance with the General Data Protection Regulation (GDPR), FitWell only collects information strictly necessary for the operation of the service.",
    "garde ta session active apr\u00e8s connexion": "keeps your session active after login",
    "prot\u00e8ge contre les attaques CSRF (s\u00e9curit\u00e9)": "protects against CSRF attacks (security)",
    "m\u00e9morise ta langue pr\u00e9f\u00e9r\u00e9e": "remembers your preferred language",
    "Aucun cookie publicitaire, aucun tracker tiers.": "No advertising cookies, no third-party trackers.",
    "Pas de Google Analytics, pas de Facebook Pixel, pas de remarketing.": "No Google Analytics, no Facebook Pixel, no remarketing.",
    "FitWell utilise uniquement des cookies techniques essentiels au fonctionnement du site :": "FitWell only uses essential technical cookies necessary for the site to function:",
    "Propri\u00e9t\u00e9 intellectuelle": "Intellectual property",
    "Tous les textes, articles, recettes, descriptions d'exercices et plans d'entra\u00eenement pr\u00e9sents sur FitWell sont la propri\u00e9t\u00e9 de leurs auteurs respectifs.": "All texts, articles, recipes, exercise descriptions and training plans on FitWell are the property of their respective authors.",
    "Tu peux librement consulter et partager nos articles avec un lien retour. La reproduction commerciale ou la republication sans accord est interdite.": "You can freely read and share our articles with a link back. Commercial reproduction or republishing without agreement is prohibited.",
    "Les images proviennent de Unsplash sous licence libre, ou ont \u00e9t\u00e9 g\u00e9n\u00e9r\u00e9es sp\u00e9cifiquement pour ce site.": "Images come from Unsplash under free license, or were generated specifically for this site.",
    "Avertissement m\u00e9dical important": "Important medical disclaimer",
    "FitWell n'est pas un service m\u00e9dical. Nos contenus sont \u00e9ducatifs, pas th\u00e9rapeutiques.": "FitWell is not a medical service. Our content is educational, not therapeutic.",
    "Avant de commencer un nouveau programme sportif ou nutritionnel :": "Before starting a new fitness or nutrition program:",
    "Consulte ton m\u00e9decin si tu as une condition m\u00e9dicale (diab\u00e8te, hypertension, etc.)": "Consult your doctor if you have a medical condition (diabetes, hypertension, etc.)",
    "Demande l'avis d'un kin\u00e9sith\u00e9rapeute si tu as des douleurs articulaires": "Ask a physiotherapist if you have joint pain",
    "Va voir un nutritionniste pour les r\u00e9gimes sp\u00e9cifiques": "See a nutritionist for specific diets",
    "Arr\u00eate imm\u00e9diatement et consulte en cas de douleur aigu\u00eb": "Stop immediately and consult in case of acute pain",
    "FitWell d\u00e9cline toute responsabilit\u00e9 en cas de blessure cons\u00e9cutive \u00e0 une mauvaise application des conseils. Le sport doit toujours \u00eatre pratiqu\u00e9 avec bon sens et progression.": "FitWell disclaims all responsibility for injury resulting from misapplication of advice. Sport should always be practiced with common sense and progression.",
    "Limites de responsabilit\u00e9": "Liability limits",
    "FitWell est fourni \u00ab\u202ftel quel\u202f\u00bb. Bien que nous mettions tout en \u0153uvre pour publier des informations fiables et v\u00e9rifi\u00e9es, nous ne pouvons garantir leur exactitude absolue ni leur applicabilit\u00e9 \u00e0 ta situation personnelle.": "FitWell is provided \"as is\". Although we make every effort to publish reliable and verified information, we cannot guarantee its absolute accuracy or applicability to your personal situation.",
    "Le service peut \u00eatre indisponible temporairement pour maintenance. Nous nous effor\u00e7ons de minimiser ces interruptions.": "The service may be temporarily unavailable for maintenance. We strive to minimize these interruptions.",
    "Une question juridique, un signalement, une demande de suppression de donn\u00e9es, ou simplement envie de discuter\u202f?": "A legal question, a report, a data deletion request, or just want to chat?",
    "Notre \u00e9quipe r\u00e9pond sous 72 heures ouvr\u00e9es.": "Our team responds within 72 business hours.",
    "Derni\u00e8re mise \u00e0 jour : avril 2026": "Last updated: April 2026",
    "Cookies": "Cookies",

    # Admin
    "Surveillance temps r\u00e9el des utilisateurs": "Real-time user monitoring",
    "En ligne": "Online",
    "Actifs aujourd'hui": "Active today",
    "V\u00e9rifi\u00e9s": "Verified",
    "Masqu\u00e9s": "Hidden",
    "Rechercher par nom, email ou IP\u2026": "Search by name, email or IP\u2026",
    "Afficher masqu\u00e9s": "Show hidden",
    "Filtrer": "Filter",
    "Utilisateur": "User",
    "Statut": "Status",
    "Logins": "Logins",
    "Inscrit le": "Joined on",
    "Masquer": "Hide",
    "Supprimer d\u00e9finitivement cet utilisateur ?": "Permanently delete this user?",
    "Voir les User-Agents (informations techniques)": "View User-Agents (technical information)",
    "Admin Panel": "Admin Panel",

    # Footer / nav
    "Mon Espace": "My Space",
    "\u00c0 propos": "About",
    "Avertissement": "Disclaimer",
    "Articles & conseils": "Articles & advice",
    "ton alli\u00e9": "your ally",
    "Le savoir,": "Knowledge,",
    "Bienvenue dans la biblioth\u00e8que de FitWell. Ici, tu trouves des articles \u00e9crits par des passionn\u00e9s qui pratiquent le sport et la nutrition tous les jours.": "Welcome to FitWell's library. Here you find articles written by passionate people who practice sport and nutrition every day.",
    "Pas de blabla, pas de promesses miracles. Chaque article r\u00e9pond \u00e0 une question concr\u00e8te : comment progresser sans se blesser, comment manger sans se priver, comment rester motiv\u00e9 m\u00eame quand c'est dur. Lis, applique, progresse.": "No fluff, no miracle promises. Each article answers a concrete question: how to progress without injury, how to eat without depriving yourself, how to stay motivated even when it's hard. Read, apply, progress.",
    "Biblioth\u00e8que d'exercices": "Exercise library",
    "Plus de 100 exercices d\u00e9taill\u00e9s, class\u00e9s par groupe musculaire et niveau. Que tu sois d\u00e9butant complet ou pratiquant avanc\u00e9, tu trouveras toujours du nouveau \u00e0 apprendre.": "Over 100 detailed exercises, sorted by muscle group and level. Whether you're a complete beginner or an advanced practitioner, you'll always find something new to learn.",
    "Chaque exercice est expliqu\u00e9 : muscles cibl\u00e9s, technique correcte, erreurs courantes \u00e0 \u00e9viter. Filtre par muscle pour construire tes propres s\u00e9ances ou explore par difficult\u00e9 pour progresser \u00e0 ton rythme.": "Each exercise is explained: target muscles, correct technique, common mistakes to avoid. Filter by muscle to build your own sessions or explore by difficulty to progress at your own pace.",
    "Bien manger n'est pas se priver. C'est nourrir ton corps avec ce dont il a besoin pour fonctionner au mieux : \u00e9nergie stable, r\u00e9cup\u00e9ration efficace, plaisir intact.": "Eating well is not depriving yourself. It's feeding your body what it needs to function at its best: stable energy, effective recovery, intact pleasure.",
    "Toutes nos recettes affichent leurs valeurs nutritionnelles (calories, prot\u00e9ines, glucides, lipides). Filtre par cat\u00e9gorie pour trouver ton repas du jour : petit-d\u00e9j \u00e9nergisant, plat principal complet, snack pr\u00e9-entra\u00eenement, shake de r\u00e9cup\u00e9ration.": "All our recipes show their nutritional values (calories, protein, carbs, fats). Filter by category to find your meal of the day: energizing breakfast, complete main course, pre-workout snack, recovery shake.",
    "Mange": "Eat",
    "intelligent": "smart",

    # Profile / delete
    "Cette action est d\u00e9finitive et irr\u00e9versible": "This action is final and irreversible",
    "Ce qui sera supprim\u00e9": "What will be deleted",
    "Ton profil et tes informations": "Your profile and information",
    "Tes articles, commentaires et likes": "Your articles, comments and likes",
    "Tes plans bien-\u00eatre et historiques d'entra\u00eenement": "Your wellness plans and training history",
    "Toutes tes donn\u00e9es associ\u00e9es": "All your associated data",
    "Cette action ne peut pas \u00eatre annul\u00e9e. Aucune restauration possible.": "This action cannot be undone. No restoration possible.",
    "Supprimer d\u00e9finitivement": "Delete permanently",
    "Tape exactement SUPPRIMER pour confirmer.": "Type exactly DELETE to confirm.",

    # Onboarding
    "Sant\u00e9 & \u00c9nergie": "Health & Energy",
    "Continuer": "Continue",
    "Quelle place souhaites-tu accorder \u00e0 ton bien-\u00eatre ?": "What place do you want to give to your well-being?",
    "Calme": "Calm",
    "Journ\u00e9es de bureau, peu de mouvement": "Office days, little movement",
    "R\u00e9gulier": "Regular",
    "Donn\u00e9es": "Data",
    "Tes m\u00e9triques personnelles pour une exp\u00e9rience sur-mesure": "Your personal metrics for a tailored experience",
    "Bienvenue": "Welcome",
    "Pr\u00eat pour ta": "Ready for your",
    "M\u00e9tamorphose": "Metamorphosis",

    # Auth
    "S\u00e9curise ton acc\u00e8s exclusif avec un nouveau mot de passe.": "Secure your exclusive access with a new password.",
    "Acc\u00e8s Priv\u00e9": "Private Access",
    "l'Aventure": "the Adventure",
    "Rejoins l'\u00e9lite et transforme ton quotidien d\u00e8s aujourd'hui": "Join the elite and transform your daily life today",
    "En t'inscrivant, tu fais le choix d'une transformation sans limite.": "By signing up, you choose a transformation without limits.",

    # Dashboard / planner
    "Ton mouvement, ton \u00e9quilibre.": "Your movement, your balance.",
    "Strat\u00e9gie": "Strategy",
    "Ton architecture sur-mesure pour une vie plus forte": "Your tailored architecture for a stronger life",
    "Ma Strat\u00e9gie de Vie": "My Life Strategy",
    "Action & Mouvement": "Action & Movement",
    "Focus": "Focus",
    "Tes s\u00e9ances": "Your sessions",
    "Carburant & Plaisir": "Fuel & Pleasure",
    "Lecture de ton Potentiel": "Reading your Potential",
    "Repos": "Rest",
    "Style de vie": "Lifestyle",
    "IMC": "BMI",
    "Red\u00e9finir ma Strat\u00e9gie": "Redefine my Strategy",
    "Mon Historique d'\u00c9volution": "My Evolution History",
    "Forger ma Strat\u00e9gie": "Forge my Strategy",
    "Quelques m\u00e9triques pour une architecture sur-mesure.": "A few metrics for a tailored architecture.",
    "Univers": "Universe",
    "Ton \u00e9volution, tes victoires, ton h\u00e9ritage quotidien.": "Your evolution, your victories, your daily legacy.",
    "Vers le niveau": "Toward level",
    "Fitness": "Fitness",
    "Optimiser": "Optimize",
    "Ton \u00e9quilibre et ta nutrition sur-mesure": "Your tailored balance and nutrition",
    "Propulser": "Propel",
    "Tes outils de mesure et de performance": "Your measurement and performance tools",
    "Mes Succ\u00e8s": "My Successes",
    "\u00c9nergie (Prot)": "Energy (Prot)",
    "Carburant (Glu)": "Fuel (Carb)",
    "Structure (Lip)": "Structure (Fat)",
    "Optimise tes r\u00e9sultats avec un plan nutritionnel sur-mesure.": "Optimize your results with a tailored nutrition plan.",
    "Personnaliser mon plan": "Customize my plan",
    "Ingr\u00e9dients": "Ingredients",
    "Mes": "My",
    "La pr\u00e9cision au service de ta progression": "Precision serving your progress",
    "Indice de Forme": "Fitness Index",
    "Ton r\u00e9sultat": "Your result",
    "Mes Besoins": "My Needs",
    "Calcule tes besoins \u00e9nerg\u00e9tiques pour une transformation ma\u00eetris\u00e9e.": "Calculate your energy needs for a controlled transformation.",
    "Calme (bureau)": "Calm (office)",
    "Actif (1-3 s\u00e9ances/sem)": "Active (1-3 sessions/wk)",
    "Tr\u00e8s actif (4-5 s\u00e9ances/sem)": "Very active (4-5 sessions/wk)",
    "Athl\u00e8te (6+ s\u00e9ances/sem)": "Athlete (6+ sessions/wk)",
    "Focus & Temps": "Focus & Time",
    "Veuillez remplir tous les champs.": "Please fill in all fields.",
    "Maigreur": "Underweight",
    "Corpulence normale": "Normal weight",
    "Ob\u00e9sit\u00e9": "Obesity",

    # Workout
    "D\u00e9tails S\u00e9ance": "Session Details",
    "Mes Notes": "My Notes",
    "Dur\u00e9e": "Duration",
    "Total S\u00e9ries": "Total Sets",
    "Analyse de la Performance": "Performance Analysis",
    "S\u00e9rie": "Set",
    "Reps": "Reps",
    "Charge": "Load",
    "Nouvelle S\u00e9ance": "New Session",
    "Historique Entra\u00eenements": "Workout History",
    "Retrace ton parcours et visualise chaque victoire vers ton sommet": "Track your journey and visualize each victory toward your peak",
    "Volume par s\u00e9ance": "Volume per session",
    "Derni\u00e8res Performances": "Latest Performances",
    "Nouvelle Ascension": "New Ascent",
    "D\u00e9tails": "Details",
    "Volume (kg)": "Volume (kg)",
    "Nouvelle S\u00e9rie": "New Set",
    "Ton Mouvement": "Your Movement",
    "Choisir un mouvement": "Choose a movement",
    "Charge (kg)": "Load (kg)",
    "Valider la s\u00e9rie": "Validate the set",
    "S\u00e9ries R\u00e9alis\u00e9es": "Sets Completed",
    "Ta progression commence ici": "Your progress starts here",
    "Finaliser ma Performance": "Finalize my Performance",
    "S\u00e9rie ajout\u00e9e !": "Set added!",
    "Terminer la s\u00e9ance maintenant ?": "End the session now?",
    "Lib\u00e8re ton plein potentiel. Ta s\u00e9ance commence maintenant.": "Unleash your full potential. Your session starts now.",
    "Notes personnelles": "Personal notes",
    "Entrer dans le Studio": "Enter the Studio",
    "Studio Live - Ton Mouvement": "Live Studio - Your Movement",
    "Mode Vie : Activ\u00e9": "Life Mode: Activated",
    "Pr\u00eat pour ton mouvement.": "Ready for your movement.",
    "Valid\u00e9e": "Validated",
    "Ton ascension continue. F\u00e9licitations.": "Your ascent continues. Congratulations.",
    "Post-Workout Id\u00e9al": "Ideal Post-Workout",
    "Optimis\u00e9 pour ta r\u00e9cup\u00e9ration et ton \u00e9nergie quotidienne.": "Optimized for your recovery and daily energy.",
    "Voir la recette": "View recipe",
    "Configure ton exp\u00e9rience et d\u00e9passe tes limites d\u00e8s maintenant": "Configure your experience and exceed your limits right now",
    "Ta S\u00e9lection de Mouvements": "Your Movement Selection",

    # Messages flash
    "Impossible de masquer un autre super-utilisateur.": "Cannot hide another superuser.",
    "masqu\u00e9": "hidden",
    "r\u00e9affich\u00e9": "shown again",
    "L'utilisateur %(u)s a \u00e9t\u00e9 %(s)s.": "User %(u)s has been %(s)s.",
    "Impossible de supprimer un autre super-utilisateur.": "Cannot delete another superuser.",
    "L'utilisateur %(u)s a \u00e9t\u00e9 supprim\u00e9 d\u00e9finitivement.": "User %(u)s has been permanently deleted.",
    "Heureux de te rencontrer ! Ton compte est pr\u00eat.": "Nice to meet you! Your account is ready.",
    "Tes r\u00e9glages ont \u00e9t\u00e9 enregistr\u00e9s ! \u2728": "Your settings have been saved! \u2728",
    "Ton nouveau mot de passe est actif. Ta s\u00e9curit\u00e9 est assur\u00e9e. \ud83d\udd12": "Your new password is active. Your security is ensured. \ud83d\udd12",
    "Oups, v\u00e9rifie les informations saisies.": "Oops, check the information entered.",
    "Ton avis a \u00e9t\u00e9 partag\u00e9 ! \u2728": "Your review has been shared! \u2728",
    "Bien jou\u00e9 ! Ta journ\u00e9e est enregistr\u00e9e. +20 d'\u00e9nergie": "Well done! Your day is logged. +20 energy",
    "F\u00e9licitations ! Ton \u00e9quilibre est pr\u00eat. +%(xp)s": "Congratulations! Your balance is ready. +%(xp)s",
    "Ton programme est pr\u00eat ! +100 d'\u00e9nergie": "Your program is ready! +100 energy",
    "C'est fait ! +%(xp)s": "Done! +%(xp)s",
    "Session Studio termin\u00e9e": "Studio session completed",
    "Bien jou\u00e9 ! +%(xp)s d'\u00e9nergie": "Well done! +%(xp)s energy",
    "Vous avez d\u00e9j\u00e0 une s\u00e9ance en cours. Terminez-la d'abord.": "You already have an ongoing session. Finish it first.",
    "C'est parti ! Profite de ton mouvement ! \u2728": "Let's go! Enjoy your movement! \u2728",
    "Cette s\u00e9ance est d\u00e9j\u00e0 termin\u00e9e.": "This session is already completed.",
    "S\u00e9ance termin\u00e9e avec succ\u00e8s ! \ud83c\udf89": "Session completed successfully! \ud83c\udf89",
    "Ton compte %(u)s a \u00e9t\u00e9 supprim\u00e9 d\u00e9finitivement. \u00c0 bient\u00f4t peut-\u00eatre.": "Your account %(u)s has been permanently deleted. See you maybe.",
    "Erreur lors de l'ajout de la s\u00e9rie": "Error adding the set",
    "Erreur lors de la finalisation": "Error during finalization",
    "Tape \"SUPPRIMER\" pour confirmer": "Type \"DELETE\" to confirm",
    "Tes objectifs du jour, ton \u00e9tat d'esprit, ce que tu ressens...": "Your goals for today, your mindset, how you feel...",
    "C'est l'instant pour donner le meilleur de toi.": "It's the moment to give your best.",

    # Long paragraphs - Home
    "FitWell r\u00e9unit deux id\u00e9es simples : <strong>Fit</strong>, \u00eatre en forme physiquement, et <strong>Well</strong>, se sentir bien mentalement. C'est un site de sport et de bien-\u00eatre qui t'accompagne jour apr\u00e8s jour avec des conseils concrets, des entra\u00eenements guid\u00e9s et une nutrition intelligente.": "FitWell brings together two simple ideas: <strong>Fit</strong>, being in physical shape, and <strong>Well</strong>, feeling mentally good. It's a sport and wellness site that supports you day after day with concrete advice, guided workouts and smart nutrition.",
    "Pas de promesses miracles. Juste des m\u00e9thodes \u00e9prouv\u00e9es, du contenu cr\u00e9\u00e9 par des passionn\u00e9s, et des outils qui marchent vraiment pour am\u00e9liorer ta vie, un petit pas \u00e0 la fois.": "No miracle promises. Just proven methods, content created by passionate people, and tools that really work to improve your life, one small step at a time.",
    "Trop de gens abandonnent le sport parce qu'ils ne savent pas par o\u00f9 commencer, ils se blessent, ou ils n'ont pas le temps. FitWell existe pour r\u00e9soudre \u00e7a.": "Too many people give up on sport because they don't know where to start, they get injured, or they don't have time. FitWell exists to solve that.",
    "Ici, tu trouves des exercices expliqu\u00e9s clairement, des recettes \u00e9quilibr\u00e9es pour manger sans te priver, des plans d'entra\u00eenement adapt\u00e9s \u00e0 ton niveau, et des articles qui d\u00e9mystifient ce qui marche vraiment pour \u00eatre en bonne sant\u00e9.": "Here, you find clearly explained exercises, balanced recipes to eat without deprivation, training plans adapted to your level, and articles that demystify what really works for good health.",
    "Parce que se sentir bien dans son corps change tout : ton \u00e9nergie, ton sommeil, ton humeur, ta confiance.": "Because feeling good in your body changes everything: your energy, your sleep, your mood, your confidence.",
    "Une vie saine repose sur trois piliers indissociables. N\u00e9gliger un seul d\u00e9s\u00e9quilibre tout le reste. C'est pourquoi nous t'accompagnons sur chacun.": "A healthy life rests on three inseparable pillars. Neglecting just one unbalances everything else. That's why we support you on each one.",
    "Pas besoin de 2h de salle par jour. 30 minutes cibl\u00e9es, 3 fois par semaine, changent d\u00e9j\u00e0 ta vie. On t'apprend les bons mouvements.": "No need for 2 hours of gym per day. 30 targeted minutes, 3 times a week, already change your life. We teach you the right movements.",
    "Fini les r\u00e9gimes restrictifs qui ne tiennent pas. Nos recettes sont simples, compl\u00e8tes, et rassasiantes. Le plaisir de manger, sans la culpabilit\u00e9.": "No more restrictive diets that don't last. Our recipes are simple, complete, and filling. The pleasure of eating, without guilt.",
    "Le savoir est ton meilleur entra\u00eeneur. Nos articles d\u00e9cryptent la science du sport, la nutrition, la r\u00e9cup\u00e9ration, et le mental.": "Knowledge is your best coach. Our articles decode the science of sport, nutrition, recovery, and mindset.",
    "Tu n'as pas besoin de tout r\u00e9volutionner d'un coup. Adopte ces 4 habitudes simples et tu sentiras la diff\u00e9rence en moins de 30 jours.": "You don't need to revolutionize everything at once. Adopt these 4 simple habits and you'll feel the difference in less than 30 days.",
    "Marche, v\u00e9lo, \u00e9tirements, mont\u00e9e d'escaliers. Peu importe la forme, l'important c'est la r\u00e9gularit\u00e9. Ton corps est fait pour le mouvement.": "Walking, biking, stretching, climbing stairs. Whatever the form, what matters is regularity. Your body is made for movement.",
    "80 %% des gens sont d\u00e9shydrat\u00e9s sans le savoir. Fatigue, faim, mal de t\u00eate : souvent c'est un simple manque d'eau. Garde une bouteille avec toi.": "80%% of people are dehydrated without knowing it. Fatigue, hunger, headaches: often it's a simple lack of water. Keep a bottle with you.",
    "C'est pendant la nuit que ton corps se r\u00e9pare, que ton esprit consolide ce que tu as appris, que tes muscles grandissent. Le sommeil n'est pas une perte de temps.": "It's at night that your body repairs, your mind consolidates what you've learned, your muscles grow. Sleep is not a waste of time.",
    "Fruits, l\u00e9gumes, viandes, poissons, c\u00e9r\u00e9ales compl\u00e8tes, l\u00e9gumineuses. Si \u00e7a a \u00e9t\u00e9 transform\u00e9 en usine, c'est rarement un ami. Simplifie ton assiette.": "Fruits, vegetables, meat, fish, whole grains, legumes. If it was processed in a factory, it's rarely a friend. Simplify your plate.",
    "On ne te vend pas de compl\u00e9ments miracles ni de brul\u00e9urs de graisse. Uniquement des conseils honn\u00eates.": "We don't sell you miracle supplements or fat burners. Only honest advice.",
    "D\u00e9butant complet ou sportif exp\u00e9riment\u00e9, tu trouveras toujours du contenu adapt\u00e9 \u00e0 ton niveau et tes objectifs.": "Complete beginner or experienced athlete, you'll always find content adapted to your level and goals.",
    "Chaque conseil s'appuie sur des \u00e9tudes reconnues et l'exp\u00e9rience de professionnels du sport et de la sant\u00e9.": "Each piece of advice is based on recognized studies and the experience of sport and health professionals.",
    "Cr\u00e9e ton compte sans payer. Acc\u00e8de \u00e0 la biblioth\u00e8que, aux recettes, au blog, \u00e0 ton planning personnalis\u00e9.": "Create your account without paying. Access the library, recipes, blog, and your personalized planning.",
    "Chaque journ\u00e9e pass\u00e9e \u00e0 attendre est une journ\u00e9e perdue. Rejoins des milliers de personnes qui ont d\u00e9cid\u00e9 de reprendre leur sant\u00e9 en main avec FitWell. C'est gratuit, c'est simple, et \u00e7a peut changer ta vie.": "Every day spent waiting is a lost day. Join thousands of people who decided to take their health back in hand with FitWell. It's free, it's simple, and it can change your life.",
    "Ton compagnon quotidien pour une vie plus saine, plus forte et plus sereine.": "Your daily companion for a healthier, stronger and more serene life.",

    # About long paragraphs
    "FitWell n'est pas un site de plus sur le fitness. C'est une plateforme con\u00e7ue par des passionn\u00e9s, pour ceux qui veulent prendre soin de leur corps et de leur esprit, sans se faire arnaquer ni se faire mal.": "FitWell is not just another fitness site. It's a platform designed by passionate people, for those who want to take care of their body and mind, without getting scammed or hurt.",
    "On vit dans un monde o\u00f9 l'industrie du fitness vend du r\u00eave : des packs de prot\u00e9ines miracles, des programmes en 21 jours qui transforment ton corps, des influenceurs qui pr\u00e9tendent avoir trouv\u00e9 LE secret.": "We live in a world where the fitness industry sells a dream: miracle protein packs, 21-day programs that transform your body, influencers who claim to have found THE secret.",
    "La v\u00e9rit\u00e9, c'est qu'il n'y a pas de secret. Juste des principes simples : bouger r\u00e9guli\u00e8rement, manger des aliments entiers, dormir suffisamment, g\u00e9rer son stress.": "The truth is there is no secret. Just simple principles: move regularly, eat whole foods, sleep enough, manage stress.",
    "Notre mission est de te donner ces principes, expliqu\u00e9s clairement, sans bullshit, gratuitement.": "Our mission is to give you these principles, clearly explained, without bullshit, for free.",
    "FitWell est n\u00e9 d'un constat simple : trop de gens veulent se mettre au sport mais abandonnent dans les premi\u00e8res semaines.": "FitWell was born from a simple observation: too many people want to start sport but give up in the first weeks.",
    "Pourquoi ? Parce qu'ils ne savent pas par o\u00f9 commencer, parce qu'ils se blessent \u00e0 cause d'une mauvaise technique, parce qu'ils suivent des r\u00e9gimes impossibles \u00e0 tenir, ou parce qu'ils n'ont pas le temps de tout comprendre eux-m\u00eames.": "Why? Because they don't know where to start, because they get injured due to bad technique, because they follow impossible diets, or because they don't have time to understand everything themselves.",
    "Nous avons cr\u00e9\u00e9 FitWell pour rassembler en un seul endroit ce qu'il faut savoir : les bons exercices, les recettes saines, les principes de r\u00e9cup\u00e9ration, et les conseils mentaux.": "We created FitWell to gather in one place what you need to know: the right exercises, healthy recipes, recovery principles, and mental advice.",
    "Tout est gratuit. Tout est accessible. Tout est expliqu\u00e9 pour les d\u00e9butants, mais assez pr\u00e9cis pour les sportifs avanc\u00e9s.": "Everything is free. Everything is accessible. Everything is explained for beginners, but precise enough for advanced athletes.",
    "Quatre principes qui guident chaque ligne de contenu publi\u00e9e sur FitWell.": "Four principles that guide every line of content published on FitWell.",
    "Si quelque chose ne marche pas, on te le dit. Si une \u00e9tude est faible, on te le pr\u00e9cise. On ne vendra jamais de compl\u00e9ment alimentaire ni de programme \u00e0 297\u20ac qui te promet la lune.": "If something doesn't work, we tell you. If a study is weak, we say so. We will never sell food supplements or a 297\u20ac program promising you the moon.",
    "Le fitness n'est pas compliqu\u00e9. C'est l'industrie qui le rend compliqu\u00e9 pour te vendre des solutions. Nos contenus sont \u00e9crits pour \u00eatre compris en 5 minutes, applicables tout de suite.": "Fitness is not complicated. The industry makes it complicated to sell you solutions. Our content is written to be understood in 5 minutes, applicable right away.",
    "Que tu sois jeune ou senior, d\u00e9butant complet ou athl\u00e8te exp\u00e9riment\u00e9, en surpoids ou maigre, FitWell est pour toi. Le sport ne devrait pas \u00eatre r\u00e9serv\u00e9 \u00e0 une \u00e9lite.": "Whether you're young or senior, complete beginner or experienced athlete, overweight or thin, FitWell is for you. Sport should not be reserved for an elite.",
    "On ne cherche pas \u00e0 te faire perdre 10 kilos en 3 semaines. On veut te construire une sant\u00e9 qui dure 50 ans. Chaque conseil est pens\u00e9 pour \u00eatre tenable durablement.": "We don't aim to make you lose 10 kilos in 3 weeks. We want to build you health that lasts 50 years. Each piece of advice is designed to be sustainable.",
    "Nos articles ne sont pas g\u00e9n\u00e9r\u00e9s \u00e0 la cha\u00eene. Ils sont \u00e9crits par des passionn\u00e9s de sport et de nutrition qui appliquent eux-m\u00eames ce qu'ils recommandent.": "Our articles are not mass-produced. They are written by sport and nutrition enthusiasts who apply themselves what they recommend.",
    "Pas de coach virtuel qui te juge. Tu choisis ce que tu lis, ce que tu fais, quand tu le fais. C'est ton parcours, on est juste l\u00e0 pour t'\u00e9clairer.": "No virtual coach to judge you. You choose what to read, what to do, when to do it. It's your journey, we're just here to enlighten you.",
    "FitWell s'enrichit chaque semaine de nouveaux articles, exercices, recettes. Inscris-toi gratuitement et reviens quand tu veux : il y aura toujours du nouveau contenu utile.": "FitWell enriches itself every week with new articles, exercises, recipes. Register for free and come back whenever you want: there will always be new useful content.",
    "Aucune information cach\u00e9e derri\u00e8re un paywall. Tout est gratuit, tout est document\u00e9, tout est partageable. Le savoir doit circuler.": "No information hidden behind a paywall. Everything is free, everything is documented, everything is shareable. Knowledge must circulate.",
    "Le changement vient de toi, pas de nous. Mais avec les bons conseils, les bonnes m\u00e9thodes, et un peu de constance, tu peux faire des choses incroyables. C'est pour \u00e7a que FitWell existe.": "Change comes from you, not from us. But with the right advice, the right methods, and a bit of consistency, you can do incredible things. That's why FitWell exists.",

    # Other long
    "Auto-rafra\u00eechi \u00e0 chaque chargement. Indicateur vert = session active maintenant.": "Auto-refreshed on each load. Green indicator = session active now.",
    "Ne te contente pas de lire. Applique ces conseils et commence ta transformation d\u00e8s aujourd'hui avec nos programmes sur-mesure.": "Don't just read. Apply these tips and start your transformation today with our tailored programs.",
    "Acc\u00e8de \u00e0 l'int\u00e9gralit\u00e9 de notre Studio et commence ta transformation d\u00e8s aujourd'hui.": "Access our full Studio and start your transformation today.",
    "Oublie les r\u00e9gimes, adopte un style de vie. Configurons ton acc\u00e8s exclusif en quelques secondes.": "Forget diets, adopt a lifestyle. Let's set up your exclusive access in seconds.",
    "Ton mot de passe est mis \u00e0 jour. Reprends ton ascension vers tes objectifs d\u00e8s maintenant.": "Your password is updated. Resume your ascent toward your goals right now.",
    "Pour choisir un nouveau mot de passe, clique simplement sur le lien ci-dessous :": "To choose a new password, simply click on the link below:",
    "Pas d'inqui\u00e9tude, entre ton email pour recevoir un lien de r\u00e9initialisation.": "Don't worry, enter your email to receive a reset link.",
    "Rejoins l'\u00e9lite et d\u00e9bloque plus de 100 recettes optimis\u00e9es pour ton succ\u00e8s.": "Join the elite and unlock over 100 recipes optimized for your success.",
    "Tu ne peux pas te supprimer toi-m\u00eame via le dashboard admin. Utilise la page profil.": "You cannot delete yourself via the admin dashboard. Use the profile page.",
    "Salut %(username)s,\n\nHeureux de te compter parmi nous. Ton voyage vers un meilleur quotidien commence maintenant.\n\nAcc\u00e8de \u00e0 ton espace : %(url)s\n\n\u00c0 tr\u00e8s vite,\nL'\u00e9quipe FitWell": "Hi %(username)s,\n\nGlad to have you with us. Your journey toward a better daily life starts now.\n\nAccess your space: %(url)s\n\nSee you very soon,\nThe FitWell team",
    "Le super-utilisateur ne peut pas se supprimer via cette page (s\u00e9curit\u00e9).": "The superuser cannot delete themselves via this page (security).",
    "S\u00e9ance termin\u00e9e avec succ\u00e8s ! \ud83c\udf89": "Session completed successfully! \ud83c\udf89",
    "Ton nouveau mot de passe est actif. Ta s\u00e9curit\u00e9 est assur\u00e9e. \ud83d\udd12": "Your new password is active. Your security is ensured. \ud83d\udd12",

    # Final missing strings (exact match with .po)
    "S\u00e9ance termin\u00e9e avec succ\u00e8s\u202f! \U0001f389": "Session completed successfully! \U0001f389",
    "Ton nouveau mot de passe est actif. Ta s\u00e9curit\u00e9 est assur\u00e9e. \U0001f512": "Your new password is active. Your security is ensured. \U0001f512",
    "Tes objectifs du jour, ton \u00e9tat d'esprit...": "Your goals for today, your mindset...",
    "Une question juridique, un signalement, une demande de suppression de donn\u00e9es, ou simplement envie de discuter ?": "A legal question, a report, a data deletion request, or just want to chat?",
    "FitWell est fourni \u00ab\u00a0tel quel\u00a0\u00bb. Bien que nous mettions tout en \u0153uvre pour publier des informations fiables et v\u00e9rifi\u00e9es, nous ne pouvons garantir leur exactitude absolue ni leur applicabilit\u00e9 \u00e0 ta situation personnelle.": "FitWell is provided \"as is\". Although we make every effort to publish reliable and verified information, we cannot guarantee its absolute accuracy or applicability to your personal situation.",
    "Une petite erreur de parcours. Notre \u00e9quipe travaille \u00e0 r\u00e9tablir l'\u00e9quilibre. Merci de ta patience.": "A small bump on the road. Our team is working to restore balance. Thank you for your patience.",
    "La page que tu cherches a pris un autre chemin. Repartons du bon pied pour ton prochain mouvement.": "The page you're looking for has taken another path. Let's start fresh for your next move.",
    "FitWell est fourni \u00ab tel quel \u00bb. Bien que nous mettions tout en \u0153uvre pour publier des informations fiables et v\u00e9rifi\u00e9es, nous ne pouvons garantir leur exactitude absolue ni leur applicabilit\u00e9 \u00e0 ta situation personnelle.": "FitWell is provided \"as is\". Although we make every effort to publish reliable and verified information, we cannot guarantee its absolute accuracy or applicability to your personal situation.",
    "S\u00e9ance termin\u00e9e avec succ\u00e8s ! \U0001f389": "Session completed successfully! \U0001f389",
}


def parse_po_blocks(content: str):
    """Parse .po into a list of blocks: each block is (start_line, end_line, msgid, msgstr_lines)."""
    lines = content.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid ') or line.startswith('msgid\t'):
            block_start = i
            # collect msgid (handles continuation strings starting with ")
            msgid_parts = [line[len('msgid '):]]
            j = i + 1
            while j < len(lines) and lines[j].startswith('"'):
                msgid_parts.append(lines[j])
                j += 1
            # j now points to msgstr (or msgid_plural which we skip for simplicity)
            if j < len(lines) and lines[j].startswith('msgstr '):
                msgstr_start = j
                msgstr_parts = [lines[j][len('msgstr '):]]
                k = j + 1
                while k < len(lines) and lines[k].startswith('"'):
                    msgstr_parts.append(lines[k])
                    k += 1
                # Decode msgid value
                msgid_str = ''.join(_decode_po_string(p) for p in msgid_parts)
                msgstr_str = ''.join(_decode_po_string(p) for p in msgstr_parts)
                blocks.append({
                    'msgid_start': block_start,
                    'msgstr_start': msgstr_start,
                    'msgstr_end': k - 1,
                    'msgid': msgid_str,
                    'msgstr': msgstr_str,
                })
                i = k
                continue
        i += 1
    return blocks, lines


def _decode_po_string(s: str) -> str:
    """Strip surrounding quotes and unescape."""
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')


def _encode_po_string(s: str) -> str:
    """Escape and wrap in quotes."""
    s = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return f'"{s}"'


def apply_translations(po_path: Path) -> tuple[int, int, list]:
    content = po_path.read_text(encoding='utf-8')
    blocks, lines = parse_po_blocks(content)

    filled = 0
    still_empty = []
    # Process from end to start to preserve line numbers
    for block in reversed(blocks):
        if block['msgid'] == '':  # header
            continue
        if block['msgstr'] != '':
            continue
        # Empty translation - try dictionary
        if block['msgid'] in TRANSLATIONS:
            translation = TRANSLATIONS[block['msgid']]
            # Replace lines from msgstr_start to msgstr_end with single line
            new_msgstr_line = 'msgstr ' + _encode_po_string(translation)
            del lines[block['msgstr_start']:block['msgstr_end'] + 1]
            lines.insert(block['msgstr_start'], new_msgstr_line)
            filled += 1
        else:
            still_empty.append(block['msgid'][:100])

    po_path.write_text('\n'.join(lines), encoding='utf-8')
    return filled, len(still_empty), still_empty


if __name__ == '__main__':
    base = Path(__file__).resolve().parent.parent
    en_po = base / 'locale' / 'en' / 'LC_MESSAGES' / 'django.po'
    filled, empty_count, empty_list = apply_translations(en_po)
    print(f'\u2705 EN: {filled} translations filled')
    print(f'   Still empty: {empty_count}')
    if empty_list:
        print('\n   Remaining missing:')
        for s in empty_list[:30]:
            print(f'     {repr(s)}')
