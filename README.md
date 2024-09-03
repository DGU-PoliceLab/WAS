![thumbnail](/resource/thumb.png)

# 소개

이 저장소는 동국대학교 대학원에서 개발한 치안현장 맞춤형 연구개발사업(폴리스랩 2.0)을 위해 개발된 인공지능 모델 통합 시스템의 대시보드입니다.

### 폴리스랩 2.0이란?

-   국민, 경찰, 연구자 등이 협업하여 치안 현장에서 발생하는 문제를 발굴하고 첨단과학기술과 ICT융합을 통해 문제해결 및 실증
-   연구자와 사용자(경찰)간 상호작용을 촉진하기 위해 실제 환경에서 기술개발이 가능한 실증 실험실(폴리스랩\*) 구축

*   > 치안을 뜻하는 폴리스(Police)와 리빙랩(Living-Lab)의 합성어

-   치안 현장의 문제해결을 위해 실제 적용 및 검증할 수 있도록 현장에서 실증연구를 강화하여 완결성 제고

![PoliceLab 2.0](/resource/introduction.png)

## 주요기능

TODO

# 설치

### 1. 라이브러리 설치

```
pip install -r requirements.txt
```

대시보드 실행을 위해 아래 라이브러리가 필요합니다.

-   fastapi
-   uvicorn
-   hypercorn
-   redis
-   pymysql
-   opencv-python

### 2. .env 생성

.env

```
# redis
REDIS_HOST='localhost'
REDIS_PORT=16379
REDIS_DATABASE=0

# mysql
MYSQL_HOST='localhost'
MYSQL_PORT=13306
MYSQL_USER='root'
MYSQL_PASSWORD='1q2w3e4r!'
MYSQL_DATABASE="pls"
MYSQL_CHARSET="utf8"
```

# 실행

### 모니터링

서버의 상태 모니터링 및 데이터베이스 기록 기능을 실행합니다.

```

python monit.py

```

-   Docker Desktop이 실행상태가 아니라면 자동으로 실행됩니다.(Windows만 지원)

### 대시보드

서버의 상태 시각화 기능을 실행합니다.

```

uvicorn main:app --reload

```

다음 링크로 API Endpoint에 접속합니다.

[API Endpoint](http://localhost:40000)
또는 https://localhost:40000

다음 링크로 API Docs에 접속합니다.

[API Docs](http://localhost:40000/docs)
또는 https://localhost:40000/docs

[API Docs(redoc)](http://localhost:40000/redoc)
또는 https://localhost:40000/redoc
