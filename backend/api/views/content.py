from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Article, Category, Comment, Tag
from api.serializers import ArticleSerializer, CategorySerializer, CommentSerializer, TagSerializer
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste les tags disponibles. Lecture seule (les tags sont créés
    automatiquement à la création d'articles/commentaires).
    URL: /api/tags/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    pagination_class = None

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Simple liste des catégories.
    On peut les trier ou chercher par nom.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'])
    def articles(self, request, slug=None):
        """
        Récupère les articles d'une catégorie spécifique.
        URL: /api/categories/{slug}/articles/
        """
        category = self.get_object()
        articles = Article.objects.filter(category=category).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API principale pour les articles.
    - Lecture : tout le monde (anonyme inclus).
    - Création : tout utilisateur authentifié.
    - Modification / Suppression : seul l'auteur (ou admin).
    """
    # On charge l'auteur et la catégorie direct pour éviter de faire 50 requêtes SQL
    queryset = (Article.objects
                .select_related('author', 'category')
                .prefetch_related('comments', 'tags')
                .order_by('-created_at'))
    serializer_class = ArticleSerializer
    # Cahier des charges : utilisateur authentifié peut créer,
    # seul l'auteur (ou admin) peut modifier/supprimer.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Filtres : par catégorie, auteur, tag, recherche texte
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'category__slug', 'tags__name', 'tags__slug']
    search_fields = ['title', 'content', 'tags__name']
    ordering_fields = ['created_at', 'title', 'author__username']

    def perform_create(self, serializer):
        # On assigne automatiquement l'auteur à l'utilisateur connecté
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Action pour liker/unliker un article.
        URL: /api/articles/{id}/like/
        """
        article = self.get_object()
        user = request.user
        
        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
            return Response({'status': 'unliked', 'likes_count': article.likes.count()})
        else:
            article.likes.add(user)
            return Response({'status': 'liked', 'likes_count': article.likes.count()})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Récupère les articles de l'utilisateur connecté.
        URL: /api/blog/articles/me/
        """
        articles = Article.objects.filter(author=request.user).order_by('-created_at')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        """
        Gère les commentaires d'un article spécifique (List / Create).
        URL: /api/articles/{id}/comments/
        """
        article = self.get_object()
        
        if request.method == 'GET':
            comments = article.comments.all().order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Injection de l'article via l'URL (route imbriquée)
            data = {**request.data, 'article': article.id}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, article=article)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """
    Gestion des commentaires sur les articles.
    Même logique : tu ne peux modifier que TES commentaires.
    """
    queryset = (Comment.objects
                .select_related('author', 'article')
                .prefetch_related('tags')
                .order_by('-created_at'))
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['article', 'author', 'tags__name', 'tags__slug']
    search_fields = ['content', 'tags__name']
    ordering_fields = ['created_at', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
