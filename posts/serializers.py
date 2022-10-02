from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    hashtags = serializers.SerializerMethodField()
    
    def get_hashtags(self, obj):
        hashtag_list = []
        for tag in obj.tags.all():
            hashtag_list.append('#' + tag.name)
        return hashtag_list
    
    class Meta:
        model = Post
        fields = ['id', 'writer', 'title', 'content', 'hashtags', 'views', 'created_date', 'updated_date', 'is_active']
        extra_kwargs = {
            'content': {'write_only': True},
        }