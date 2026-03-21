from django.utils.translation import gettext as _

def generate_split_training(goal, activity_level):
    """
    Génère un split d'entraînement (Push/Pull/Legs ou Full Body).
    """
    if activity_level in ['elite', 'active']:
        # PPL Split pour utilisateurs actifs
        return {
            'type': 'PPL',
            'frequency': '6x/semaine' if activity_level == 'elite' else '3x/semaine',
            'split': {
                'push': {
                    'focus': 'Pectoraux, Épaules, Triceps',
                    'exercises': ['Développé Couché', 'Développé Incliné', 'Développé Militaire', 'Élévations Latérales', 'Dips Triceps'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                },
                'pull': {
                    'focus': 'Dos, Biceps',
                    'exercises': ['Tractions', 'Rowing Barre', 'Tirage Vertical', 'Rowing Haltère', 'Curls Biceps'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                },
                'legs': {
                    'focus': 'Jambes, Abdominaux',
                    'exercises': ['Squats', 'Soulevé de Terre', 'Leg Press', 'Fentes', 'Planche'],
                    'sets': '15-20 sets total',
                    'reps': '8-12 reps' if goal == 'muscle_gain' else '12-15 reps'
                }
            }
        }
    else:
        # Full Body pour débutants/modérés
        return {
            'type': 'Full Body',
            'frequency': '3x/semaine',
            'exercises': ['Squats', 'Développé Couché', 'Rowing Barre', 'Développé Militaire', 'Tractions', 'Planche'],
            'sets': '3-4 sets par exercice',
            'reps': '10-12 reps' if goal == 'muscle_gain' else '12-15 reps',
            'rest': '90-120 secondes'
        }

def get_workout_schedule(activity_level):
    schedule = _("4 jours/semaine - split haut/bas")
    if activity_level in ['active', 'elite']:
        schedule = _("6 jours/semaine - Split PPL (Push/Pull/Legs)")
    return schedule

def get_base_exercises():
    return [
        _("Mouvements composés (squat, soulevé de terre, développé couché)"),
        _("Travail d'accessoires (haltères, poulies)"),
        _("Mobilité (10 min avant séance)"),
        _("Cardio zone 2 (2x 30min)")
    ]
