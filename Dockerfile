FROM python:3.9

# 설치해야 할 종속성들
RUN apt-get update && apt-get install -y wget libgl1-mesa-glx libnss3-tools ffmpeg

# mkcert 설치
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
RUN mv mkcert-v1.4.3-linux-amd64 /usr/bin/mkcert
RUN chmod +x /usr/bin/mkcert

# 애플리케이션 파일 복사
COPY . /app
WORKDIR /app

# 인증서 설치
RUN mkcert -install
RUN mkcert localhost 127.0.0.1

# 인증서 이름 변경
RUN mv localhost+1-key.pem key.pem
RUN mv localhost+1.pem cert.pem

# 종속성 설치
RUN pip install -r requirements.txt
RUN pip install ffmpeg-python

# 포트 노출
EXPOSE 40000

# 애플리케이션 실행
CMD ["hypercorn", "run:app", "-c", "hypercorn_config.py", "--reload"]