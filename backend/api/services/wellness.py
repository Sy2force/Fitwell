from .nutrition import calculate_bmr_tdee, calculate_macros, get_meal_plan
from .workout import generate_split_training, get_workout_schedule, get_base_exercises
from .scoring import calculate_health_score

def generate_wellness_plan(age, gender, height, weight, goal, activity_level):
    """
    Generates a workout and nutrition plan based on biometrics.
    Returns a tuple (workout_plan, nutrition_plan, health_score).
    """
    # 1. Nutrition Logic
    tdee = calculate_bmr_tdee(age, gender, height, weight, activity_level)
    
    target_calories = tdee
    if goal == 'weight_loss':
        target_calories -= 500
    elif goal == 'muscle_gain':
        target_calories += 300
        
    macros = calculate_macros(weight, target_calories)
    
    nutrition_plan = {
        "calories": int(target_calories),
        "macros": macros,
        "meals": get_meal_plan()
    }

    # 2. Workout Logic
    split_training = generate_split_training(goal, activity_level)
    schedule = get_workout_schedule(activity_level)
    exercises = get_base_exercises()
    
    # 3. Scoring & Analysis
    analysis = calculate_health_score(height, weight, activity_level)
    
    workout_plan = {
        'schedule': schedule,
        'exercises': exercises,
        'split': split_training,
        'analysis': analysis
    }
    
    return workout_plan, nutrition_plan, analysis['score']
