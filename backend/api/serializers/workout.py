from rest_framework import serializers
from api.models import Exercise, ExerciseSet, WorkoutSession


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'name', 'slug', 'muscle_group', 'difficulty', 'description', 'equipment', 'image_url')
        read_only_fields = ('slug',)


class ExerciseSetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.ReadOnlyField(source='exercise.name')
    exercise_details = ExerciseSerializer(source='exercise', read_only=True)
    volume = serializers.ReadOnlyField()
    
    class Meta:
        model = ExerciseSet
        fields = ('id', 'session', 'exercise', 'exercise_name', 'exercise_details', 'set_number', 'reps', 'weight', 'rest_seconds', 'notes', 'volume', 'created_at')
        read_only_fields = ('created_at',)


class WorkoutSessionSerializer(serializers.ModelSerializer):
    sets = ExerciseSetSerializer(many=True, read_only=True)
    user_username = serializers.ReadOnlyField(source='user.username')
    sets_count = serializers.IntegerField(source='sets.count', read_only=True)
    
    class Meta:
        model = WorkoutSession
        fields = ('id', 'user', 'user_username', 'started_at', 'completed_at', 'duration_minutes', 'status', 'notes', 'total_volume', 'sets', 'sets_count')
        read_only_fields = ('user', 'started_at', 'completed_at', 'duration_minutes', 'total_volume')


class WorkoutSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = ('notes',)


class ExerciseSetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ('exercise', 'set_number', 'reps', 'weight', 'rest_seconds', 'notes')
