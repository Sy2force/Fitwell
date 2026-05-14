from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from api.models import User, Exercise, WellnessPlan, Recipe

class FlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='flowuser', password='password')
        self.user.is_onboarded = True
        self.user.save()
        
        # Create some exercises
        self.ex1 = Exercise.objects.create(name="Pushups", muscle_group="chest", difficulty="beginner", description="Push the floor")
        self.ex2 = Exercise.objects.create(name="Squats", muscle_group="legs", difficulty="beginner", description="Sit down and up")
        
        # Create a recipe
        self.recipe = Recipe.objects.create(title="Protein Shake", category="shake", calories=200, protein_g=20, carbs_g=10, fats_g=5, ingredients="Whey\nWater", instructions="Mix.")

    def test_home_view_context(self):
        # 1. Unauthenticated
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Language-agnostic: checks that the translated "Create my free account" CTA is present
        self.assertContains(response, _("Créer mon compte gratuit"))
        
        # 2. Authenticated, No Plan
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Page accessible pour utilisateur authentifié
        
        # 3. Authenticated, With Plan
        WellnessPlan.objects.create(
            user=self.user, age=25, gender='male', height=180, weight=80, goal='maintenance', activity_level='moderate'
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Page accessible avec plan

    def test_workout_flow_auto_gen(self):
        """Test accessing workout session directly (auto-generation)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('workout_session'))
        self.assertEqual(response.status_code, 200)
        # Should contain at least Warmup, Cooldown and some exercises
        # Sequence is a list of dicts in context
        sequence = response.context['sequence']
        self.assertTrue(len(sequence) >= 3) # Warmup + 1 Ex + Cooldown minimum
        self.assertEqual(sequence[0]['type'], 'warmup')
        self.assertEqual(sequence[-1]['type'], 'cooldown')

    def test_workout_flow_manual_setup(self):
        """Test submitting form from setup page"""
        self.client.force_login(self.user)
        
        url = reverse('workout_session')
        data = {
            'work_duration': 60,
            'rest_duration': 30,
            'exercises': [self.ex1.id, self.ex2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        sequence = response.context['sequence']
        # Sequence: Warmup, Ex1, Rest, Ex2, Rest, Cooldown
        # total items: 1 (warmup) + 2*2 (ex+rest) - last rest might be skipped? Logic says:
        # Loop ex: append ex, append rest.
        # Then append cooldown.
        # So 1 + 2 + 2 + 1 = 6 items.
        
        self.assertTrue(len(sequence) >= 4) 
        
        # Check if our exercises are in there
        ex_names = [s['name'] for s in sequence if s['type'] == 'exercise']
        self.assertIn("Pushups", ex_names)
        self.assertIn("Squats", ex_names)
        
        # Check durations
        ex_items = [s for s in sequence if s['type'] == 'exercise']
        self.assertEqual(ex_items[0]['duration'], 60)
        
        rest_items = [s for s in sequence if s['type'] == 'rest']
        self.assertEqual(rest_items[0]['duration'], 30)

    def test_exercise_library_filter(self):
        self.client.force_login(self.user)
        url = reverse('exercise_library')
        
        # All
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Filter by chest
        url = reverse('exercise_library') + '?muscle=chest'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Filter by legs
        url = reverse('exercise_library') + '?muscle=legs'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_filter(self):
        self.client.force_login(self.user)
        Recipe.objects.create(title="Salad", category="lunch", difficulty="easy")
        
        url = reverse('recipe_list')
        response = self.client.get(url + '?category=shake')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Protein Shake")
        self.assertNotContains(response, "Salad")

    def test_complete_workout_api(self):
        """Test the API endpoint for completing a workout"""
        self.client.force_login(self.user)
        url = reverse('complete_workout')
        
        # Initial stats
        initial_xp = self.user.stats.xp
        initial_streak = self.user.stats.current_streak
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['energy_gain'], 100)
        
        # Verify DB updates
        self.user.stats.refresh_from_db()
        self.assertEqual(self.user.stats.xp, initial_xp + 100)
        # Streak might not change if already updated today, but let's check it doesn't break
        
        # Verify Daily Log
        from api.models import DailyLog
        from django.utils import timezone
        log = DailyLog.objects.get(user=self.user, date=timezone.now().date())
        # Language-agnostic: checks the log entry contains the XP gain marker (+100)
        self.assertIn("+100", log.notes)
        # Also verify it contains either the French or English translation of the session message
        self.assertTrue(
            _("Session Studio terminée") in log.notes,
            f"Expected translated session-complete message in: {log.notes}"
        )
