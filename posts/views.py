from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts import serializers

from posts.service.post_services import (
    read_posts,
    create_post,
)

class PostView(APIView):
    def get(self, request):
        posts = read_posts()
        return Response(posts, status=status.HTTP_200_OK)
    
    def post(self, request):
        create_post(request.data, request.user)
        return Response({'detail': '게시글이 작성되었습니다'}, status=status.HTTP_201_CREATED)