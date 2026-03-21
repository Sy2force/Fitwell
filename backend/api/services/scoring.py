from django.utils.translation import gettext as _

def calculate_health_score(height, weight, activity_level):
    """
    Calcule le score de santé global et fournit une analyse.
    """
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    bmi_score = 0
    message = ""
    
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

    return {
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
