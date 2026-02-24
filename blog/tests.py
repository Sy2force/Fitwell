from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article, Category, User

class BlogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Health')
        self.article = Article.objects.create(
            title='Test Article',
            content='Test Content',
            author=self.user,
            category=self.category,
            is_published=True
        )
        self.url = reverse('article-list')

    def test_get_articles(self):
        """Test retrieving list of articles"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_article_authenticated(self):
        """Test creating an article with authentication"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Article',
            'content': 'New Content',
            'category': self.category.id,
            'is_published': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)

    def test_create_article_unauthenticated(self):
        """Test creating an article without authentication fails"""
        data = {
            'title': 'New Article',
            'content': 'New Content',
            'category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_article_as_author(self):
        """Test updating an article as the author"""
        self.client.force_authenticate(user=self.user)
        url = reverse('article-detail', kwargs={'pk': self.article.pk})
        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': self.category.id,
            'is_published': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')

    def test_update_article_as_non_author(self):
        """Test updating an article as a non-author fails"""
        other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.force_authenticate(user=other_user)
        url = reverse('article-detail', kwargs={'pk': self.article.pk})
        data = {
            'title': 'Hacked Title',
            'content': 'Hacked Content',
            'category': self.category.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article_as_author(self):
        """Test deleting an article as the author"""
        self.client.force_authenticate(user=self.user)
        url = reverse('article-detail', kwargs={'pk': self.article.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_search_articles(self):
        """Test searching articles"""
        Article.objects.create(
            title='Fitness Tips',
            content='Great fitness advice',
            author=self.user,
            category=self.category,
            is_published=True
        )
        url = reverse('article-search')
        response = self.client.get(url, {'q': 'fitness'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_categories(self):
        """Test retrieving list of categories"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if at least the category we created exists
        self.assertGreaterEqual(len(response.data), 1)

    def test_add_comment_authenticated(self):
        """Test adding a comment with authentication"""
        self.client.force_authenticate(user=self.user)
        url = reverse('article-comments', kwargs={'pk': self.article.pk})
        data = {'content': 'Great article!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.article.comments.count(), 1)

    def test_add_comment_unauthenticated(self):
        """Test adding a comment without authentication fails"""
        url = reverse('article-comments', kwargs={'pk': self.article.pk})
        data = {'content': 'Great article!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_article_comments(self):
        """Test retrieving comments for an article"""
        from .models import Comment
        Comment.objects.create(
            article=self.article,
            user=self.user,
            content='Test comment'
        )
        url = reverse('article-comments', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_like_article(self):
        """Test liking and unliking an article"""
        self.client.force_authenticate(user=self.user)
        url = reverse('article-like', kwargs={'pk': self.article.pk})
        
        # Like
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')
        self.assertEqual(self.article.likes.count(), 1)
        
        # Unlike
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unliked')
        self.assertEqual(self.article.likes.count(), 0)

    def test_update_user_profile(self):
        """Test updating user profile bio and avatar"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-profile')
        data = {
            'bio': 'Updated bio',
            'avatar': 'https://example.com/avatar.jpg'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'Updated bio')
        self.assertEqual(self.user.avatar, 'https://example.com/avatar.jpg')
