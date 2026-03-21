from rest_framework import serializers
from api.models import Article, Comment, Category


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
