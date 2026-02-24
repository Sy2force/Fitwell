from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import User, Category, Article, Comment, UserPlan

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'avatar')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar')
        read_only_fields = ('username',)  # Username usually shouldn't change easily

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_avatar = serializers.ReadOnlyField(source='user.avatar')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'user')

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.ReadOnlyField(source='author.avatar')
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at', 'likes')

    @extend_schema_field(bool)
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)

class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = '__all__'
        read_only_fields = ('user', 'workout_plan', 'nutrition_plan', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        # Logic to generate plan based on input
        # This is a simplified simulation logic
        goal = validated_data.get('goal')
        
        workout_plan = {
            'schedule': '3 days/week',
            'focus': 'General Fitness',
            'exercises': ['Squats', 'Pushups', 'Plank']
        }
        
        # Base Nutrition Plan
        nutrition_plan = {
            'calories': 2000,
            'macros': {'protein': '150g', 'carbs': '200g', 'fats': '65g'},
            'meals': {
                'breakfast': 'Oatmeal with whey protein and berries',
                'lunch': 'Grilled chicken breast with quinoa and broccoli',
                'dinner': 'Baked salmon with sweet potato and asparagus',
                'snack': 'Greek yogurt with almonds'
            }
        }

        if goal == 'weight_loss':
            workout_plan = {
                'schedule': '4-5 days/week',
                'focus': 'High Intensity Interval Training (HIIT) + Cardio',
                'exercises': ['Burpees', 'Mountain Climbers', 'Jump Rope', 'Sprints']
            }
            nutrition_plan['calories'] = 1800
            nutrition_plan['macros'] = {'protein': '180g', 'carbs': '120g', 'fats': '60g'}
            nutrition_plan['meals'] = {
                'breakfast': 'Egg white omelet with spinach and mushrooms',
                'lunch': 'Tuna salad with mixed greens and olive oil dressing',
                'dinner': 'Lean turkey meatballs with zucchini noodles',
                'snack': 'Celery sticks with almond butter'
            }
        elif goal == 'muscle_gain':
            workout_plan = {
                'schedule': '4-5 days/week',
                'focus': 'Hypertrophy & Strength',
                'exercises': ['Deadlifts', 'Bench Press', 'Squats', 'Overhead Press']
            }
            nutrition_plan['calories'] = 3000
            nutrition_plan['macros'] = {'protein': '220g', 'carbs': '350g', 'fats': '80g'}
            nutrition_plan['meals'] = {
                'breakfast': '3 whole eggs, oatmeal with banana and peanut butter',
                'lunch': 'Steak burrito bowl with brown rice, black beans, and avocado',
                'dinner': 'Chicken pasta with marinara sauce and parmesan',
                'snack': 'Protein shake and a bagel with cream cheese'
            }
        elif goal == 'endurance':
             workout_plan = {
                'schedule': '5-6 days/week',
                'focus': 'Cardiovascular Endurance',
                'exercises': ['Long Run', 'Cycling', 'Swimming', 'Tempo Run']
            }
             nutrition_plan['calories'] = 2600
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
