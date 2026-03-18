from django.test import TestCase
from django.urls import reverse
from api.models import User, CustomEvent
from django.utils import timezone
import datetime

class AgendaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='agendatester', password='password')
        self.client.force_login(self.user)

    def test_add_event(self):
        url = reverse('custom_planner')
        data = {
            'title': 'Test Meeting',
            'event_type': 'work',
            'day_of_week': 'monday',
            'start_time': '09:00',
            'end_time': '10:00',
            'priority': 'high'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirects back
        
        self.assertTrue(CustomEvent.objects.filter(user=self.user, title='Test Meeting').exists())
        event = CustomEvent.objects.get(title='Test Meeting')
        self.assertEqual(event.priority, 'high')

    def test_delete_event(self):
        event = CustomEvent.objects.create(
            user=self.user, 
            title='Delete Me', 
            day_of_week='monday',
            start_time='12:00'
        )
        url = reverse('delete_custom_event', args=[event.id])
        response = self.client.post(url) # Using post usually for delete, or get if view allows
        # View uses get usually for simple delete links but better practice is post. 
        # Looking at views.py: delete_custom_event accepts GET (no @require_POST).
        # Let's check views.py again.
        # It's a standard view, default methods allowed.
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomEvent.objects.filter(id=event.id).exists())

    def test_complete_event_ajax(self):
        event = CustomEvent.objects.create(
            user=self.user, 
            title='Complete Me', 
            priority='medium'
        )
        url = reverse('complete_custom_event', args=[event.id])
        # This view is @require_POST and returns JsonResponse
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        event.refresh_from_db()
        self.assertTrue(event.is_completed)
        
        # Check XP gain
        self.user.stats.refresh_from_db()
        self.assertTrue(self.user.stats.xp > 0)

    def test_dashboard_shows_today_events(self):
        # Create an event for today
        today_name = timezone.now().strftime('%A').lower()
        CustomEvent.objects.create(
            user=self.user,
            title='Today Event',
            day_of_week=today_name,
            start_time='08:00'
        )
        
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Today Event')
