from django.test import TestCase
from rest_framework import exceptions

from users.models import User
from users.services.user_services import sign_up


class TestUserServices(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existed_user_data = User.objects.create(
            username="test_user", email="test_email@example.com", password="test_pw"
        )

    def test_sign_up(self):
        """
        회원가입하는 sign_up service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/ User object를 하나 생성
        """
        create_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "user1password",
        }
        users = User.objects.all().count()
        sign_up(create_data)
        after_created_user = User.objects.all().count()
        self.assertEqual(users, after_created_user - 1)

    def test_fail_sign_up_same_username(self):
        """
        회원가입하는 sign_up service 검증
        case : 중복되는 username을 입력했을 경우
        result : 실패/ ValidationError 발생
        """
        create_data = {
            "username": "test_user",
            "email": "user1@example.com",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_same_email(self):
        """
        회원가입하는 sign_up service 검증
        case : 중복되는 email을 입력했을 경우
        result : 실패/ ValidationError 발생
        """
        create_data = {
            "username": "user1",
            "email": "test_email@example.com",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_without_arg_create_data(self):
        """
        회원가입하는 sign_up service 검증
        case : 인자 값 create_data가 들어오지 않을 경우
        result : 실패/TypeError 발생
        """
        with self.assertRaises(TypeError):
            sign_up()

    def test_fail_sign_up_without_username(self):
        """
        회원가입하는 sign_up service 검증
        case : username값이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        create_data = {
            "username": "",
            "email": "user1@example.com",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_without_email(self):
        """
        회원가입하는 sign_up service 검증
        case : email값이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        create_data = {
            "username": "user1",
            "email": "",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_without_password(self):
        """
        회원가입하는 sign_up service 검증
        case : password값이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        create_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_over_max_length_of_username(self):
        """
        회원가입하는 sign_up service 검증
        case : username값이 길이 제한인 12자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        create_data = {
            "username": "user123456789012345",
            "email": "user1@example.com",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)

    def test_fail_sign_up_over_max_length_of_email(self):
        """
        회원가입하는 sign_up service 검증
        case : email값이 길이 제한인 50자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        create_data = {
            "username": "user1",
            "email": "user0011111222223333344444555556666677777@example.com",
            "password": "user1password",
        }
        with self.assertRaises(exceptions.ValidationError):
            sign_up(create_data)
