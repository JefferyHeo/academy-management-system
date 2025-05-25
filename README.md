# 📘 Academy Management System (AMS)

> 학생 출결, 과제, 시험 점수 및 마일리지를 효율적으로 관리할 수 있는 Django 기반 학원 관리 시스템입니다.

---

## 🚀 주요 기능

### 👩‍🏫 선생님 기능
- 학생 등록 / 수정 / 삭제
- 반(클래스) 생성 및 삭제
- 출결 기록 추가 및 수정
- 과제 제출 여부 기록
- 시험 점수 등록
- 마일리지 규칙 정의 및 자동 계산
- 반 삭제 시 학생은 자동으로 "미정" 반으로 이동

### 🙋‍♂️ 학생 기능
- 4자리 비밀번호로 간편 로그인
- 본인의 출결, 과제, 시험, 마일리지 확인

---

## 🛠️ 기술 스택

- Python 3.8+
- Django 4.x
- Gunicorn + Nginx (운영 서버)
- SQLite3 (개발용)
- Bootstrap 5 (프론트엔드)

---

## ⚙️ 설치 방법 (로컬 환경 기준)

```bash
# 1. 프로젝트 클론
git clone https://github.com/yourusername/academy-management-system.git
cd academy-management-system

# 2. 가상환경 설정
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 마이그레이션 및 슈퍼유저 생성
python manage.py migrate
python manage.py createsuperuser

# 5. 개발 서버 실행
python manage.py runserver
```

---

## 🌐 배포 서버 설정 요약 (EC2 기준)

- Gunicorn systemd 서비스로 실행 (`/etc/systemd/system/gunicorn.service`)
- Nginx 리버스 프록시 설정
- `STATIC_ROOT` 설정 후 `python manage.py collectstatic` 필수
- `gunicorn.sock` 사용하여 Nginx 연동

---

## 🔐 보안 관련 주의사항

- `SECRET_KEY`, DB 비밀번호는 `.env`로 분리하고 `.gitignore` 처리
- `DEBUG=False` 설정 시 템플릿 캐시 주의 (gunicorn 재시작 필요)
- `.env`, `db.sqlite3`, `gunicorn.sock`, `venv/` 등은 반드시 `.gitignore`에 추가

---

## 🙌 팀원

- 허승범

---

## 📌 기타

- 반 삭제 시 학생들은 자동으로 `"미정"` 반으로 이동됩니다.
- 마일리지 규칙 삭제는 상세 페이지에서 가능하며, 수정 페이지에서는 제공되지 않습니다.
