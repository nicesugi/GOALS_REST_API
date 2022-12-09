from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.user_services import sign_up


class UserView(APIView):
    """
    post : 회원가입
    """

    def post(self, request):
        if request.data == {}:
            return Response(
                {"detail": "입력받은 값이 없습니다. 다시 확인해주세요"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            sign_up(request.data)
            return Response({"detail": "회원가입을 성공하였습니다"}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError as e:
            error = "\n".join(
                [str(value) for values in e.detail.values() for value in values]
            )
            if "blank일 수 없습니다" in error:
                error = "\n".join(
                    [
                        (keys + value.split("필드")[1])
                        for keys, values in e.detail.items()
                        for value in values
                    ]
                )
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
