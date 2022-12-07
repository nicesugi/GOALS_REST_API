from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Like, Post
from posts.services.post_services import (create_post, edit_post,
                                          filtering_posts, hard_delete_post,
                                          like_post, pagination_posts,
                                          read_detail_post, read_posts,
                                          recover_post, search_posts,
                                          soft_delete_post)


class PostView(APIView):
    """
    get : 게시글 목록 조회
    post : 게시글 작성
    put : 게시글 수정
    delete : 게시글 비활성화(soft_delete)
    """

    def get(self, request):
        order_by = self.request.query_params.get("order_by", "created_date")
        reverse = int(self.request.query_params.get("reverse", 1))
        search = self.request.query_params.get("search", "")
        tags = self.request.query_params.get("tags", "")
        page_size = int(self.request.query_params.get("page_size", 10))
        page = int(self.request.query_params.get("page", 1))

        try:
            posts = read_posts(order_by, reverse)
            posts = search_posts(posts, search)
            posts = filtering_posts(posts, tags)
            posts = pagination_posts(posts, page_size, page)
            return Response(posts, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {"detail": "로그인상태나 작성내용을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            create_post(request.data, request.user)
            return Response({"detail": "게시글이 작성되었습니다"}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError:
            return Response(
                {"detail": "제목이나 내용을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {"detail": "로그인상태나 작성내용을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            edit_post(request.data, request.user, post_id)
            return Response({"detail": "게시글이 수정되었습니다"}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError:
            return Response(
                {"detail": "제목이나 내용을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError:
            return Response(
                {"detail": "로그인상태나 수정내용을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            soft_delete_post(request.user, post_id)
            return Response({"detail": "게시글이 비활성화가 되었습니다"}, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )


class ExistencePostView(APIView):
    """
    post : 비활성화된 게시글 복구
    delete : 게시글 완전 삭제(hard_delete)
    """

    def post(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            recover_post(request.user, post_id)
            return Response({"detail": "게시글이 복구되었습니다"}, status=status.HTTP_201_CREATED)
        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            hard_delete_post(request.user, post_id)
            return Response({"detail": "게시글이 삭제되었습니다"}, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )


class PostDetailView(APIView):
    """
    get : 게시글 상세 조회
    """

    def get(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            post = read_detail_post(post_id)
            return Response(post, status=status.HTTP_200_OK)
        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )


class LikeView(APIView):
    """
    post : 게시글 좋아요/좋아요취소 + 좋아요 수 카운트
    """

    def post(self, request, post_id):
        if request.user.is_anonymous:
            return Response(
                {"detail": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            if like_post(request.user, post_id):
                like_count = Like.objects.filter(post=post_id).count()
                return Response(
                    {"detail": "좋아요 했습니다", "like_count": like_count},
                    status=status.HTTP_200_OK,
                )
            like_count = Like.objects.filter(post=post_id).count()
            return Response(
                {"detail": "좋아요를 취소했습니다", "like_count": like_count},
                status=status.HTTP_200_OK,
            )
        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )
