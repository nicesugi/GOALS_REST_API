# Social_Networking_Service

SNS 기능
<br>
<br>

## MVP Service
사용자는 본 서비스에 접속하여, 게시물을 업로드 하거나 다른 사람의 게시물을 확인하고, 좋아요를 누를 수 있습니다.

- User
    - 기본 회원가입, 로그인 시 사용 = Email
    - 로그아웃은 프로트 엔드에서 처리
    - JWT 기능 구현
- 게시글
    - 필드
        - 제목, 내용, 해시태그 등을 입력하여 생성
        - user는 JWT 토큰의 request.user를 통해서 가져온다.
        - 해시태그는 #로 시작되고 , 로 구분되는 텍스트가 입력됩니다.
        ex) { “hashtags”: “#맛집,#서울,#브런치 카페,#주말”, …}
    - 게시글 권한
        - 읽기 권한
            - 모든 사용자는 모든 게시물에 보기권한이 있습니다.
        - 수정 권한
            - 작성자만 수정할 수 있습니다.
        - 삭제 권한
            - 작성자만 삭제할 수 있습니다.
            - soft delete를 구현해서 게시글을 복구할 수 있는 기능 (복구 방법에 대해서 생각 해보아야 할 듯)
    - **게시글 상세보기 화면**
        - 좋아요 기능 구현
        - get_or_create()
        - create가 되면은 return 생성
        - get이되면 삭제
        - 상세보기를 할 때마다 조회수 1증가 기능
    - 게시글 목록
        - 제목, 작성자, 해시태그, 작성일, 좋아요 수, 조회수 가 포함
    - 추가 기능
        - Ordering (= Sorting, 정렬)
            - (default: 작성일,  / 작성일, 좋아요 수, 조회수 중 1개 만 선택가능)
            - 오름차순, 내림차순 두가지를 구현
        - Searching (= 검색)
            - 해당 키워드가 문자열 중 포함 된 데이터 검색
            - 1.  some-url?search=후기 >>  “후기" 가 제목에 포함된 게시글 목록.
            - params를 통한 매개변수를 받아와서, search 기능 구현
        - Filtering (= 필터링)
            - 지정한 키워드로 해당 키워드를 포함한 게시물을 필터링
                - 예시 1) some-url?hastags=서울 >> “서울" 해시태그를 가진 게시글 목록.
                - 예시 2) some-url?hastags=서울,맛집 >> “서울" 과 “맛집” 해시태그를 모두 가진 게시글 목록.
                - [ex. “서울” 검색 시 > #서울(검색됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
                - [ex. “서울,맛집” 검색 시 > #서울(검색안됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
        - Pagination (= 페이지 기능)
            - 사용자는 1 페이지 당 게시글 수를 조정할 수 있습니다. (default: 10건)

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

<img width="500" src="https://user-images.githubusercontent.com/104303285/192102890-ed55d395-6af7-40a8-b7b0-94ced715fcab.png" />
<br>
<br>

## API 명세서

 <img width="785" src="https://user-images.githubusercontent.com/104303285/192102941-8cad8c30-95b3-4365-937b-eb155bb6e51e.png" />

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

### 벼락치기의 규칙

- 컨벤션 지키기
- Commit 단위 지키기
- 말 이쁘게하기
- 문제를 마주하여 트러블을 겪었다면, 어떻게 해결을 했는지 공유를 해주기
- 각자의 작업을 미리 작성을 하여서 각자의 작업을 공유하기
<br>
<br>
