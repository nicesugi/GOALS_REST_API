from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.user_services import sign_up


class UserView(APIView):
    """
    post : 회원가입
    """

    def post(self, request):
        try:
            sign_up(request.data)
            return Response({"detail": "회원가입을 성공하였습니다"}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError as e:
            error = "\n".join(
                [str(value) for values in e.detail.values() for value in values]
            )
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(
                {"detail": "작성내용을 확인해주세요"}, status=status.HTTP_404_NOT_FOUND
            )
