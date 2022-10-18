from django.db.models import Count, Q
from typing import Dict
from posts.models import (
    Like, Post, TagName,
    )
from posts.serializers import PostSerializer, PostDetailSerializer
from users.models import User

def read_posts(order_by: str, reverse: int) -> Post:
    """
    Args:
        order_by (str) : 정렬 기준 (작성일, 조회수, 좋아요수 중 1개)
        reverse (int) : 정렬 기준(1-내림차순 / 0-오름차순)
        
    Returns:
        Post : 정렬(작성일/조회수/좋아요수/내림차순/오름차순)이 된 게시글의 QuerySet
    """
    if reverse == 1:
        reverse = '-'
    elif reverse == 0:
        reverse = ''
    if order_by == 'created_date' or order_by == 'views': 
        posts = Post.objects.all().order_by(reverse + order_by)
    elif order_by == 'likes':
        posts = Post.objects.all().annotate(like_count=Count('like')).order_by(reverse + 'like_count')
    return posts

def search_posts(posts: Post, search: str) -> Post:
    """
    Args:
        posts (QuerySet) : 정렬이 된 게시글
        search (str) : 검색 키워드

    Returns:
        Post : 정렬,검색이 된 게시글의 QuerySet
    """
    posts = posts.filter(
        Q(title__icontains=search) | Q(content__icontains=search)
    )
    return posts

def filtering_posts(posts: Post, tags: str) -> Post:
    """
    Args:
        posts (QuerySet) : 정렬,검색이 된 게시글
        tags (str) : 필터링할 해시태그

    Returns:
        Post : 정렬,검색,태그필터링이 된 게시글의 QuerySet
    """
    if tags == '':
        query_set = posts.all()
    else:    
        tags = tags.split(',')
        query_set = posts.none()
        for tag in tags:
            query_set = query_set | posts.filter(posttag__tags__name__icontains=tag).distinct()
    return query_set

def pagination_posts(posts: Post, page_size: int, page: int) -> PostSerializer:
    """
    Args:
        posts (QuerySet) : 정렬,검색,태그필터링이 된 게시글
        page_size (int) : 한 페이지에 보여지는 게시글 수
        page (int) : 보고자하는 페이지

    Returns:
        PostSerializer : 정렬,검색,태그필터링,페이징이 된 게시글들
    """
    start_post = page_size * (page-1)
    end_post = page * page_size
    posts_serializer = PostSerializer(posts[start_post:end_post], many=True).data
    return posts_serializer

def create_post(create_data: Dict[str, str], user: User) -> None:
    """
    Args:
        create_data (Dict[str, str]) : {
            "writer" : user,
            "title" : post의 title,
            "content" : post의 content,
            "tags" : post의 hashtags /예시)"#제목,#내용,#태그"
            }
        user (int) : 로그인이 되어있는 작성자의 FK
        
    Returns:
        None
    """
    create_data['writer'] = user.id
    post_data_serializer = PostSerializer(data=create_data)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()
    
    tags_data_list = create_data['tags'].replace(',' , '').split('#')
    del tags_data_list[0]
    for tag in tags_data_list:
        TagName.objects.get_or_create(name=tag)
        post_data_serializer.instance.tags.add(TagName.objects.get(name=tag))
    
def edit_post(edit_data: Dict[str, str], user: User, post_id: int) -> None:
    """
    Args:
        edit_data (Dict[str, str]) : {
            "title" : post의 title,
            "content" : post의 content,
            "tags" : post의 hashtags /예시)"#제목,#내용,#태그"
            }
        user (int) : 로그인이 되어있는 작성자의 FK
        post_id (int) : 수정하고자 하는 게시글의 PK

    Returns:
        None
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    post_serializer = PostSerializer(post, data=edit_data, partial=True)
    if post_serializer.is_valid(raise_exception=True):
        post_serializer.save()
        
    tags_data_list = edit_data['tags'].replace(',' , '').split('#')
    del tags_data_list[0]
    for tag in tags_data_list:
        TagName.objects.get_or_create(name=tag)
        post_serializer.instance.tags.add(TagName.objects.get(name=tag))
    
def soft_delete_post(user: User, post_id: int) -> None:
    """
    Args:
        user (int) : 로그인이 되어있는 작성자의 FK
        post_id (int) : 비활성화하고자 하는 게시글의 PK
        
    Returns:
        None
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    post.is_active = False
    post.save()
    
def recover_post(user: User, post_id: int) -> None:
    """
    Args:
        user (int) : 로그인이 되어있는 작성자의 FK
        post_id (int) : 복구하고자 하는 게시글의 PK
        
    Returns:
        None
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    if post.is_active == False:
        post.is_active = True
        post.save()
        
def hard_delete_post(user: User, post_id: int) -> None:
    """
    Args:
        user (int) : 로그인이 되어있는 작성자의 FK
        post_id (int) : 완전 삭제하고자 하는 게시글의 PK
        
    Returns:
        None
    """
    post = Post.objects.get(id=post_id, writer_id=user)
    post.delete()
    
def read_detail_post(post_id: int) -> PostDetailSerializer:
    """
    Args:
        post_id (int) : 자세한 내용을 열람하고자 하는 게시글의 PK

    Returns:
        PostDetailSerializer : 해당 게시글의 상세정보
    """
    post = Post.objects.get(id=post_id)
    post.update_views
    post_serializer = PostDetailSerializer(post).data
    return post_serializer

def like_post(user: User, post_id: int) -> bool:
    """
    Args:
        user (int) : 좋아요/좋아요취소 하는 사용자의 FK
        post_id (int) : 좋아요/좋아요취소 하는 게시글의 PK

    Returns:
        True : "좋아요"
        False : "좋아요취소" 
    """
    post = Post.objects.get(id=post_id)
    getted_like_obj, created_like_obj = Like.objects.get_or_create(user=user, post=post)
    if created_like_obj:
        return True
    getted_like_obj.delete()
    return False