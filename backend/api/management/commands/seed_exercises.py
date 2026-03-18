from django.core.management.base import BaseCommand
from api.models import Exercise

class Command(BaseCommand):
    help = 'Seeds the database with 100+ exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            # CHEST (Pectoraux) - 15 exercices
            {"name": "Pompes (Push-ups)", "muscle_group": "chest", "difficulty": "beginner", "description": "Exercice classique au poids du corps pour développer les pectoraux, triceps et épaules.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Développé Couché (Bench Press)", "muscle_group": "chest", "difficulty": "intermediate", "description": "Exercice roi pour la masse pectorale. Allongé sur un banc, poussez la barre vers le haut.", "equipment": "Barre + Banc", "image_url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800"},
            {"name": "Développé Incliné", "muscle_group": "chest", "difficulty": "intermediate", "description": "Cible le haut des pectoraux. Banc incliné à 30-45 degrés.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Développé Décliné", "muscle_group": "chest", "difficulty": "intermediate", "description": "Focus sur le bas des pectoraux. Banc décliné.", "equipment": "Barre + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Écarté Haltères", "muscle_group": "chest", "difficulty": "intermediate", "description": "Étirement maximal des pectoraux. Mouvement d'ouverture.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Dips Pectoraux", "muscle_group": "chest", "difficulty": "intermediate", "description": "Penchez-vous en avant pour cibler les pectoraux.", "equipment": "Barres parallèles", "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800"},
            {"name": "Pompes Diamant", "muscle_group": "chest", "difficulty": "intermediate", "description": "Mains rapprochées en forme de diamant. Focus triceps et centre pectoraux.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Pompes Déclinées", "muscle_group": "chest", "difficulty": "intermediate", "description": "Pieds surélevés pour augmenter l'intensité.", "equipment": "Poids du corps + Banc", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Cable Crossover", "muscle_group": "chest", "difficulty": "intermediate", "description": "Croisement de câbles pour une contraction maximale.", "equipment": "Machine à câbles", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Pec Deck (Butterfly)", "muscle_group": "chest", "difficulty": "beginner", "description": "Machine guidée pour isoler les pectoraux.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Développé Haltères", "muscle_group": "chest", "difficulty": "intermediate", "description": "Plus grande amplitude que la barre. Meilleur étirement.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Pompes Pliométriques", "muscle_group": "chest", "difficulty": "advanced", "description": "Pompes explosives avec décollement des mains. Puissance.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Pullover Haltère", "muscle_group": "chest", "difficulty": "intermediate", "description": "Étirement de la cage thoracique. Travaille aussi le dos.", "equipment": "Haltère + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Pompes Archer", "muscle_group": "chest", "difficulty": "advanced", "description": "Pompes unilatérales. Un bras travaille plus que l'autre.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Landmine Press", "muscle_group": "chest", "difficulty": "intermediate", "description": "Poussée avec barre en landmine. Angle unique.", "equipment": "Barre + Landmine", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            
            # BACK (Dos) - 15 exercices
            {"name": "Tractions (Pull-ups)", "muscle_group": "back", "difficulty": "intermediate", "description": "Exercice roi pour le dos. Prise large pour les dorsaux.", "equipment": "Barre de traction", "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800"},
            {"name": "Soulevé de Terre", "muscle_group": "back", "difficulty": "advanced", "description": "Roi des exercices. Toute la chaîne postérieure.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Rowing Barre", "muscle_group": "back", "difficulty": "intermediate", "description": "Tirage horizontal pour l'épaisseur du dos.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Rowing Haltère", "muscle_group": "back", "difficulty": "intermediate", "description": "Tirage unilatéral. Corrige les déséquilibres.", "equipment": "Haltère + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Tirage Vertical", "muscle_group": "back", "difficulty": "beginner", "description": "Alternative aux tractions. Machine guidée.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Tirage Horizontal", "muscle_group": "back", "difficulty": "beginner", "description": "Rowing à la machine. Milieu du dos.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Tractions Supination", "muscle_group": "back", "difficulty": "intermediate", "description": "Paumes vers soi. Plus de biceps.", "equipment": "Barre de traction", "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800"},
            {"name": "Face Pull", "muscle_group": "back", "difficulty": "beginner", "description": "Tirage vers le visage. Arrière d'épaules et trapèzes.", "equipment": "Câble", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Shrugs (Haussements)", "muscle_group": "back", "difficulty": "beginner", "description": "Isolation des trapèzes supérieurs.", "equipment": "Haltères ou Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Soulevé de Terre Roumain", "muscle_group": "back", "difficulty": "intermediate", "description": "Variante jambes tendues. Focus ischio-jambiers.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "T-Bar Row", "muscle_group": "back", "difficulty": "intermediate", "description": "Rowing avec barre en T. Épaisseur du dos.", "equipment": "Barre + Landmine", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Pullover Câble", "muscle_group": "back", "difficulty": "intermediate", "description": "Extension des bras vers le bas. Dorsaux.", "equipment": "Câble", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Good Morning", "muscle_group": "back", "difficulty": "intermediate", "description": "Flexion du buste. Lombaires et ischio-jambiers.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Hyperextensions", "muscle_group": "back", "difficulty": "beginner", "description": "Renforcement des lombaires. Banc à 45°.", "equipment": "Banc à lombaires", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Seal Row", "muscle_group": "back", "difficulty": "intermediate", "description": "Rowing allongé sur banc. Élimine la triche.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            
            # LEGS (Jambes) - 15 exercices
            {"name": "Squats", "muscle_group": "legs", "difficulty": "intermediate", "description": "Roi des exercices jambes. Quadriceps, fessiers, ischio.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Squats Avant", "muscle_group": "legs", "difficulty": "advanced", "description": "Barre devant. Plus de quadriceps, moins de dos.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Fentes (Lunges)", "muscle_group": "legs", "difficulty": "beginner", "description": "Travail unilatéral. Équilibre et coordination.", "equipment": "Poids du corps ou Haltères", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Leg Press", "muscle_group": "legs", "difficulty": "beginner", "description": "Machine guidée. Sécuritaire pour charger lourd.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Leg Extension", "muscle_group": "legs", "difficulty": "beginner", "description": "Isolation des quadriceps. Finition.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Leg Curl", "muscle_group": "legs", "difficulty": "beginner", "description": "Isolation des ischio-jambiers.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Bulgarian Split Squat", "muscle_group": "legs", "difficulty": "intermediate", "description": "Fente arrière pied surélevé. Intense.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Hack Squat", "muscle_group": "legs", "difficulty": "intermediate", "description": "Machine à squat inclinée. Quadriceps.", "equipment": "Machine", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Goblet Squat", "muscle_group": "legs", "difficulty": "beginner", "description": "Squat avec haltère ou kettlebell devant.", "equipment": "Haltère", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Step-ups", "muscle_group": "legs", "difficulty": "beginner", "description": "Montées sur banc. Fessiers et quadriceps.", "equipment": "Banc + Haltères", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Sissy Squat", "muscle_group": "legs", "difficulty": "advanced", "description": "Squat penché en arrière. Quadriceps intense.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Pistol Squat", "muscle_group": "legs", "difficulty": "advanced", "description": "Squat sur une jambe. Force et équilibre.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Nordic Curl", "muscle_group": "legs", "difficulty": "advanced", "description": "Flexion ischio-jambiers assistée. Très intense.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Calf Raises (Mollets)", "muscle_group": "legs", "difficulty": "beginner", "description": "Élévations sur pointes de pieds. Mollets.", "equipment": "Poids du corps ou Machine", "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=800"},
            {"name": "Box Jumps", "muscle_group": "legs", "difficulty": "intermediate", "description": "Sauts sur boîte. Puissance explosive.", "equipment": "Boîte pliométrique", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            
            # SHOULDERS (Épaules) - 12 exercices
            {"name": "Développé Militaire", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Poussée verticale. Deltoïdes antérieurs et moyens.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Développé Haltères Assis", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Plus grande amplitude que la barre.", "equipment": "Haltères + Banc", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Élévations Latérales", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes moyens. Largeur d'épaules.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Élévations Frontales", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes antérieurs.", "equipment": "Haltères ou Barre", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Oiseau (Rear Delt Fly)", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Isolation deltoïdes postérieurs. Penché en avant.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Arnold Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Rotation des haltères. Travail complet.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Upright Row", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Tirage vertical. Deltoïdes et trapèzes.", "equipment": "Barre ou Haltères", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Pike Push-ups", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Pompes en V inversé. Poids du corps.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Handstand Push-ups", "muscle_group": "shoulders", "difficulty": "advanced", "description": "Pompes en équilibre sur les mains. Très difficile.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?w=800"},
            {"name": "Cable Lateral Raise", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Élévations latérales au câble. Tension constante.", "equipment": "Câble", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Bradford Press", "muscle_group": "shoulders", "difficulty": "intermediate", "description": "Développé avant/arrière alterné. Tension continue.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            {"name": "Lu Raise", "muscle_group": "shoulders", "difficulty": "beginner", "description": "Élévation en arc de cercle. Deltoïdes complets.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800"},
            
            # ARMS (Bras) - 12 exercices
            {"name": "Curls Biceps Barre", "muscle_group": "arms", "difficulty": "beginner", "description": "Exercice de base pour la masse des biceps.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Curls Haltères", "muscle_group": "arms", "difficulty": "beginner", "description": "Flexion alternée ou simultanée.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Curls Marteau", "muscle_group": "arms", "difficulty": "beginner", "description": "Prise neutre. Brachial et avant-bras.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Curls Pupitre", "muscle_group": "arms", "difficulty": "intermediate", "description": "Bras calés sur pupitre. Isolation stricte.", "equipment": "Haltère + Pupitre", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Dips Triceps", "muscle_group": "arms", "difficulty": "intermediate", "description": "Corps vertical. Focus triceps.", "equipment": "Barres parallèles", "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800"},
            {"name": "Extensions Triceps", "muscle_group": "arms", "difficulty": "beginner", "description": "Bras au-dessus de la tête. Isolation longue portion.", "equipment": "Haltère", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Kickback Triceps", "muscle_group": "arms", "difficulty": "beginner", "description": "Extension arrière. Finition triceps.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Barre au Front", "muscle_group": "arms", "difficulty": "intermediate", "description": "Skull crushers. Triceps complets.", "equipment": "Barre + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Curls Concentration", "muscle_group": "arms", "difficulty": "beginner", "description": "Assis, coude calé sur cuisse. Pic de contraction.", "equipment": "Haltère", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            {"name": "Close Grip Bench", "muscle_group": "arms", "difficulty": "intermediate", "description": "Développé couché prise serrée. Triceps.", "equipment": "Barre + Banc", "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
            {"name": "Cable Pushdown", "muscle_group": "arms", "difficulty": "beginner", "description": "Extension triceps au câble. Tension constante.", "equipment": "Câble", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "21s Biceps", "muscle_group": "arms", "difficulty": "intermediate", "description": "7 reps bas + 7 reps haut + 7 reps complètes. Congestion.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?w=800"},
            
            # ABS (Abdominaux) - 12 exercices
            {"name": "Planche (Plank)", "muscle_group": "abs", "difficulty": "beginner", "description": "Gainage statique. Sangle abdominale profonde.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Flexion du buste. Grand droit.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Relevé de Jambes", "muscle_group": "abs", "difficulty": "intermediate", "description": "Bas des abdominaux. Allongé ou suspendu.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Russian Twist", "muscle_group": "abs", "difficulty": "intermediate", "description": "Rotation du buste. Obliques.", "equipment": "Poids du corps ou Médecine ball", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Mountain Climbers", "muscle_group": "abs", "difficulty": "intermediate", "description": "Genoux vers poitrine alternés. Cardio + abs.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Ab Wheel Rollout", "muscle_group": "abs", "difficulty": "advanced", "description": "Roulette abdominale. Très intense.", "equipment": "Ab wheel", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Planche Latérale", "muscle_group": "abs", "difficulty": "intermediate", "description": "Gainage sur le côté. Obliques.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Bicycle Crunch", "muscle_group": "abs", "difficulty": "beginner", "description": "Coude vers genou opposé. Rotation.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "V-Ups", "muscle_group": "abs", "difficulty": "intermediate", "description": "Toucher les pieds en V. Complet.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Dragon Flag", "muscle_group": "abs", "difficulty": "advanced", "description": "Corps rigide suspendu. Très difficile.", "equipment": "Banc", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Hollow Hold", "muscle_group": "abs", "difficulty": "intermediate", "description": "Position creuse maintenue. Gainage dynamique.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?w=800"},
            {"name": "Cable Crunch", "muscle_group": "abs", "difficulty": "intermediate", "description": "Crunch au câble. Résistance progressive.", "equipment": "Câble", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            
            # CARDIO - 10 exercices
            {"name": "Burpees", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Squat + pompe + saut. Métabolique intense.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Jump Rope (Corde à sauter)", "muscle_group": "cardio", "difficulty": "beginner", "description": "Cardio classique. Coordination.", "equipment": "Corde à sauter", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Sprints", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Course à vitesse maximale. Explosivité.", "equipment": "Espace", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Battle Ropes", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Ondes avec cordes lourdes. Cardio + bras.", "equipment": "Battle ropes", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Rowing Machine", "muscle_group": "cardio", "difficulty": "beginner", "description": "Rameur. Cardio + dos.", "equipment": "Rameur", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "Assault Bike", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Vélo avec bras. Très intense.", "equipment": "Assault bike", "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800"},
            {"name": "High Knees", "muscle_group": "cardio", "difficulty": "beginner", "description": "Genoux hauts sur place. Cardio rapide.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Jumping Jacks", "muscle_group": "cardio", "difficulty": "beginner", "description": "Échauffement classique. Cardio léger.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Kettlebell Swings", "muscle_group": "cardio", "difficulty": "intermediate", "description": "Balancement explosif. Cardio + postérieur.", "equipment": "Kettlebell", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Sled Push", "muscle_group": "cardio", "difficulty": "advanced", "description": "Poussée de traîneau. Force + cardio.", "equipment": "Traîneau", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            
            # FULL BODY (Corps complet) - 10 exercices
            {"name": "Thruster", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + développé militaire. Complet.", "equipment": "Barre ou Haltères", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Clean & Press", "muscle_group": "full", "difficulty": "advanced", "description": "Épaulé + développé. Olympique.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Turkish Get-Up", "muscle_group": "full", "difficulty": "advanced", "description": "Se lever avec poids au-dessus de la tête. Stabilité.", "equipment": "Kettlebell", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Man Makers", "muscle_group": "full", "difficulty": "advanced", "description": "Burpee + rowing + clean. Très complet.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Bear Crawl", "muscle_group": "full", "difficulty": "intermediate", "description": "Marche à quatre pattes. Coordination.", "equipment": "Poids du corps", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Farmer's Walk", "muscle_group": "full", "difficulty": "intermediate", "description": "Marche avec charges lourdes. Grip + core.", "equipment": "Haltères ou Kettlebells", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Wall Balls", "muscle_group": "full", "difficulty": "intermediate", "description": "Squat + lancer de ballon. Explosif.", "equipment": "Médecine ball", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
            {"name": "Snatch (Arraché)", "muscle_group": "full", "difficulty": "advanced", "description": "Mouvement olympique. Puissance totale.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Clean (Épaulé)", "muscle_group": "full", "difficulty": "advanced", "description": "Barre du sol aux épaules. Explosif.", "equipment": "Barre", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800"},
            {"name": "Devil Press", "muscle_group": "full", "difficulty": "advanced", "description": "Burpee + snatch haltères. Très intense.", "equipment": "Haltères", "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"},
        ]

        self.stdout.write(self.style.SUCCESS(f"🌱 Seeding {len(exercises)} Exercises..."))
        created_count = 0
        updated_count = 0
        
        for data in exercises:
            ex, created = Exercise.objects.update_or_create(
                name=data["name"], 
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"   ✅ Created: {ex.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"   🔄 Updated: {ex.name}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created: {created_count} | Updated: {updated_count} | Total: {len(exercises)}"))
