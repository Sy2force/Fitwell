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

def generate_wellness_plan(age, gender, height, weight, goal, activity_level):
    """
    Generates a workout and nutrition plan based on biometrics.
    Returns a tuple (workout_plan, nutrition_plan, health_score).
    """
    # 1. BMR / TDEE Calculation
    # Mifflin-St Jeor Equation
    bmr = 10 * weight + 6.25 * height - 5 * age
    bmr += 5 if gender == 'male' else -161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'moderate': 1.55,
        'active': 1.725,
        'elite': 1.9
    }
    # Default to moderate if not found
    multiplier = activity_multipliers.get(activity_level, 1.55)
    tdee = bmr * multiplier
    
    # 2. Adjust for Goal
    target_calories = tdee
    if goal == 'weight_loss':
        target_calories -= 500
    elif goal == 'muscle_gain':
        target_calories += 300

    # 3. Nutrition Plan Structure
    # Protein: 2g per kg of bodyweight (Standard for active individuals)
    protein_g = int(weight * 2)
    protein_cals = protein_g * 4
    
    # Remaining calories for Carbs and Fats
    remaining_cals = target_calories - protein_cals
    
    # Split remaining: 60% Carbs, 40% Fats
    # This ensures Total Cals = Protein + Carbs + Fats
    carbs_cals = remaining_cals * 0.60
    fats_cals = remaining_cals * 0.40
    
    carbs_g = int(carbs_cals / 4)
    fats_g = int(fats_cals / 9)
    
    nutrition_plan = {
        "calories": int(target_calories),
        "macros": {
            "protein": f"{protein_g}g",
            "carbs": f"{carbs_g}g",
            "fats": f"{fats_g}g"
        },
        "meals": {
            "breakfast": _("Flocons d'avoine, whey protéine & fruits rouges"),
            "lunch": _("Blanc de poulet, quinoa, légumes rôtis"),
            "snack": _("Yaourt grec & amandes"),
            "dinner": _("Pavé de saumon avec patate douce")
        }
    }

    # 4. Workout Plan Structure avec Split Training
    split_training = generate_split_training(goal, activity_level)
    
    schedule = _("4 jours/semaine - split haut/bas")
    if activity_level in ['active', 'elite']:
        schedule = _("6 jours/semaine - Split PPL (Push/Pull/Legs)")
    
    exercises = [
        _("Mouvements composés (squat, soulevé de terre, développé couché)"),
        _("Travail d'accessoires (haltères, poulies)"),
        _("Mobilité (10 min avant séance)"),
        _("Cardio zone 2 (2x 30min)")
    ]
    
    workout_plan = {
        'schedule': schedule,
        'exercises': exercises,
        'split': split_training
    }

    # Dynamic Analysis Calculation
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    bmi_score = 0
    
    # BMI Scoring
    if 18.5 <= bmi <= 24.9:
        bmi_score = 90
        message = _("Votre profil biométrique est excellent. Maintenez cette fondation.")
    elif 25 <= bmi <= 29.9:
        bmi_score = 75
        message = _("Légère surcharge pondérale détectée. Le plan inclut un déficit calorique modéré.")
    elif bmi < 18.5:
        bmi_score = 70
        message = _("Indice de masse corporelle bas. Focus sur l'hypertrophie et le surplus calorique.")
    else:
        bmi_score = 60
        message = _("Optimisation métabolique requise. Priorité à l'activité non-sportive (NEAT).")

    # Activity Adjustment
    activity_bonus = {
        'sedentary': 0,
        'moderate': 5,
        'active': 10,
        'elite': 15
    }.get(activity_level, 5)

    health_score = int((bmi_score + 70 + activity_bonus) / 2)
    health_score = min(99, max(40, health_score)) # Clamp between 40 and 99

    workout_plan["analysis"] = {
        "score": health_score,
        "message": message,
        "bmi": round(bmi, 1),
        "breakdown": {
            "fitness": 60 + (activity_bonus * 2),
            "recovery": 85 - activity_bonus,
            "lifestyle": 70 + activity_bonus,
            "consistency": 90
        }
    }
    
    return workout_plan, nutrition_plan, health_score
