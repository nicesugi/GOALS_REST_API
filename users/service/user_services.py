from typing import Dict
from users.serializers import UserSignupSerializer


def create_user(create_data: (Dict[str, str])) -> None:
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
    user_data_serializer = UserSignupSerializer(data=create_data)
    user_data_serializer.is_valid(raise_exception=True)
    user_data_serializer.save()
