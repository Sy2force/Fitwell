from rest_framework import serializers
from api.models import WellnessPlan


class WellnessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessPlan
        fields = '__all__'
        read_only_fields = ('user', 'workout_plan', 'nutrition_plan', 'created_at')
