from rest_framework.test import APIClient, APITestCase
from posts.models import Like, Post, PostTag, TagName
from users.models import User
import json


class TestAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user',
            email='test_email@naver.com',
            password='test_pw'
        )

        tag_data1 = TagName.objects.create(name='sns')

        post_data1 = Post.objects.create(
            writer=user,
            title='test_title',
            content='test_content',
            is_active=True,
            views=60,
            created_date='2022-10-16 08:00:00.000000'
        )
        post_data2 = Post.objects.create(
            writer=user,
            title='test_title2',
            content='test_content2',
            is_active=True,
            views=20,
            created_date='2022-10-17 08:00:00.000000'
        )

        post_tag_data1 = PostTag.objects.create(
            tags=tag_data1, posts=post_data1)
        post_tag_data2 = PostTag.objects.create(
            tags=tag_data1, posts=post_data2)

        like_data1 = Like.objects.create(post=post_data1, user=user)

    def test_post_view_def_get_ok(self):
        client = APIClient()

        url = '/posts/'
        response = client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'test_title2')

    def test_post_view_def_post_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        create_data = {
            'title': 'test_title',
            'content': 'test_content',
            'tags': '#sns',
            'is_active': True,
            'views': 60,
            'created_date': '2022-10-16 08:00:00.000000'
        }

        url = '/posts/'
        response = client.post(
            url,
            json.dumps(create_data),
            content_type="application/json"
        )
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['detail'], '게시글이 작성되었습니다')

    def test_post_view_def_put_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')
        edit_data = {
            'title': 'test_edit_title',
            'content': 'test_edit_content',
            'tags': '#sns,#apple',
            'is_active': True,
            'views': 60,
            'created_date': '2022-10-16 08:00:00.000000'
        }

        url = '/posts/' + str(post.id)
        response = client.put(
            url,
            json.dumps(edit_data),
            content_type="application/json"
        )
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['detail'], '게시글이 수정되었습니다')

    def test_post_view_def_delete_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')

        url = '/posts/' + str(post.id)
        response = client.delete(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['detail'], '게시글이 비활성화가 되었습니다')

    def test_existence_post_view_def_post_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')

        url = '/posts/' + str(post.id) + '/existence'
        response = client.post(url)
        result = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['detail'], '게시글이 복구되었습니다')

    def test_existence_post_view_def_delete_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')

        url = '/posts/' + str(post.id) + '/existence'
        response = client.delete(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['detail'], '게시글이 삭제되었습니다')

    def test_post_detail_view_def_get_ok(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')

        url = '/posts/detail/' + str(post.id)
        response = client.get(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['title'], 'test_title')

    def test_like_view_def_post_ok_case_true(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title2', content='test_content2')

        url = '/posts/' + str(post.id) + '/like'
        response = client.post(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['detail'], '좋아요 했습니다')
        self.assertEqual(result['like_count'], 1)

    def test_like_view_def_post_ok_case_false(self):
        client = APIClient()

        user = User.objects.get(username='test_user')
        client.force_authenticate(user=user)
        post = Post.objects.get(title='test_title', content='test_content')

        url = '/posts/' + str(post.id) + '/like'
        response = client.post(url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['detail'], '좋아요를 취소했습니다')
        self.assertEqual(result['like_count'], 0)
