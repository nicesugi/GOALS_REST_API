# Social_Networking_Service
RESTful API를 작성하는 것과 테스트코드를 작성해 빈틈없는 코드, 컨벤션에 맞는 클린코드를 작성하기 위한 개인 프로젝트

<img src="https://img.shields.io/badge/Python-3.9.10-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/Django REST framework-092E20?style=flat-square&logo=Django REST framework&logoColor=white"/> 

### 목차
[1. 기능구현](#기능구현) <br>
[2. API 명세서](#api-명세서) <br>
[3. ERD](#erd) <br>
[4. 컨벤션](#컨벤션) <br>

---

## 기능구현

<details open>
<summary>
사용자
</summary>
<pre>
    - 회원가입, 로그인 시 사용 = Email
    - simple JWT로 로그인 기능 구현
</pre></details>

<details open>
<summary>게시글</summary>
<pre>

<details><summary> 목록 조회</summary>
    - 권한 : 모든 사용자
    - params를 통한 매개변수를 받아와서 기능 구현
    - 정렬
        - default : 작성일 + 내림차순
        - [작성일 / 좋아요 수 / 조회수] 중 1개 선택
        - 오름차순, 내림차순
    - 검색
        - 검색어가 제목이나 내용에 포함된 게시글
    - 필터링
        - 해당 키워드의 해시태그를 포함한 게시글
            - 예시 1) ?tags=서울 >> “서울" 해시태그를 포함한 게시글
            - 예시 2) ?tags=서울,맛집 >> “서울" 과 “맛집” 해시태그를 포함한 게시글
            - [ex. “서울” 검색 시 > #서울(검색됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)]
            - [ex. “서울,맛집” 검색 시 > #서울(검색안됨) / #서울맛집 (검색안됨)  / #서울,#맛집(검색됨)] 
    - 페이징
        - default : 1 페이지 당 10개의 게시글 수
        - params에 원하는 게시글 사이즈를 입력하여 사이즈 조정이 가능
</details>

<details><summary> 게시글 상세 조회</summary>
    - 권한 : 로그인이 된 사용자
    - 상세보기를 할 때마다 조회수 + 1
</details>

<details><summary> 작성</summary>
    - 권한 : 로그인이 된 작성자
    - 입력값 : 제목, 내용, 해시태그
    - 사용자는 JWT 토큰의 request.user를 통해서 가져옴
    - 해시태그는 '#'로 시작되고 ','로 구분되는 텍스트가 입력됨
        - 예시 { “tags”: “#맛집,#서울,#브런치 카페,#주말” }
</details>

<details><summary> 수정</summary>
    - 권한 : 로그인이 된 작성자
</details>

<details><summary> 삭제 </summary>
    - 권한 : 로그인이 된 작성자
    - soft delete 삭제시 비활성화
    - hard delete 삭제시 영구삭제
</details>

<details><summary> 복구</summary>
    - 권한 : 로그인이 된 작성자
</details>

<details><summary> 좋아요</summary>
    - 권한 : 로그인이 된 사용자
    - get_or_create()
    - create가 되면은 return 생성
    - get이 되면 삭제
</details>
</pre>
</details>

---

## API 명세서
<img width="700" alt="스크린샷 2022-10-21 오후 12 54 15" src="https://user-images.githubusercontent.com/104303285/197108032-dba1e5fc-2e3f-4201-9d86-d741bf0c5720.png">

---

## ERD
<img width="600" src="https://user-images.githubusercontent.com/104303285/197109255-f988ff08-d53c-4b08-aeb4-a04c265cd89b.png">


---

## 컨벤션

### Commit Message

- feat/ 기능 추가/수정/삭제
- enhan/ 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ 코드 리팩토링
- fix/ 버그 수정
- test/ 테스트 코드/기능 추가
- edit/ 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

### Naming

- Class : Pascal
- Variable : Snake
- Function : Snake
- Constant : Pascal + Snake

### 주석

- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.
