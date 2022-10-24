from typing import Dict
from users.serializers import UserSignUpSerializer


def sign_up(create_data: (Dict[str, str])) -> None:
    """
    Args:
        create_data (Dict[str, str]) : {
            "username" : user의 username,
            "email" : user의 email,
            "password" : user의 password
        }

    Returns:
        None

    """
    serializer = UserSignUpSerializer(data=create_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
