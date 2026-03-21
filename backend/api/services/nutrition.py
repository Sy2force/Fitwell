from django.utils.translation import gettext as _

def calculate_bmr_tdee(age, gender, height, weight, activity_level):
    """
    Calcule le BMR (Mifflin-St Jeor) et le TDEE.
    """
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
    return tdee

def calculate_macros(weight, target_calories):
    """
    Calcule les macronutriments (Protéines, Glucides, Lipides).
    """
    # Protein: 2g per kg of bodyweight (Standard for active individuals)
    protein_g = int(weight * 2)
    protein_cals = protein_g * 4
    
    # Remaining calories for Carbs and Fats
    remaining_cals = target_calories - protein_cals
    
    # Split remaining: 60% Carbs, 40% Fats
    carbs_cals = remaining_cals * 0.60
    fats_cals = remaining_cals * 0.40
    
    carbs_g = int(carbs_cals / 4)
    fats_g = int(fats_cals / 9)
    
    return {
        "protein": f"{protein_g}g",
        "carbs": f"{carbs_g}g",
        "fats": f"{fats_g}g"
    }

def get_meal_plan():
    return {
        "breakfast": _("Flocons d'avoine, whey protéine & fruits rouges"),
        "lunch": _("Blanc de poulet, quinoa, légumes rôtis"),
        "snack": _("Yaourt grec & amandes"),
        "dinner": _("Pavé de saumon avec patate douce")
    }
