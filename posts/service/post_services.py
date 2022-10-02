from posts.serializers import PostSerializer
from posts.models import Post

def read_posts():
    """
    Returns:
        PostSerializer
    """
    posts = Post.objects.all().order_by('-created_date')
    posts_serializer = PostSerializer(posts, many=True).data
    return posts_serializer
    
def create_post(create_data):
    """
    Args:
        "writer" : post의 writer,
        "title" : post의 title,
        "content" : post의 content,
        "tags" : post의 hashtags, 예시)"#제목,#내용,#태그"
    """
    post_data_serializer = PostSerializer(data=create_data)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()

    tags_data_list = create_data['tags'].replace(',' , '').split('#')
    del tags_data_list[0]
    for tag in tags_data_list:
        Post.objects.last().tags.add(tag)
        
