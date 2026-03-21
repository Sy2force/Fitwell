from rest_framework import viewsets, permissions
from api.models import WellnessPlan
from api.serializers import WellnessPlanSerializer
from api.services import generate_wellness_plan

class WellnessPlanViewSet(viewsets.ModelViewSet):
    """
    API pour le Planner.
    - POST: Génère un plan basé sur les biometrics.
    - GET: Récupère l'historique des plans.
    """
    serializer_class = WellnessPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WellnessPlan.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # 1. Récupération des données d'entrée
        data = serializer.validated_data
        
        # 2. Génération du plan via le service centralisé (Source Unique de Vérité)
        workout_plan, nutrition_plan, health_score = generate_wellness_plan(
            age=data.get('age'),
            gender=data.get('gender'),
            height=data.get('height'),
            weight=data.get('weight'),
            goal=data.get('goal'),
            activity_level=data.get('activity_level')
        )

        # 3. Sauvegarde
        serializer.save(
            user=self.request.user, 
            workout_plan=workout_plan, 
            nutrition_plan=nutrition_plan
        )
        
        # 4. Mise à jour des stats User
        if hasattr(self.request.user, 'stats'):
            stats = self.request.user.stats
            stats.health_score = health_score
            
            # Mise à jour des sous-scores depuis l'analyse
            if 'analysis' in workout_plan and 'breakdown' in workout_plan['analysis']:
                breakdown = workout_plan['analysis']['breakdown']
                stats.fitness_score = breakdown.get('fitness', 0)
                stats.recovery_score = breakdown.get('recovery', 0)
                stats.lifestyle_score = breakdown.get('lifestyle', 0)
                stats.consistency_score = breakdown.get('consistency', 0)
            
            # Gamification: +100 XP
            stats.xp += 100
            stats.level = 1 + (stats.xp // 500)
            
            stats.save()
