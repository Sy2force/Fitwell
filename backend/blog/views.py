from django.db import models
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Category, Comment
from .serializers import (
    ArticleSerializer, ArticleDetailSerializer, CategorySerializer,
    CommentSerializer
)
from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories.

    Endpoints:
    - GET /api/categories/ : List all categories
    - GET /api/categories/{slug}/ : Retrieve a specific category
    - GET /api/categories/{slug}/articles/ : List all articles in a specific category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def articles(self, request, slug=None):
        category = self.get_object()
        articles = Article.objects.filter(category=category, is_published=True)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing articles.

    Endpoints:
    - GET /api/articles/ : List all articles (paginated)
    - POST /api/articles/ : Create a new article (Auth required)
    - GET /api/articles/{id}/ : Retrieve a specific article
    - PUT/PATCH /api/articles/{id}/ : Update an article (Author only)
    - DELETE /api/articles/{id}/ : Delete an article (Author only)
    - GET /api/articles/search/?q=... : Search articles by title or content
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'category__slug': ['exact'],
        'is_published': ['exact'],
        'author': ['exact'],
        'author__username': ['exact']
    }
    search_fields = ['title', 'content', 'category__name']
    ordering_fields = ['created_at', 'title', 'likes']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        articles = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    # Custom action to search articles (alternative to ?search=)
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            articles = self.queryset.filter(models.Q(title__icontains=query) | models.Q(content__icontains=query))
        else:
            articles = self.queryset

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user
        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
            return Response({'status': 'unliked', 'likes_count': article.likes.count()}, status=status.HTTP_200_OK)
        else:
            article.likes.add(user)
            return Response({'status': 'liked', 'likes_count': article.likes.count()}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        article = self.get_object()

        if request.method == 'GET':
            comments = article.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, article=article)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
