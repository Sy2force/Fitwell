"""
Applique les traductions EN au fichier .po EN pour toutes les msgstr vides.
Le dictionnaire est curated manuellement pour une qualit\u00e9 \u00e9ditoriale.

Usage:
    python3 scripts/translate_po.py
"""
import re
from pathlib import Path

# Dictionnaire FR -> EN (curated, qualit\u00e9 \u00e9ditoriale)
TRANSLATIONS = {
    # === Page About ===
    "\u00c0 propos de nous": "About us",
    "Le sport accessible.": "Accessible fitness.",
    "Pour de vrai.": "For real.",
    "01.": "01.",
    "02.": "02.",
    "03.": "03.",
    "04.": "04.",
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
    "Notre engagement": "Our commitment",
    "Bienvenue sur FitWell": "Welcome to FitWell",
    "Mission, valeurs et histoire de FitWell": "FitWell's mission, values and story",
    "Le sport n'est pas une punition.": "Sport is not a punishment.",
    "C'est un cadeau que tu te fais.": "It's a gift you give yourself.",

    # === Home page ===
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
    "Trois piliers, un \u00e9quilibre": "Three pillars, one balance",
    "Pilier 1": "Pillar 1",
    "Pilier 2": "Pillar 2",
    "Pilier 3": "Pillar 3",

    # === Page Legal ===
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

    # === Admin panel ===
    "Admin": "Admin",
    "Panel": "Panel",
    "Surveillance temps r\u00e9el des utilisateurs": "Real-time user monitoring",
    "Total": "Total",
    "En ligne": "Online",
    "Actifs aujourd'hui": "Active today",
    "V\u00e9rifi\u00e9s": "Verified",
    "Staff": "Staff",
    "Masqu\u00e9s": "Hidden",
    "Rechercher par nom, email ou IP\u2026": "Search by name, email or IP\u2026",
    "Afficher masqu\u00e9s": "Show hidden",
    "Filtrer": "Filter",
    "Utilisateur": "User",
    "Statut": "Status",
    "IP": "IP",
    "Logins": "Logins",
    "Inscrit le": "Joined on",
    "Masquer": "Hide",
    "Supprimer d\u00e9finitivement cet utilisateur ?": "Permanently delete this user?",
    "Voir les User-Agents (informations techniques)": "View User-Agents (technical information)",
    "Admin Panel": "Admin Panel",

    # === Footer / nav ===
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

    # === Profile / delete ===
    "Cette action est d\u00e9finitive et irr\u00e9versible": "This action is final and irreversible",
    "Ce qui sera supprim\u00e9": "What will be deleted",
    "Ton profil et tes informations": "Your profile and information",
    "Tes articles, commentaires et likes": "Your articles, comments and likes",
    "Tes plans bien-\u00eatre et historiques d'entra\u00eenement": "Your wellness plans and training history",
    "Toutes tes donn\u00e9es associ\u00e9es": "All your associated data",
    "Cette action ne peut pas \u00eatre annul\u00e9e. Aucune restauration possible.": "This action cannot be undone. No restoration possible.",
    "Tape \\\"SUPPRIMER\\\" pour confirmer": "Type \\\"DELETE\\\" to confirm",
    "Supprimer d\u00e9finitivement": "Delete permanently",
    "Tape exactement SUPPRIMER pour confirmer.": "Type exactly DELETE to confirm.",
    "Ton compte %(u)s a \u00e9t\u00e9 supprim\u00e9 d\u00e9finitivement. \u00c0 bient\u00f4t peut-\u00eatre.": "Your account %(u)s has been permanently deleted. See you maybe.",

    # === Onboarding ===
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

    # === Auth ===
    "S\u00e9curise ton acc\u00e8s exclusif avec un nouveau mot de passe.": "Secure your exclusive access with a new password.",
    "Acc\u00e8s Priv\u00e9": "Private Access",
    "l'Aventure": "the Adventure",
    "Rejoins l'\u00e9lite et transforme ton quotidien d\u00e8s aujourd'hui": "Join the elite and transform your daily life today",
    "En t'inscrivant, tu fais le choix d'une transformation sans limite.": "By signing up, you choose a transformation without limits.",

    # === Dashboard / planner ===
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

    # === Workout ===
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
    "Erreur lors de l\\\\'ajout de la s\u00e9rie": "Error adding the set",
    "Terminer la s\u00e9ance maintenant ?": "End the session now?",
    "Erreur lors de la finalisation": "Error during finalization",
    "Lib\u00e8re ton plein potentiel. Ta s\u00e9ance commence maintenant.": "Unleash your full potential. Your session starts now.",
    "Notes personnelles": "Personal notes",
    "Tes objectifs du jour, ton \u00e9tat d\\\\'": "Your goals for today, your state of",
    "Entrer dans le Studio": "Enter the Studio",
    "Studio Live - Ton Mouvement": "Live Studio - Your Movement",
    "Mode Vie : Activ\u00e9": "Life Mode: Activated",
    "Pr\u00eat pour ton mouvement.": "Ready for your movement.",
    "Valid\u00e9e": "Validated",
    "Ton ascension continue. F\u00e9licitations.": "Your ascent continues. Congratulations.",
    "Post-Workout Id\u00e9al": "Ideal Post-Workout",
    "Optimis\u00e9 pour ta r\u00e9cup\u00e9ration et ton \u00e9nergie quotidienne.": "Optimized for your recovery and daily energy.",
    "Voir la recette": "View recipe",
    "C\\\\'": "C'",
    "Configure ton exp\u00e9rience et d\u00e9passe tes limites d\u00e8s maintenant": "Configure your experience and exceed your limits right now",
    "Ta S\u00e9lection de Mouvements": "Your Movement Selection",

    # === Messages flash / errors ===
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
    "FitWell": "FitWell",
    "Cr\u00e9er mon compte gratuit": "Create my free account",
    "Lire nos conseils": "Read our advice",
    "Rejoindre l'aventure (gratuit)": "Join the adventure (free)",
    "J'ai d\u00e9j\u00e0 un compte": "I already have an account",
}


def apply_translations(po_path: Path) -> tuple[int, int]:
    """Apply translations to .po file. Returns (filled, still_empty)."""
    text = po_path.read_text(encoding="utf-8")

    # Process line by line to find msgid -> msgstr pairs
    lines = text.split("\n")
    new_lines = []
    filled = 0
    still_empty = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        # Detect simple "msgid \"...\"" then "msgstr \"\""
        m = re.match(r'^msgid "(.*)"$', line)
        if m and i + 1 < len(lines):
            msgid_value = m.group(1)
            next_line = lines[i + 1]
            if next_line == 'msgstr ""':
                # Try to find a translation
                if msgid_value in TRANSLATIONS and msgid_value:
                    # Escape quotes in translation
                    translated = TRANSLATIONS[msgid_value].replace('"', '\\"')
                    new_lines.append(f'msgstr "{translated}"')
                    filled += 1
                    i += 2
                    continue
                elif msgid_value:
                    still_empty += 1
        i += 1

    po_path.write_text("\n".join(new_lines), encoding="utf-8")
    return filled, still_empty


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    en_po = base / "locale" / "en" / "LC_MESSAGES" / "django.po"
    if not en_po.exists():
        print(f"ERROR: {en_po} not found")
        raise SystemExit(1)
    filled, still_empty = apply_translations(en_po)
    print(f"\u2705 EN: {filled} translations filled, {still_empty} still empty")
    print(f"  Dictionary size: {len(TRANSLATIONS)}")
