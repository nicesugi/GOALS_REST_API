import json

from rest_framework.test import APIClient, APITestCase

from users.models import User


class TestUserViewAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existed_user_data = User.objects.create(
            username="test_user",
            email="test_user@example.com",
            password="test_user_password",
        )

    def test_user_view_def_post_ok(self):
        client = APIClient()

        create_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "user1password",
        }
        url = "/users"

        response = client.post(
            url, json.dumps(create_data), content_type="application/json"
        )
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["detail"], "회원가입을 성공하였습니다")

    def test_user_view_def_post_400_same_email(self):
        client = APIClient()
        create_data = {
            "username": "test_user",
            "email": "user1@example.com",
            "password": "user1password",
        }
        url = "/users"

        response = client.post(
            url, json.dumps(create_data), content_type="application/json"
        )
        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["detail"], "user의 사용자 계정은/는 이미 존재합니다.")

    def test_user_view_def_post_400_without_email(self):
        client = APIClient()

        create_data = {
            "username": "",
            "email": "user1@example.com",
            "password": "user1password",
        }
        url = "/users"

        response = client.post(
            url, json.dumps(create_data), content_type="application/json"
        )
        result = response.json()
        field = result["detail"].split("는")[0]
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["detail"], field + "는 blank일 수 없습니다.")

    def test_user_view_def_post_400_over_max_length_of_username(self):
        client = APIClient()

        create_data = {
            "username": "user123456789012345",
            "email": "user1@example.com",
            "password": "user1password",
        }
        url = "/users"

        response = client.post(
            url, json.dumps(create_data), content_type="application/json"
        )
        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["detail"], "이 필드의 글자 수가 12 이하인지 확인하십시오.")
