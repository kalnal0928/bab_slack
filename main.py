import requests
import os
import json
from datetime import datetime

# --- 설정 파일 로드 ---
def load_config():
    """config.json 파일에서 API 키와 Slack Webhook URL을 로드합니다."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get("NEIS_API_KEY"), config.get("SLACK_WEBHOOK_URL")
    except FileNotFoundError:
        print("에러: config.json 파일을 찾을 수 없습니다. API 키와 Slack Webhook URL을 입력하여 파일을 생성해주세요.")
        return None, None
    except json.JSONDecodeError:
        print("에러: config.json 파일의 형식이 올바르지 않습니다.")
        return None, None

# NEIS API 기본 정보
API_URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"
ATPT_OFCDC_SC_CODE = "R10"  # 경상북도교육청
SD_SCHUL_CODE = "7670053"      # 경덕중학교

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
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return None

def format_meal_data(data):
    """API 응답 데이터를 Slack 메시지 형식으로 가공합니다."""
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

        message = (
            f"🏫 *경덕중학교 오늘의 중식* 🏫\n\n"
            f"*{dish}*\n\n"
            f"🍚 *칼로리*: {cal_info}\n\n"
            f"🥗 *영양정보*:\n{ntr_info}"
        )
        return message

    except (KeyError, TypeError, IndexError):
        # 데이터가 없는 경우 (INFO-200)
        if data.get('RESULT', {}).get('CODE') == 'INFO-200':
            return "오늘은 급식 정보가 없습니다."
        return "급식 정보를 파싱하는 중 오류가 발생했습니다."

def send_to_slack(webhook_url, message):
    """Slack으로 메시지를 전송합니다."""
    payload = {'text': message}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
        response.raise_for_status()
        print("Slack 메시지 전송 성공")
    except requests.exceptions.RequestException as e:
        print(f"Slack 전송 중 에러 발생: {e}")

if __name__ == "__main__":
    neis_api_key, slack_webhook_url = load_config()

    if not neis_api_key or not slack_webhook_url:
        print("스크립트를 종료합니다. config.json 파일에 키와 URL을 올바르게 설정했는지 확인해주세요.")
    else:
        today_date = datetime.now().strftime('%Y%m%d')
        api_response = get_api_data(neis_api_key, today_date)

        if api_response:
            slack_message = format_meal_data(api_response)
            send_to_slack(slack_webhook_url, slack_message)