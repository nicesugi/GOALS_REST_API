from users.serializers import UserSignupSerializer

def create_user(create_data):
    """
    Args:
        "email" : user의 email,
        "password" : user의 password
        }
    """
    user_data_serializer = UserSignupSerializer(data=create_data)
    user_data_serializer.is_valid(raise_exception=True)
    user_data_serializer.save()