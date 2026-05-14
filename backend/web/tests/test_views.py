from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from api.models import User, Article, Category, Comment

class WebTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.is_onboarded = True
        self.user.save()
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.article = Article.objects.create(
            title='Test Article', 
            content='Test Content', 
            author=self.user, 
            category=self.category,
            is_published=True
        )

    def test_planner_view_requires_login(self):
        """
        Verify that the planner page redirects to login if not authenticated.
        """
        response = self.client.get(reverse('planner'))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_planner_view_authenticated(self):
        """
        Verify that the planner page loads for an authenticated user.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('planner'))
        self.assertEqual(response.status_code, 200)
        # Language-agnostic: checks for the translated "Strategy" heading
        self.assertContains(response, _("Stratégie"))

    def test_blog_comment_submission(self):
        """
        Verify that an authenticated user can post a comment.
        """
        self.client.force_login(self.user)
        url = reverse('article_detail', args=[self.article.slug])
        data = {'content': 'This is a test comment.'}
        response = self.client.post(url, data)
        
        # Should redirect back to article page
        self.assertEqual(response.status_code, 302)
        
        # Verify comment was created
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'This is a test comment.')

    def test_article_like(self):
        """
        Verify that a user can like an article.
        """
        self.client.force_login(self.user)
        url = reverse('like_article', args=[self.article.slug])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.article.likes.filter(id=self.user.id).exists())

    def test_edit_profile(self):
        """
        Verify that a user can update their profile.
        """
        self.client.force_login(self.user)
        url = reverse('edit_profile')
        data = {
            'email': 'newemail@test.com',
            'bio': 'New Bio',
            'avatar': 'http://image.url'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect to profile
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@test.com')
        self.assertEqual(self.user.bio, 'New Bio')

    def test_change_password(self):
        """
        Verify that a user can change their password.
        """
        self.client.force_login(self.user)
        url = reverse('change_password')
        data = {
            'old_password': 'password',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect to profile
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_blog_search_and_filter(self):
        """
        Verify that blog search and category filtering work.
        """
        # Create another article in a different category
        cat2 = Category.objects.create(name='Nutrition', slug='nutrition')
        Article.objects.create(
            title='Nutrition Basics',
            content='Eat healthy.',
            author=self.user,
            category=cat2,
            is_published=True
        )

        # 1. Test Search
        response = self.client.get(reverse('blog_list') + '?q=Nutrition')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutrition Basics')
        self.assertNotContains(response, 'Test Article') # Should be filtered out

        response = self.client.get(reverse('blog_list') + '?category=nutrition')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutrition Basics')
        self.assertNotContains(response, 'Test Article') # Should be filtered out

    def test_delete_comment(self):
        """
        Verify that a user can delete their own comment.
        """
        self.client.force_login(self.user)
        
        # Create a comment
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content="To be deleted"
        )
        
        # Delete it
        url = reverse('delete_comment', args=[comment.id])
        response = self.client.post(url)
        
        # Check redirection
        self.assertEqual(response.status_code, 302)
        
        # Check it's gone
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        
    def test_delete_other_user_comment(self):
        """
        Verify that a user cannot delete another user's comment.
        """
        other_user = User.objects.create_user(username='other', password='password')
        comment = Comment.objects.create(
            article=self.article,
            author=other_user,
            content="Other user comment"
        )
        
        self.client.force_login(self.user)
        url = reverse('delete_comment', args=[comment.id])
        response = self.client.post(url)
        
        # Should redirect but NOT delete
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())

    def test_dashboard_view(self):
        """
        Verify that the dashboard requires login and loads correctly with context data.
        """
        url = reverse('dashboard')
        
        # 1. Unauthenticated -> Redirect
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # 2. Authenticated -> 200 OK
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/dashboard.html')
        self.assertIn('avg_sleep', response.context)
        self.assertIn('today_events', response.context)


