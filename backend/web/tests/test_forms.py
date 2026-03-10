from django.test import TestCase
from web.forms import WellnessPlanForm

class WellnessPlanFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'age': 25,
            'gender': 'male',
            'height': 180,
            'weight': 75,
            'goal': 'muscle_gain',
            'activity_level': 'active'
        }
        form = WellnessPlanForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_height(self):
        data = {
            'age': 25,
            'gender': 'male',
            'height': -10, # Invalid
            'weight': 75,
            'goal': 'muscle_gain',
            'activity_level': 'active'
        }
        form = WellnessPlanForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('height', form.errors)

    def test_invalid_weight(self):
        data = {
            'age': 25,
            'gender': 'male',
            'height': 180,
            'weight': 0, # Invalid
            'goal': 'muscle_gain',
            'activity_level': 'active'
        }
        form = WellnessPlanForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('weight', form.errors)

    def test_invalid_age(self):
        data = {
            'age': -5, # Invalid
            'gender': 'male',
            'height': 180,
            'weight': 75,
            'goal': 'muscle_gain',
            'activity_level': 'active'
        }
        form = WellnessPlanForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
