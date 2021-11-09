# 원티드x위코드 백엔드 프리온보딩 과제3 :: 원티드랩(Wantedlab)

# 배포 주소 :

### 1. [TEAM] WithCODE

#### Members

| 이름   | github                         |
| ------ | ------------------------------ |
| 김민호 | https://github.com/maxkmh712   |
| 김주형 | https://github.com/BnDC        |
| 박치훈 | https://github.com/chihunmanse |
| 박현우 | https://github.com/Pagnim      |
| 이기용 | https://github.com/leeky940926 |
| 이정아 | https://github.com/wjddk97     |

-----

### 2. 과제

#### [필수 포함 사항]

- READ.ME 작성
  - 프로젝트 빌드, 자세한 실행 방법 명시
  - 구현 방법과 이유에 대한 간략한 설명
  - 완료된 시스템이 배포된 서버의 주소
  - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
  - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

#### [과제  안내]

- 원티드 선호 기술스택: Python flask 또는 fastapi

#### 📝 다음과 같은 내용을 포함하는 테이블을 설계하고 다음과 같은 기능을 제공하는 REST API 서버를 개발해주세요.

#### 1. 데이터

- 회사 정보
  - 회사 이름 (다국어 지원 가능)
- 회사 정보 예제
  - 회사 이름 (원티드랩 / Wantedlab)
- 데이터 셋은 원티드에서 제공
  [wanted_temp_data.csv](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/81f13ae2-fabc-4fad-a754-9b2d684f41a8/wanted_temp_data.csv)
- 데이터셋 예제
  - 원티드랩 회사는 한국어, 영어 회사명을 가지고 있습니다. (모든 회사가 모든 언어의 회사명을 가지고 있지는 않습니다.)

#### 2. REST API 기능

- 회사명 자동완성
  - 회사명의 일부만 들어가도 검색이 되어야 합니다.
- 회사 이름으로 회사 검색
- 새로운 회사 추가

#### 3. 개발 조건

- 제공되는 test case를 통과할 수 있도록 개발해야 합니다.
  [test_app.py](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0d2517b3-b80b-4a1b-82c4-9bc6f2a0d5ae/test_app.py)
- ORM 사용해야 합니다.
- 결과는 JSON 형식이어야 합니다.
- database는 RDB를 사용해야 합니다.
- database table 갯수는 제한없습니다.
- 필요한 조건이 있다면 추가하셔도 좋습니다.
- Docker로 개발하면 가산점이 있습니다.

-----

### 3. Skill & Tools

- **Skill :** <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white"/>
- **Depoly :** <img src="https://img.shields.io/badge/AWS EC2-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"/> <br>
- **ETC :**  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>

-----

### 

-----

### 4. 모델링

![wanted](https://user-images.githubusercontent.com/79758688/140933586-1de78372-10d8-47b4-b7f7-f7b3f3ab8baf.png)

-----

### 5. Postman API 명세서

(포스트맨 주소)

-----

### 6. 구현 사항 상세 설명

### GET /search?query

QueryParameter를 통해 요청에서 검색어를 입력받아 해당 검색어가 포함된 회사명을 조회합니다. 검색어가 회사명과 완전히 일치하지 않고 일부만 들어가도 검색이 가능합니다.

headers에 x-wanted-language로 전달받은 언어타입에 따라 검색된 회사명이 해당 언어타입으로 변환되어 출력됩니다. 

만약 query 값이 들어오지 않으면 전체 회사명이 조회됩니다. 

헤더에서 전달받은 언어타입이 존재하지 않을시 404 code가 return 됩니다.

### GET /companies/{str:company_name}

path 변수를 통해 회사명을 입력받아 해당 회사를 조회합니다. headers에 x-wanted-language로 전달받은 언어타입에 따라 검색된 회사명과 회사의 태그들이 해당 언어타입으로 변환되어 출력됩니다.

만약 path 변수에 입력받은 회사명이 존재하지 않을시 404 code가 return 됩니다.

헤더에서 전달받은 언어타입이 존재하지 않을시 404 code가 return 됩니다.

### POST /companies

body에서 입력받은 회사명을 통해 새로운 회사가 생성됩니다. 회사명에 새로운 언어타입이 있다면 해당 언어타입이 새로 생성됩니다.

body에서 입력받은 태그들이 생성된 회사와 연결됩니다. 새로운 언어타입이 있다면 생성된 언어타입으로 태그명이 새로 생성됩니다.

headers에 x-wanted-language로 전달받은 언어타입에 따라 생성된 회사명과 태그가 출력됩니다.

요청에 body가 존재하지 않을시 400 code가 return 됩니다.

-----

### 7. Unittest 결과

(사진)

-----

### 8. Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 원티드랩(wantedlab)에서 출제한 과제를 기반으로 만들었습니다.
