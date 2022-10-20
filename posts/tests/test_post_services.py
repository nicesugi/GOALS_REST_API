from django.db import connection
from django.db.models import Count
from django.test import TestCase
from django.test.utils import CaptureQueriesContext 
from rest_framework import exceptions
from posts.models import Post, Like, PostTag, TagName
from posts.services.post_services import (
    read_posts,
    search_posts,
    filtering_posts,
    pagination_posts,
    create_post,
    edit_post,
    soft_delete_post,
    recover_post,
    hard_delete_post,
    like_post
)
from users.models import User

class TestService(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username = 'test_user',
            email = 'test_email@naver.com',
            password = 'test_pw'
            )
        user2 = User.objects.create(
            username = 'test_user2',
            email = 'test_email2@naver.com',
            password = 'test_pw2'
            )
        user3 = User.objects.create(
            username = 'test_user3',
            email = 'test_email3@naver.com',
            password = 'test_pw3'
            )
        
        tag_data1 = TagName.objects.create(name = 'sns')
        tag_data2 = TagName.objects.create(name = 'apple')
        tag_data3 = TagName.objects.create(name = 'choco')
        
        created_data = Post.objects.create(
            writer = user,
            title = 'test_title',
            content = 'test_content',
            is_active = True,
            views = 60,
            created_date = '2022-10-16 08:00:00.000000'
            )
        created_data2 = Post.objects.create(
            writer = user,
            title = 'test_title2',
            content = 'test_content2',
            is_active = True,
            views = 20,
            created_date = '2022-10-17 08:00:00.000000'
            )
        created_data3 = Post.objects.create(
            writer = user,
            title = 'test_title3',
            content = 'test_content3',
            is_active = True,
            views = 30,
            created_date = '2022-10-18 08:00:00.000000'
            )
        
        post_tag_data1 = PostTag.objects.create(tags = tag_data1, posts = created_data)
        post_tag_data2 = PostTag.objects.create(tags = tag_data1, posts = created_data2)
        post_tag_data3 = PostTag.objects.create(tags = tag_data2, posts = created_data2)
        post_tag_data4 = PostTag.objects.create(tags = tag_data1, posts = created_data3)
        post_tag_data5 = PostTag.objects.create(tags = tag_data2, posts = created_data3)
        post_tag_data6 = PostTag.objects.create(tags = tag_data3, posts = created_data3)
        
        like_data1 = Like.objects.create(post = created_data, user = user)
        like_data2 = Like.objects.create(post = created_data2, user = user2)
        like_data3 = Like.objects.create(post = created_data2, user = user3)
        like_data4 = Like.objects.create(post = created_data2, user = user)
        like_data5 = Like.objects.create(post = created_data2, user = user2)
        like_data6 = Like.objects.create(post = created_data3, user = user)
    
    def test_read_posts_case_created_date_n_reverse(self):
        """
        게시글을 정렬(작성일+내림차순)하여 조회하는 read_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/게시글 수 확인과 가장 첫번째 게시글을 확인하여 게시글 조회
        """ 
        test_posts = Post.objects.all().order_by('-created_date')
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        read_posts_count = posts.count()
        self.assertEqual(read_posts_count, 3)
        self.assertEqual(test_posts[0].id, posts[0].id)
        
    def test_read_posts_case_views_n_reverse(self):
        """
        게시글을 정렬(조회수+오름차순)하여 조회하는 read_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/게시글 수 확인과 가장 첫번째 게시글을 확인하여 게시글 조회
        """ 
        test_posts = Post.objects.all().order_by('views')
        reverse = 0
        order_by = 'views'
        posts = read_posts(order_by, reverse)
        read_posts_count = posts.count()
        self.assertEqual(read_posts_count, 3)
        self.assertEqual(test_posts[0].id, posts[0].id)

    def test_read_posts_case_likes_n_reverse(self):
        """
        게시글을 정렬(좋아요수+내림차순)하여 조회하는 read_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/게시글 수 확인과 가장 첫번째 게시글을 확인하여 게시글 조회
        """ 
        test_posts = Post.objects.all().annotate(like_count=Count('like')).order_by('-like_count')
        reverse = 1
        order_by = 'likes'
        posts = read_posts(order_by, reverse)
        read_posts_count = posts.count()
        self.assertEqual(read_posts_count, 3)
        self.assertEqual(test_posts[0].id, posts[0].id)

    def test_fail_read_posts_without_arg_order_by(self):
        """
        게시글 정렬 조회하는 read_posts service 검증
        case : 인자 값 중 order_by가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        reverse = 1
        with self.assertRaises(TypeError):
            read_posts(reverse)
            
    def test_fail_read_posts_without_arg_reverse(self):
        """
        게시글 정렬 조회하는 read_posts service 검증
        case : 인자 값 중 reverse가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        order_by = 'created_date'
        with self.assertRaises(TypeError):
            read_posts(order_by)
            
    def test_search_posts(self):
        """
        게시글 검색 조회하는 search_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/검색어를 포함한 게시글 수를 확인과 가장 첫번째 게시글을 확인하여 게시글 조회
        """
        test_posts = Post.objects.all().order_by('-created_date')
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        searched_posts_count = search_posts(posts, search).count()
        self.assertEqual(searched_posts_count, 3)
        self.assertEqual(test_posts[0].id, posts[0].id)
                        
    def test_fail_search_posts_without_arg_posts(self):
        """
        게시글 검색 조회하는 search_posts service 검증
        case : 인자 값 중 posts가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        search = 'test_title'
        with self.assertRaises(TypeError):
            search_posts(search)
            
    def test_fail_search_posts_without_arg_search(self):
        """
        게시글 검색 조회하는 search_posts service 검증
        case : 인자 값 중 search가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        reverse = 1
        order_by = 'likes'
        posts = read_posts(order_by, reverse)
        with self.assertRaises(TypeError):
            search_posts(posts)

    def test_filtering_posts(self):
        """
        게시글 해시태그를 필터링하는 filtering_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/해시태그를 포함한 게시글 수를 확인과 가장 첫번째 게시글을 확인하여 게시글 조회
        """
        test_posts = Post.objects.all().order_by('-created_date')
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        posts = search_posts(posts, search)
        tags = 'apple'
        filtering_posts_count = filtering_posts(posts, tags).count()
        self.assertEqual(filtering_posts_count, 2)
        self.assertEqual(test_posts[0].id, posts[0].id)
    
    def test_fail_filtering_posts_without_arg_posts(self):
        """
        게시글 검색 조회하는 filtering_posts service 검증
        case : 인자 값 중 posts가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        tags = 'apple'
        with self.assertRaises(TypeError):
            filtering_posts(tags)
            
    def test_fail_filtering_posts_without_arg_tags(self):
        """
        게시글 검색 조회하는 filtering_posts service 검증
        case : 인자 값 중 search가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        posts = search_posts(posts, search)
        tags = 'apple'
        posts = filtering_posts(posts, tags)
        with self.assertRaises(TypeError):
            filtering_posts(posts)

    def test_pagination_posts(self):
        """
        게시글 페이징하는 pagination_posts service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/결과값인 쿼리셋의 길이 확인과 가장 첫번째 게시글의 제목을 확인하여 게시글 조회
        """
        test_posts = Post.objects.all().order_by('-created_date')
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        posts = search_posts(posts, search)
        tags = 'apple'
        posts = filtering_posts(posts, tags)
        page_size = 10
        page = 1
        posts = pagination_posts(posts, page_size, page)
        self.assertEqual(len(posts), 2)
        self.assertEqual(test_posts[0].title, posts[0]['title'])

    def test_fail_pagination_posts_without_arg_posts(self):
        """
        게시글 페이징하는 pagination_posts service 검증
        case : 인자 값 중 posts가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        page_size = 10
        page = 1
        with self.assertRaises(TypeError):
            pagination_posts(page_size, page)
            
    def test_fail_pagination_posts_without_arg_page_size(self):
        """
        게시글 페이징하는 pagination_posts service 검증
        case : 인자 값 중 page_size가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        posts = search_posts(posts, search)
        tags = 'apple'
        posts = filtering_posts(posts, tags)
        page = 1
        with self.assertRaises(TypeError):
            pagination_posts(posts, page)
                        
    def test_fail_pagination_posts_without_arg_page(self):
        """
        게시글 페이징하는 pagination_posts service 검증
        case : 인자 값 중 page가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        reverse = 1
        order_by = 'created_date'
        posts = read_posts(order_by, reverse)
        search = 'test_title'
        posts = search_posts(posts, search)
        tags = 'apple'
        posts = filtering_posts(posts, tags)
        page_size = 10
        with self.assertRaises(TypeError):
            pagination_posts(posts, page_size)

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
            'tags' : '#sns,#like,#post'
            }
        
        with CaptureQueriesContext(connection) as ctx:
            create_post(create_data, user)
        ctx.captured_queries
        with self.assertNumQueries(14):
            create_post(create_data, user)
    
    def test_fail_create_post_without_arg_create_data(self):
        """
        게시물을 작성하는 create_post service 검증
        case : 인자 값 중 create_data가 들어오지 않을 경우 
        result : 실패/TypeError 발생        
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            create_post(user)
    
    def test_fail_create_post_without_arg_user(self):
        """
        게시물을 작성하는 create_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        create_data = {
            'title' : 'test_title',
            'content' : 'test_content',
            'tags' : '#sns,#like,#post'
            }
        with self.assertRaises(TypeError):
            create_post(create_data)
            
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
            'tags' : '#sns,#like,#post'
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
            'tags' : '#sns,#like,#post'
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

    def test_fail_create_post_over_max_length_of_title(self):
        """
        게시물을 작성하는 create_post service 검증
        case : title값이 길이 제한인 50자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : 'testtesttesttesttesttesttesttesttesttesttesttesttest',
            'content' : 'test_content',
            'tags' : '#sns,#like,#post'
            }
        with self.assertRaises(exceptions.ValidationError):
            create_post(create_data, user)
            
    def test_fail_create_post_over_max_length_of_content(self):
        """
        게시물을 작성하는 create_post service 검증
        case : content값이 길이 제한인 400자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        create_data = {
            'title' : 'test_title',
            'content' : 'testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest',
            'tags' : '#sns,#like,#post'
            }
        with self.assertRaises(exceptions.ValidationError):
            create_post(create_data, user)
            
    def test_edit_post(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/바꾸고자하는 데이터와 바뀐 결과값이 같은지 확인
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        edit_post(edit_data, user, post.id)
        edited_post = Post.objects.get(id = post.id)
        self.assertEqual(edit_data['title'], edited_post.title)

    def test_fail_edit_post_without_arg_edit_data(self):
        """
            게시물을 수정하는 edit_post service 검증
            case : 인자 값 중 edit_data가 들어오지 않을 경우 
            result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        with self.assertRaises(TypeError):
            edit_post(user, post.id)

    def test_fail_edit_post_without_arg_user(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(TypeError):
            edit_post(edit_data, post.id)
     
    def test_fail_edit_post_without_arg_post_id(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : 인자 값 중 post_id가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(TypeError):
            edit_post(edit_data, user)
            
    def test_fail_edit_post_without_title(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : title이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : '',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(exceptions.ValidationError):
            edit_post(edit_data, user, post.id)
            
    def test_fail_edit_post_without_content(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : content이 빈 값일 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : '',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(exceptions.ValidationError):
            edit_post(edit_data, user, post.id)

    def test_edit_post_without_tags(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : tags가 빈 값일 경우
        result : 정상/바꾸고자하는 데이터와 바뀐 결과값이 같은지 확인
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : 'test_edit_content',
            'tags' : ''
            }
        edit_post(edit_data, user, post.id)
        edited_post = Post.objects.get(id = post.id)
        self.assertEqual(edit_data['title'], edited_post.title)
        
    def test_fail_edit_post_over_max_length_of_title(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : title값이 길이 제한인 50자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : 'testtesttesttesttesttesttesttesttesttesttesttesttest',
            'content' : 'test_edit_content',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(exceptions.ValidationError):
            edit_post(edit_data, user, post.id)
            
    def test_fail_edit_post_over_max_length_of_content(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : content값이 길이 제한인 400자를 넘었을 경우
        result : 실패/ValidationError 발생
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(writer = user, title = 'test_title')
        edit_data = {
            'title' : 'test_edit_title',
            'content' : 'testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest\
                        testtesttesttesttesttesttesttesttesttesttesttesttest',
            'tags' : '#edit_sns,#edit_like,#edit_post'
            }
        with self.assertRaises(exceptions.ValidationError):
            edit_post(edit_data, user, post.id)
            
    def test_fail_edit_post_the_post_not_exist(self):
        """
        게시물을 수정하는 edit_post service 검증
        case : 없는 post를 수정할 경우 
        result : 실패/DoesNotExist 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(Post.DoesNotExist):
            recover_post(user, post_id=10000)
                
    def test_soft_delete_post(self):
        """
        게시물을 삭제(비활성화)하는 soft_delete_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/Post object를 삭제(비활성화)
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        soft_delete_post(user, post.id)
        soft_deleted_post = Post.objects.get(id = post.id)
        self.assertFalse(soft_deleted_post.is_active)
        
    def test_fail_soft_delete_post_without_arg_user(self):
        """
        게시물을 삭제(비활성화)하는 soft_delete_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        with self.assertRaises(TypeError):
            soft_delete_post(post.id)
            
    def test_fail_soft_delete_post_without_arg_post_id(self):
        """
        게시물을 삭제(비활성화)하는 soft_delete_post service 검증
        case : 인자 값 중 post_id가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            soft_delete_post(user)
    
    def test_fail_soft_delete_post_the_post_not_exist(self):
        """
        게시물을 삭제(비활성화)하는 soft_delete_post service 검증
        case : 없는 post를 삭제(비활성)할 경우 
        result : 실패/DoesNotExist 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(Post.DoesNotExist):
            recover_post(user, post_id=10000)
            
    def test_recover_post(self):
        """
        비활성화된 게시글 복구하는 recover_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/Post object를 활성화
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        recover_post(user, post.id)
        recovered_post = Post.objects.get(id = post.id)
        self.assertTrue(recovered_post.is_active)
        
    def test_fail_recover_post_without_arg_user(self):
        """
        비활성화된 게시글 복구하는 recover_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        with self.assertRaises(TypeError):
            recover_post(post.id)
            
    def test_fail_recover_post_without_arg_post_id(self):
        """
        비활성화된 게시글 복구하는 recover_post service 검증
        case : 인자 값 중 post_id가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            recover_post(user)
            
    def test_fail_recover_post_the_post_not_exist(self):
        """
        비활성화된 게시글 복구하는 recover_post service 검증
        case : 없는 post를 복구할 경우 
        result : 실패/DoesNotExist 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(Post.DoesNotExist):
            recover_post(user, post_id=10000)
    
    def test_hard_delete_post(self):
        """
        게시글 완전 삭제하는 hard_delete_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/Post object를 삭제
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        posts_count = Post.objects.all().count()
        hard_delete_post(user, post.id)
        after_posts_count = Post.objects.all().count()
        self.assertEqual(posts_count, after_posts_count+1)
        
    def test_fail_hard_delete_post_without_arg_user(self):
        """
        게시글 완전 삭제하는 hard_delete_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        with self.assertRaises(TypeError):
            recover_post(post.id)
            
    def test_fail_hard_delete_post_without_arg_post_id(self):
        """
        게시글 완전 삭제하는 hard_delete_post service 검증
        case : 인자 값 중 post_id가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            recover_post(user)
            
    def test_fail_hard_delete_post_the_post_not_exist(self):
        """
        게시글 완전 삭제하는 hard_delete_post service 검증
        case : 없는 post를 삭제하려고 할 경우 
        result : 실패/DoesNotExist 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(Post.DoesNotExist):
            recover_post(user, post_id=10000)
    
    def test_like_post_case_true(self):
        """
        게시글 좋아요 + 좋아요 수 카운트 like_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/결과값이 True가 나와 좋아요 등록하고 좋아요 수를 카운트 +1
        """
        user = User.objects.get(username = 'test_user')
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        like_post(user, post.id)
        self.assertEqual(like_post(user, post.id), True)
        created_like_obj_count = Post.objects.get(id=1).like_set.count()
        self.assertEqual(created_like_obj_count, 1)
    
    def test_like_post_case_false(self):
        """
        게시글 좋아요취소 + 좋아요 수 카운트 like_post service 검증
        case : 정상적으로 작동 했을 경우
        result : 정상/결과값이 False가 나와 좋아요 취소하고 좋아요 수 카운트 -1
        """
        user = User.objects.get(username = 'test_user2')
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        like_post(user, post.id)
        self.assertEqual(like_post(user, post.id), False)
        getted_like_obj_count = Post.objects.get(id=1).like_set.count()
        self.assertEqual(getted_like_obj_count-1, 0)
        
    def test_fail_like_post_without_arg_user(self):
        """
        게시글 좋아요/좋아요취소 + 좋아요 수 카운트 like_post service 검증
        case : 인자 값 중 user가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        post = Post.objects.get(title = 'test_title', content = 'test_content')
        with self.assertRaises(TypeError):
            like_post(post.id)
    
    def test_fail_like_post_without_arg_post_id(self):
        """
        게시글 좋아요/좋아요취소 + 좋아요 수 카운트 like_post service 검증
        case : 인자 값 중 post_id가 들어오지 않을 경우 
        result : 실패/TypeError 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(TypeError):
            like_post(user)
            
    def test_fail_like_post_the_post_not_exist(self):
        """
        게시글 좋아요/좋아요취소 + 좋아요 수 카운트 like_post service 검증
        case : 없는 post에 좋아요를 등록할 경우 
        result : 실패/DoesNotExist 발생
        """
        user = User.objects.get(username = 'test_user')
        with self.assertRaises(Post.DoesNotExist):
            like_post(user, post_id=10000)
            
