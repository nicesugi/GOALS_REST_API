from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Like
from posts.services.post_services import (
    read_posts,
    search_posts,
    filtering_posts,
    pagination_posts,
    create_post,
    edit_post,
    soft_delete_post,
    recover_post,
    hard_delete_post,
    read_detail_post,
    like_post
)

class PostView(APIView):
    """
    get : 게시글 목록 조회
    post : 게시글 작성
    put : 게시글 수정
    delete : 게시글 비활성화(soft_delete)
    """
    def get(self, request):
        order_by = self.request.query_params.get('order_by', 'created_date')
        reverse = int(self.request.query_params.get('reverse', 1))
        search = self.request.query_params.get('search')
        tags = self.request.query_params.get('tags')
        page_size = int(self.request.query_params.get('page_size', 10))
        page = int(self.request.query_params.get('page', 1))
        
        posts = read_posts(order_by, reverse)
        posts = search_posts(posts, search)
        posts = filtering_posts(posts, tags)
        posts = pagination_posts(posts, page_size, page)
        return Response(posts, status=status.HTTP_200_OK)
    
    def post(self, request):
        create_post(request.data, request.user)
        return Response({'detail': '게시글이 작성되었습니다'}, status=status.HTTP_201_CREATED)
    
    def put(self, request, post_id):
        edit_post(request.data, request.user, post_id)
        return Response({'detail': '게시글이 수정되었습니다'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        soft_delete_post(request.user, post_id)
        return Response({'detail': '게시글이 비활성화가 되었습니다'}, status=status.HTTP_200_OK)
    
class ExistencePostView(APIView):
    """
    post : 비활성화된 게시글 복구
    delete : 게시글 완전 삭제(hard_delete)
    """
    def post(self, request, post_id):
        recover_post(request.user, post_id)
        return Response({'detail': '게시글이 복구되었습니다'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        hard_delete_post(request.user, post_id)
        return Response({'detail': '게시글이 삭제되었습니다'}, status=status.HTTP_200_OK)

class PostDetailView(APIView):
    """
    get : 게시글 상세 조회
    """
    def get(self, request, post_id):
        post = read_detail_post(post_id)
        return Response(post, status=status.HTTP_200_OK)

class LikeView(APIView):
    """
    post : 게시글 좋아요/좋아요취소 + 좋아요 수 카운트
    """
    def post(self, request, post_id):
        if like_post(request.user, post_id):
            like_count = Like.objects.filter(post=post_id).count()
            return Response({'detail': '좋아요 했습니다', 'like_count': like_count}, status=status.HTTP_200_OK)
        return Response({'detail': '좋아요를 취소했습니다'}, status=status.HTTP_200_OK)