from posts.serializers import PostSerializer, PostDetailSerializer
from posts.models import Post

def read_posts():
    """
    Returns:
        PostSerializer
    """
    posts = Post.objects.all().order_by('-created_date')
    posts_serializer = PostSerializer(posts, many=True).data
    return posts_serializer
    
def create_post(create_data, user):
    """
    Args:
        create_data : {
            "writer" : post의 writer,
            "title" : post의 title,
            "content" : post의 content,
            "tags" : post의 hashtags, 예시)"#제목,#내용,#태그"
            },
        user : users.User FK | 글을 작성하는 현재 로그인이 되어있는 user
    """
    create_data['writer'] = user.id
    post_data_serializer = PostSerializer(data=create_data)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()

    tags_data_list = create_data['tags'].replace(',' , '').split('#')
    del tags_data_list[0]
    for tag in tags_data_list:
        Post.objects.last().tags.add(tag)
        
def edit_post(edit_data, user, post_id):
    """
    Args:
        edit_data : {
            "title" : post의 title,
            "content" : post의 content,
            "tags" : post의 hashtags, 예시)"#제목,#내용,#태그"
            }
        user : users.User FK | 글을 수정하는 현재 로그인이 되어있는 user
        post_id : 수정하고자 하는 게시글의 id

    Returns:
        PostSerializer
    """
    edit_data['writer'] = user.id
    post = Post.objects.get(id=post_id)
    
    post_serializer = PostSerializer(post, data=edit_data, partial=True)
    if post_serializer.is_valid(raise_exception=True):
        post_serializer.save()
        
        tags_data_list = edit_data['tags'].replace(',' , '').split('#')
        del tags_data_list[0]
        for tag in tags_data_list:
            post.tags.add(tag)

        return post_serializer.data
    
def deactivate_post(user, post_id):
    """
    Args:
        user : users.User FK | 글을 비활성화하는 현재 로그인이 되어있는 user
        post_id : 비활성화하고자 하는 게시글의 id
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    post.is_active = False
    post.save()
    
def recover_post(user, post_id):
    """
    Args:
        user : users.User FK | 작성한 사용자
        post_id : 복구하고자 하는 게시글의 id
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    if post.is_active == False:
        post.is_active = True
        post.save()
        
def read_detail_post(post_id):
    """
    Args:
        post_id : 자세한 내용을 열람하고자 하는 게시글의 id

    Returns:
        PostDetailSerializer
    """
    post = Post.objects.get(id=post_id)
    post.update_views
    post_serializer = PostDetailSerializer(post).data
    return post_serializer