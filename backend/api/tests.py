from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Article, Category

class AccountTests(APITestCase):
    def test_registration(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('api:register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class ArticleTests(APITestCase):
    def setUp(self):
        # Create an admin user because only admins can create articles now
        self.user = User.objects.create_superuser(username='admin_author', email='admin@test.com', password='password')
        self.category = Category.objects.create(name='Health')
        self.client.force_authenticate(user=self.user)

    def test_create_article(self):
        """
        Ensure we can create a new article object.
        """
        url = reverse('api:article-list')
        data = {'title': 'Test Article', 'content': 'Content here', 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'Test Article')

    def test_get_articles(self):
        """
        Ensure we can retrieve articles.
        """
        Article.objects.create(title='Article 1', content='Content 1', author=self.user, category=self.category)
        url = reverse('api:article-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

from .services import generate_wellness_plan

class ServiceTests(APITestCase):
    def test_generate_wellness_plan_math(self):
        """
        Verify that the generated plan's calories and macros are mathematically consistent.
        """
        # Inputs
        age = 25
        gender = 'male'
        height = 180
        weight = 80
        goal = 'maintenance'
        activity_level = 'moderate'

        workout, nutrition, score = generate_wellness_plan(age, gender, height, weight, goal, activity_level)

        # 1. Verify Structure
        self.assertIn('calories', nutrition)
        self.assertIn('macros', nutrition)
        
        # 2. Verify Calorie/Macro consistency
        # Parse "160g" -> 160
        p_grams = int(nutrition['macros']['protein'][:-1])
        c_grams = int(nutrition['macros']['carbs'][:-1])
        f_grams = int(nutrition['macros']['fats'][:-1])
        
        total_cals_from_macros = (p_grams * 4) + (c_grams * 4) + (f_grams * 9)
        target_cals = nutrition['calories']
        
        # Allow small rounding difference (e.g. +/- 5 kcals)
        diff = abs(target_cals - total_cals_from_macros)
        self.assertTrue(diff <= 10, f"Calorie mismatch: Target {target_cals} vs Calc {total_cals_from_macros} (Diff: {diff})")
        
        # 3. Verify Protein Rule (2g per kg)
        expected_protein = weight * 2
        self.assertEqual(p_grams, expected_protein)

class WebViewsTests(APITestCase):
    def test_public_urls(self):
        """
        Test that public pages are accessible.
        """
        urls = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            reverse('blog_list'),
            reverse('legal'),
            reverse('password_reset'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed on {url}")

    def test_redirect_if_not_logged_in(self):
        """
        Test that protected pages redirect to login.
        """
        urls = [
            reverse('profile'),
            reverse('edit_profile'),
            reverse('change_password'),
            reverse('planner'),
            reverse('tools'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertIn('/login/', response.url)
