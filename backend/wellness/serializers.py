from rest_framework import serializers
from .models import OnboardingEntry, DailyHabit, HealthScore, UserPlan


class OnboardingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingEntry
        fields = '__all__'
        read_only_fields = ('user', 'completed_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DailyHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyHabit
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class HealthScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthScore
        fields = '__all__'
        read_only_fields = (
            'user', 'date', 'total_score', 'fitness_score',
            'recovery_score', 'lifestyle_score', 'consistency_score'
        )


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = '__all__'
        read_only_fields = ('user', 'workout_plan', 'nutrition_plan', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user

        # Extract data for analysis
        goal = validated_data.get('goal')
        age = validated_data.get('age')
        gender = validated_data.get('gender', 'male')
        weight = validated_data.get('weight')
        height = validated_data.get('height')
        activity_level = validated_data.get('activity_level')

        # --- ANALYSIS ALGORITHM ---
        # 1. BMI Calculation
        height_m = height / 100
        bmi = weight / (height_m * height_m)

        # 2. Detailed Scoring Logic

        # A. Fitness Score (Based on BMI & Activity)
        fitness_score = 70
        if 18.5 <= bmi <= 24.9:
            fitness_score += 15
        elif 25 <= bmi <= 29.9:
            fitness_score += 5
        else:
            fitness_score -= 5

        if activity_level == 'elite':
            fitness_score += 15
        elif activity_level == 'active':
            fitness_score += 10
        elif activity_level == 'moderate':
            fitness_score += 5
        fitness_score = min(max(fitness_score, 0), 100)

        # B. Recovery Score (Age & Gender heuristics)
        recovery_score = 80
        if age < 30:
            recovery_score += 10
        elif age > 50:
            recovery_score -= 10

        if gender == 'female':
            recovery_score += 5  # Slightly better recovery on average in some models
        recovery_score = min(max(recovery_score, 0), 100)

        # C. Lifestyle Score (Dietary Habits)
        lifestyle_score = 75
        dietary_preferences = validated_data.get('dietary_preferences', '').lower()
        if any(d in dietary_preferences for d in ['keto', 'vegan', 'paleo', 'clean']):
            lifestyle_score += 15
        if not dietary_preferences:
            lifestyle_score -= 5
        lifestyle_score = min(max(lifestyle_score, 0), 100)

        # D. Consistency Score (New Plan Base)
        consistency_score = 85  # Start strong

        # Total Weighted Score
        total_score = int(
            (fitness_score * 0.4) +
            (recovery_score * 0.2) +
            (lifestyle_score * 0.2) +
            (consistency_score * 0.2)
        )

        # Update User's Stats (Gamification)
        if hasattr(user, 'profile'):
            user.profile.health_score = total_score
            user.profile.add_xp(500)  # Award 500 XP for creating a plan
            # user.profile.save() is called inside add_xp

        # Create Historical Health Score Record
        HealthScore.objects.create(
            user=user,
            fitness_score=fitness_score,
            recovery_score=recovery_score,
            lifestyle_score=lifestyle_score,
            consistency_score=consistency_score,
            total_score=total_score
        )

        workout_plan = {
            'schedule': '3 days/week',
            'focus': 'General Fitness',
            'exercises': ['Squats', 'Pushups', 'Plank'],
            'analysis': {
                'bmi': round(bmi, 1),
                'score': total_score,
                'breakdown': {
                    'fitness': fitness_score,
                    'recovery': recovery_score,
                    'lifestyle': lifestyle_score,
                    'consistency': consistency_score
                },
                'message': f"You are operating at {total_score}% of your potential. "
                           f"Optimized for {goal.replace('_', ' ')}."
            }
        }

        # Base Nutrition Plan
        base_calories = 2000
        if gender == 'female':
            base_calories = 1800

        nutrition_plan = {
            'calories': base_calories,
            'macros': {'protein': '150g', 'carbs': '200g', 'fats': '65g'},
            'meals': {
                'breakfast': 'Oatmeal with whey protein and berries',
                'lunch': 'Grilled chicken breast with quinoa and broccoli',
                'dinner': 'Baked salmon with sweet potato and asparagus',
                'snack': 'Greek yogurt with almonds'
            }
        }

        if goal == 'weight_loss':
            workout_plan['schedule'] = '4-5 days/week'
            workout_plan['focus'] = 'High Intensity Interval Training (HIIT) + Cardio'
            workout_plan['exercises'] = ['Burpees', 'Mountain Climbers', 'Jump Rope', 'Sprints']

            nutrition_plan['calories'] = base_calories - 300
            nutrition_plan['macros'] = {'protein': '180g', 'carbs': '120g', 'fats': '60g'}
            nutrition_plan['meals'] = {
                'breakfast': 'Egg white omelet with spinach and mushrooms',
                'lunch': 'Tuna salad with mixed greens and olive oil dressing',
                'dinner': 'Lean turkey meatballs with zucchini noodles',
                'snack': 'Celery sticks with almond butter'
            }
        elif goal == 'muscle_gain':
            workout_plan['schedule'] = '4-5 days/week'
            workout_plan['focus'] = 'Hypertrophy & Strength'
            workout_plan['exercises'] = ['Deadlifts', 'Bench Press', 'Squats', 'Overhead Press']

            nutrition_plan['calories'] = base_calories + 500
            nutrition_plan['macros'] = {'protein': '220g', 'carbs': '350g', 'fats': '80g'}
            nutrition_plan['meals'] = {
                'breakfast': '3 whole eggs, oatmeal with banana and peanut butter',
                'lunch': 'Steak burrito bowl with brown rice, black beans, and avocado',
                'dinner': 'Chicken pasta with marinara sauce and parmesan',
                'snack': 'Protein shake and a bagel with cream cheese'
            }
        elif goal == 'endurance':
            workout_plan['schedule'] = '5-6 days/week'
            workout_plan['focus'] = 'Cardiovascular Endurance'
            workout_plan['exercises'] = ['Long Run', 'Cycling', 'Swimming', 'Tempo Run']

            nutrition_plan['calories'] = base_calories + 300
            nutrition_plan['macros'] = {'protein': '140g', 'carbs': '400g', 'fats': '60g'}
            nutrition_plan['meals'] = {
                'breakfast': 'Bagel with jam and a side of fruit',
                'lunch': 'Pasta salad with grilled chicken and light vinaigrette',
                'dinner': 'Rice bowl with tofu and stir-fried vegetables',
                'snack': 'Banana and energy bar'
            }

        validated_data['workout_plan'] = workout_plan
        validated_data['nutrition_plan'] = nutrition_plan

        plan, created = UserPlan.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return plan
