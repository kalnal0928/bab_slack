import requests
import os
import json
from datetime import datetime

# --- 설정 파일 로드 ---
def load_config():
    """환경 변수에서 API 키와 Telegram Bot Token, Chat ID를 로드합니다."""
    neis_api_key = os.getenv("NEIS_API_KEY")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    print(f"환경 변수 확인:")
    print(f"NEIS_API_KEY: {'설정됨' if neis_api_key else '설정되지 않음'}")
    print(f"TELEGRAM_BOT_TOKEN: {'설정됨' if telegram_bot_token else '설정되지 않음'}")
    print(f"TELEGRAM_CHAT_ID: {'설정됨' if telegram_chat_id else '설정되지 않음'}")

    if not neis_api_key:
        print("에러: NEIS_API_KEY 환경 변수를 찾을 수 없습니다.")
    if not telegram_bot_token:
        print("에러: TELEGRAM_BOT_TOKEN 환경 변수를 찾을 수 없습니다.")
    if not telegram_chat_id:
        print("에러: TELEGRAM_CHAT_ID 환경 변수를 찾을 수 없습니다.")

    return neis_api_key, telegram_bot_token, telegram_chat_id

# NEIS API 기본 정보
API_URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"
ATPT_OFCDC_SC_CODE = "R10"  # 경상북도교육청
SD_SCHUL_CODE = "8791090"      # 경덕중학교 (급식 정보 확인된 코드)

def get_api_data(api_key, meal_date):
    """NEIS API를 호출하여 급식 정보를 가져옵니다."""
    params = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDC_SC_CODE': ATPT_OFCDC_SC_CODE,
        'SD_SCHUL_CODE': SD_SCHUL_CODE,
        'MLSV_YMD': meal_date
    }
    try:
        print(f"API 요청 파라미터: {params}")
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        print(f"Lunch API response: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return None

def format_meal_data(data):
    """API 응답 데이터를 Telegram 메시지 형식으로 가공합니다."""
    try:
        meal_info = data['mealServiceDietInfo'][1]['row']
        
        # 중식 정보만 필터링
        lunch_menu = next((item for item in meal_info if item['MMEAL_SC_NM'] == '중식'), None)

        if not lunch_menu:
            return "오늘은 중식 정보가 없습니다."

        # 메뉴, 칼로리, 영양 정보 추출 및 가공
        dish = lunch_menu['DDISH_NM'].replace('<br/>', '\n')
        cal_info = lunch_menu.get('CAL_INFO', '정보 없음')
        ntr_info = lunch_menu.get('NTR_INFO', '정보 없음').replace('<br/>', '\n')

        # Telegram에서 안전하게 표시할 수 있는 메시지 형식
        message = (
            f"🏫 경덕중학교 오늘의 중식 🏫\n\n"
            f"🍽️ 메뉴:\n{dish}\n\n"
            f"🍚 칼로리: {cal_info}\n\n"
            f"🥗 영양정보:\n{ntr_info}"
        )
        return message

    except (KeyError, TypeError, IndexError):
        # 데이터가 없는 경우 (INFO-200)
        if data.get('RESULT', {}).get('CODE') == 'INFO-200':
            return "오늘은 급식 정보가 없습니다."
        return "급식 정보를 파싱하는 중 오류가 발생했습니다."

def send_to_telegram(bot_token, chat_id, message):
    """Telegram으로 메시지를 전송합니다."""
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Telegram API에서 안전하게 처리할 수 있는 메시지로 변환
    safe_message = message.replace('*', '').replace('_', '').replace('[', '(').replace(']', ')')
    
    payload = {
        'chat_id': chat_id,
        'text': safe_message,
        'parse_mode': 'HTML'  # HTML 파싱 모드 사용
    }
    
    # HTML 태그로 메시지 재구성
    html_message = safe_message.replace('\n', '<br>')
    payload['text'] = html_message
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        print(f"Telegram API URL: {telegram_api_url}")
        print(f"Chat ID: {chat_id}")
        print(f"전송할 메시지: {html_message}")
        
        response = requests.post(telegram_api_url, json=payload, headers=headers, timeout=15)
        
        print(f"Telegram API 응답 상태 코드: {response.status_code}")
        print(f"Telegram API 응답 내용: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Telegram 메시지 전송 성공")
                return True
            else:
                print(f"❌ Telegram API 오류: {result.get('description', '알 수 없는 오류')}")
                return False
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Telegram 전송 중 네트워크 에러 발생: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

def test_telegram_connection(bot_token, chat_id):
    """Telegram 연결을 테스트합니다."""
    print("🔍 Telegram 연결 테스트 시작...")
    
    test_message = "🧪 급식 알림봇 연결 테스트 메시지입니다."
    success = send_to_telegram(bot_token, chat_id, test_message)
    
    if success:
        print("✅ Telegram 연결 테스트 성공!")
    else:
        print("❌ Telegram 연결 테스트 실패!")
    
    return success

if __name__ == "__main__":
    print("🚀 급식 알림봇 시작...")
    
    neis_api_key, telegram_bot_token, telegram_chat_id = load_config()

    if not neis_api_key or not telegram_bot_token or not telegram_chat_id:
        print("❌ 필수 환경 변수가 설정되지 않았습니다. 스크립트를 종료합니다.")
        exit(1)
    
    # Telegram 연결 테스트
    if not test_telegram_connection(telegram_bot_token, telegram_chat_id):
        print("❌ Telegram 연결에 실패했습니다. 설정을 확인해주세요.")
        exit(1)
    
    today_date = datetime.now().strftime('%Y%m%d')
    print(f"📅 오늘 날짜: {today_date}")
    
    api_response = get_api_data(neis_api_key, today_date)

    if api_response:
        print("--- NEIS API Raw Response ---")
        print(json.dumps(api_response, indent=2, ensure_ascii=False))
        print("-----------------------------")
        
        telegram_message = format_meal_data(api_response)
        print(f"📝 가공된 메시지:\n{telegram_message}")
        
        success = send_to_telegram(telegram_bot_token, telegram_chat_id, telegram_message)
        if success:
            print("🎉 급식 정보 전송 완료!")
        else:
            print("💥 급식 정보 전송 실패!")
    else:
        print("❌ NEIS API에서 데이터를 가져올 수 없습니다.")
        # API 실패 시에도 테스트 메시지 전송
        error_message = f"⚠️ {today_date} 급식 정보 조회에 실패했습니다."
        send_to_telegram(telegram_bot_token, telegram_chat_id, error_message)
