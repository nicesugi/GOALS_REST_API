from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.service.post_services import (
    create_post,
)

class PostView(APIView):
    def post(self, request):
        create_post(request.data)
        return Response({'detail': '게시글이 작성되었습니다'}, status=status.HTTP_201_CREATED)