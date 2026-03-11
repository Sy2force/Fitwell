from django.http import HttpResponse
import csv
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment, Category, User, WellnessPlan, UserStats
from .serializers import ArticleSerializer, CommentSerializer, CategorySerializer, UserSerializer, WellnessPlanSerializer, EmailTokenObtainPairSerializer
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .services import generate_wellness_plan

# -----------------------------------------------------------------------------
# AUTHENTIFICATION
# -----------------------------------------------------------------------------
class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Vue de login qui utilise l'email au lieu du username.
    """
    serializer_class = EmailTokenObtainPairSerializer

# -----------------------------------------------------------------------------
# WELLNESS PLANNER
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# GESTION DES UTILISATEURS
# -----------------------------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les utilisateurs.
    Permet de voir la liste, chercher par nom/email.
    L'inscription (register) est ouverte à tous.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_permissions(self):
        # N'importe qui peut s'inscrire, pas besoin d'être connecté.
        if self.action == 'register':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def register(self, request):
        # Action personnalisée pour créer un compte facilement
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Endpoint pour récupérer ou mettre à jour son propre profil.
        URL: /api/users/me/
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def export(self, request):
        """
        Export des utilisateurs en CSV (Admin seulement).
        URL: /api/users/export/
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom d\'utilisateur', 'Email', 'Staff', 'Date d\'inscription'])

        users = User.objects.all().values_list('id', 'username', 'email', 'is_staff', 'date_joined')
        for user in users:
            writer.writerow(user)

        return response

# -----------------------------------------------------------------------------
# CATÉGORIES (Force, Nutrition, etc.)
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# ARTICLES DE BLOG
# -----------------------------------------------------------------------------
class ArticleViewSet(viewsets.ModelViewSet):
    """
    API principale pour les articles.
    - Lecture : Pour tout le monde.
    - Écriture / Modification : Seulement Admin.
    """
    # On charge l'auteur et la catégorie direct pour éviter de faire 50 requêtes SQL
    queryset = Article.objects.select_related('author', 'category').prefetch_related('comments').order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # Filtres puissants : par catégorie, auteur, recherche texte
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'category__slug']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

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
            # Create comment
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, article=article)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# COMMENTAIRES
# -----------------------------------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    """
    Gestion des commentaires sur les articles.
    Même logique : tu ne peux modifier que TES commentaires.
    """
    queryset = Comment.objects.select_related('author', 'article').order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['article', 'author']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

