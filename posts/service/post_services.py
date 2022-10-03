from django.db.models import Q
from posts.serializers import PostSerializer, PostDetailSerializer
from posts.models import Like, Post

def read_posts(order_by, reverse):
    """
    Args:
        order_by : 작성일, 조회수 중 1개
        reverse : 1 > 내림차순  / 0 > 오름차순
    Returns:
        Post
    """
    
    if reverse == 1:
        reverse = '-'
    elif reverse == 0:
        reverse = ''
        
    posts = Post.objects.all().order_by(reverse + order_by)
    return posts

def search_posts(posts, search):
    """
    Args:
        posts : 정렬이 완료된 게시글
        search : 게시글 중 제목이나 내용에 해당 값이 들어있는 게시글만 반환

    Returns:
        Post
    """
    posts = posts.filter(
        Q(title__icontains=search) | Q(content__icontains=search)
    )
    return posts
    
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

def like_post(user, post_id):
    """
    Args:
        user : users.User FK | 좋아요/좋아요취소 하는 사용자
        post_id : 좋아요/좋아요취소 하는 게시글의 id

    Returns:
        True : "좋아요",
        False : "좋아요취소" 
    """
    post = Post.objects.get(id=post_id)
    getted_like_obj, created_like_obj = Like.objects.get_or_create(user=user, post=post)
    if created_like_obj:
        return True
    getted_like_obj.delete()
    return False