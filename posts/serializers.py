from rest_framework import serializers
from .models import Like, Post

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    
    def get_tags(self, obj):
        hashtag_list = []
        for tag in obj.tags.all():
            hashtag_list.append('#' + tag.name)
        return hashtag_list
    
    def get_likes(self, obj):
        return Like.objects.filter(post=obj.id).count()
    
    class Meta:
        model = Post
        fields = ['id', 'writer', 'title', 'content', 'tags', 'views', 'likes', 'created_date', 'updated_date', 'is_active']
        extra_kwargs = {
            'content': {'write_only': True},
        }
        
class PostDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    
    def get_tags(self, obj):
        hashtag_list = []
        for tag in obj.tags.all():
            hashtag_list.append('#' + tag.name)
        return hashtag_list
    
    class Meta:
        model = Post
        fields = '__all__'