# 경덕중학교 급식 알림봇

경상북도 안동시 경덕중학교의 급식 정보를 NEIS API로 조회하여 텔레그램으로 전송하는 봇입니다.

## 🚀 기능

- NEIS API를 통한 급식 정보 조회
- 텔레그램 봇을 통한 급식 정보 전송
- GitHub Actions를 통한 자동 실행

## 📋 필요 환경

- Python 3.8+
- NEIS API 키
- 텔레그램 봇 토큰
- 텔레그램 채팅 ID

## 🛠️ 설치 및 설정

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

#### 로컬 테스트용 (.env 파일 생성)

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
NEIS_API_KEY=your_neis_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

#### GitHub Actions용

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 시크릿을 설정하세요:

- `NEIS_API_KEY`: NEIS API 키
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 텔레그램 채팅 ID

## 🚀 실행 방법

### 로컬 실행

```bash
python main.py
```

### GitHub Actions 실행

1. GitHub 저장소의 Actions 탭으로 이동
2. "Send Daily Lunch Menu" 워크플로우 선택
3. "Run workflow" 버튼 클릭

## 📊 API 정보

- **교육청 코드**: R10 (경상북도교육청)
- **학교 코드**: R100000897 (안동중앙고등학교)
- **API 엔드포인트**: https://open.neis.go.kr/hub/mealServiceDietInfo

## 🔧 문제 해결

### 급식 정보가 전송되지 않는 경우

1. 환경변수가 올바르게 설정되었는지 확인
2. NEIS API 키가 유효한지 확인
3. 텔레그램 봇 토큰과 채팅 ID가 올바른지 확인
4. 해당 날짜에 급식 정보가 있는지 확인

### 로그 확인

프로그램 실행 시 상세한 로그가 출력됩니다. 다음 정보를 확인하세요:

- API 요청/응답 상태
- 데이터 파싱 과정
- 텔레그램 전송 상태

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 