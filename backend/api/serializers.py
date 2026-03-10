from rest_framework import serializers
from .models import User, Article, Comment, Category, UserStats, WellnessPlan
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # On attend 'email' et 'password'
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                # On cherche le user par email
                user = User.objects.get(email=email)
                # On injecte le username pour que le parent puisse authentifier
                attrs['username'] = user.username
                # On peut retirer email s'il gêne, mais généralement kwargs accepte extra
            except User.DoesNotExist:
                # Laissez le parent gérer l'échec ou levez une erreur
                # Si on ne trouve pas le user, super().validate échouera probablement sur username manquant ou invalide
                pass
        
        return super().validate(attrs)

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = ('xp', 'level', 'current_streak', 'health_score', 
                  'fitness_score', 'recovery_score', 'lifestyle_score', 'consistency_score')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile', 'is_staff', 'marketing_opt_in', 'is_verified', 'date_joined')

    def get_profile(self, obj):
        # On construit l'objet "profile" attendu par le frontend
        # Il combine les champs du User (bio, avatar) et les stats (xp, level...)
        try:
            stats = obj.stats
        except UserStats.DoesNotExist:
            stats = None
            
        stats_data = UserStatsSerializer(stats).data if stats else {}
        
        return {
            'bio': obj.bio,
            'avatar': obj.avatar if obj.avatar else None,
            'level': stats_data.get('level', 1),
            'xp': stats_data.get('xp', 0),
            'current_streak': stats_data.get('current_streak', 0),
            'health_score': stats_data.get('health_score', 0),
            'scores': {
                'fitness': stats_data.get('fitness_score', 0),
                'recovery': stats_data.get('recovery_score', 0),
                'lifestyle': stats_data.get('lifestyle_score', 0),
                'consistency': stats_data.get('consistency_score', 0),
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user
    
    def update(self, instance, validated_data):
        # Custom update pour gérer le nested profile update (bio, avatar)
        instance.email = validated_data.get('email', instance.email)
        
        profile_data = self.initial_data.get('profile', {})
        if profile_data:
            instance.bio = profile_data.get('bio', instance.bio)
            instance.avatar = profile_data.get('avatar', instance.avatar)

        instance.save()
        return instance

class WellnessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessPlan
        fields = '__all__'
        read_only_fields = ('user', 'workout_plan', 'nutrition_plan', 'created_at')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'article', 'author', 'author_username', 'content', 'created_at')
        read_only_fields = ('author',)

class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    image_url = serializers.CharField(source='image', required=False, allow_null=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'slug', 'author', 'author_username', 'category', 'category_name', 'category_slug', 'content', 'image_url', 'is_published', 'created_at', 'updated_at', 'comments', 'likes_count', 'is_liked')
        read_only_fields = ('author', 'slug')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
