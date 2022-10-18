from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.service.user_services import (
    create_user,
)

class UserView(APIView):
    """
    post : 회원가입
    """
    def post(self, request: Request):
        create_user(request.data)
        return Response({'detail': '회원가입을 성공하였습니다'}, status=status.HTTP_201_CREATED)