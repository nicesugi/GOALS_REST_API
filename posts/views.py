from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.service.post_services import (
    read_posts,
    create_post,
    edit_post,
    deactivate_post,
    recover_post,
    read_detail_post,
    like_post
)

class PostView(APIView):
    def get(self, request):
        posts = read_posts()
        return Response(posts, status=status.HTTP_200_OK)
    
    def post(self, request):
        create_post(request.data, request.user)
        return Response({'detail': '게시글이 작성되었습니다'}, status=status.HTTP_201_CREATED)
    
    def put(self, request, post_id):
        edit_post(request.data, request.user, post_id)
        return Response({'detail': '게시글이 수정되었습니다'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        deactivate_post(request.user, post_id)
        return Response({'detail': '게시글이 비활성화가 되었습니다'}, status=status.HTTP_200_OK)
    
class RecoverPostView(APIView):
    def post(self, request, post_id):
        recover_post(request.user, post_id)
        return Response({'detail': '게시글이 복구되었습니다'}, status=status.HTTP_200_OK)

class PostDetailView(APIView):
    def get(self, request, post_id):
        post = read_detail_post(post_id)
        return Response(post, status=status.HTTP_200_OK)


class LikeView(APIView):
    def post(self, request, post_id):
        if like_post(request.user, post_id):
            return Response({'detail': '좋아요 했습니다'}, status=status.HTTP_200_OK)
        return Response({'detail': '좋아요를 취소했습니다'}, status=status.HTTP_200_OK)
        
        