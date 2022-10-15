from django.test import TestCase
from django.test.utils import CaptureQueriesContext 
from django.db import connection
from rest_framework import exceptions
from users.models import User
from posts.models import Post
from posts.services.post_services import (
    create_post,
    edit_post,
)

class TestService(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username = 'test_user',
            email = 'test_email@naver.com',
            password = 'test_pw'
            )
        
        created_data = Post.objects.create(
            writer = user,
            title = 'test_title',
            content = 'test_content',
            tags = '#sns, #like, #post'
            )
    def test_create_post(self):
        """
        게시물을 작성하는 create_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/쿼리수를 확인하여 Post object를 하나 생성
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : 'test_title',
            'content' : 'test_content',
            'tags' : '#sns, #like, #post'
            }
        # with CaptureQueriesContext(connection) as ctx:
        #     create_post(create_data, user)
        # ctx.captured_queries
        with self.assertNumQueries(39):
            create_post(create_data, user)
            
    def test_fail_create_post_without_arg_user(self):
        """
        게시물을 작성하는 create_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        create_data = {
            'title' : 'test_title',
            'content' : 'test_content',
            'tags' : '#sns, #like, #post'
            }
        with self.assertRaises(TypeError):
            create_post(create_data)
            
    def test_fail_create_post_without_arg_create_data(self):
        """
        게시물을 작성하는 create_post service 검증
        case : 인자 값 중 create_data가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            create_post(user)
        
    def test_fail_create_post_without_title(self):
        """
        게시물을 작성하는 create_post service 검증
        case : title이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : '',
            'content' : 'test_content',
            'tags' : '#sns, #like, #post'
            }
        with self.assertRaises(exceptions.ValidationError):
            create_post(create_data, user)
            
    def test_fail_create_post_without_content(self):
        """
        게시물을 작성하는 create_post service 검증
        case : content이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : 'test_title',
            'content' : '',
            'tags' : '#sns, #like, #post'
            }
        with self.assertRaises(exceptions.ValidationError):
            create_post(create_data, user)

    def test_create_post_without_tags(self):
        """
        게시물을 작성하는 create_post service 검증
        case : tags가 빈 값일 경우
        result : 정상/Post object를 하나 생성
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : 'test_title',
            'content' : 'test_content',
            'tags' : ''
            }
        all_post_count = Post.objects.all().count()
        create_post(create_data, user)
        after_all_post_count = Post.objects.all().count()
        self.assertEqual(all_post_count, after_all_post_count-1)

    def test_edit_post(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/바꾸고자하는 데이터와 바뀐 결과값이 같은지 확인
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')

        edit_data = {
            'writer' : user.id,
            'title' : 'test_edit_title',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns, #edit_like, #edit_post'
            }
                
        with self.assertNumQueries(39):
            edit_post(edit_data, user, post.id)
        edited_post = Post.objects.get(id = post.id)
        self.assertEqual(edit_data['title'], edited_post.title)
