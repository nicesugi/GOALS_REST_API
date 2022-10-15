# Social_Networking_Service

[1. 기능명세서](#기능명세서) <br>
[2. 기술스택](#기술-스택) <br>
[3. ERD](#erd) <br>
[4. API](#api-명세서) <br>
[5. 컨벤션](#컨벤션) <br>

## 기능명세서
사용자는 본 서비스에 접속하여, 게시물을 업로드 하거나 다른 사람의 게시물을 확인하고, 좋아요를 누를 수 있습니다.

- 사용자
    - 기본 회원가입, 로그인 시 사용 = Email
    - 로그아웃은 프론트엔드에서 처리
    - simple JWT로 로그인 기능 구현
- 게시글
    - 게시글 접근 권한
        - 읽기 권한
            - 모든 사용자
        - 수정 권한
            - 작성자만
        - 삭제 권한
            - 작성자만
            - soft delete를 구현해서 삭제시 비활성화
        - 복구 권한
            - 작성자만
    - 게시글 생성
        - 입력값 : 제목, 내용, 해시태그
        - 사용자는 JWT 토큰의 request.user를 통해서 가져옴
        - 해시태그는 '#'로 시작되고 ','로 구분되는 텍스트가 입력됨
            - 예시 { “tags”: “#맛집,#서울,#브런치 카페,#주말” }
    - 게시글 상세보기
        - 좋아요
            - get_or_create()
            - create가 되면은 return 생성
            - get이 되면 삭제
        - 상세보기를 할 때마다 조회수 + 1
    - 게시글 목록
        - 제목, 작성자, 해시태그, 작성일, 좋아요 수, 조회수
        - 정렬
            - default : 작성일 
            - [작성일 / 좋아요 수 / 조회수] 중 1개 선택
            - 오름차순, 내림차순
        - 검색
            - 해당 키워드가 제목이나 내용에 포함된 게시글 목록
            - params를 통한 매개변수를 받아와서, search 기능 구현. ?search=cookie
        - 필터링
            - 해당 키워드의 해시태그를 포함한 게시글 목록
                - 예시 1) some-url?hastags=서울 >> “서울" 해시태그를 가진 게시글 목록
                - 예시 2) some-url?hastags=서울,맛집 >> “서울" 과 “맛집” 해시태그를 모두 가진 게시글 목록
                - [ex. “서울” 검색 시 > #서울(검색됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
                - [ex. “서울,맛집” 검색 시 > #서울(검색안됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
        - 페이징
            - 사용자는 1 페이지 당 게시글 수를 조정할 수 있음 (default : 10건)

<br>
<br>

## 기술 스택

<div style='flex'>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white" >
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/Django REST framework-092E20?style=for-the-badge&logo=Django REST framework&logoColor=white">
</div>
<br>
<br>

## ERD

<img width="300" src="https://user-images.githubusercontent.com/104303285/193576893-a87828aa-6f04-4ea8-92e6-8c9b8dd13514.png" />
<br>
<br>

## API 명세서

 <img width="785" src="https://user-images.githubusercontent.com/104303285/193740266-209d4b7a-544a-43d3-a82c-be662118d043.png" />

## 컨벤션

### Commit Message

- feat/ : 기능 추가/수정/삭제
- enhan/ : 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ : 코드 리팩토링, 버그 수정
- test/ : 테스트 코드/기능 추가
- edit/ : 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

### Naming

- Class : Pascal
- Variable : Snake
- Function : Snake
- Constant : Pascal + Snake

### 주석

- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.
