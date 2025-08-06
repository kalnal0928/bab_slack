import json
import os
import requests
from datetime import datetime, timedelta

# get_meal_data.py의 내용을 여기에 통합
def get_meal_data(api_key):
    today = datetime.now()
    # 주말에는 다음 주 월요일 식단을 가져오도록 수정
    if today.weekday() >= 5: # 토요일(5) 또는 일요일(6)
        today += timedelta(days=(7 - today.weekday())) # 다음 주 월요일로 이동

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={api_key}&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010578&MLSV_YMD={today.strftime('%Y%m%d')}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        data = response.json()

        if "mealServiceDietInfo" in data:
            meals = data["mealServiceDietInfo"][1]["row"]
            lunch_menu = "점심 메뉴가 없습니다."
            for meal in meals:
                if meal["MMEAL_SC_NM"] == "중식":
                    lunch_menu = meal["DDISH_NM"].replace("<br/>", "\n")
                    break
            return lunch_menu
        else:
            return "식단 정보를 가져올 수 없습니다."
    except requests.exceptions.RequestException as e:
        return f"식단 정보를 가져오는 중 오류 발생: {e}"
    except json.JSONDecodeError:
        return "API 응답을 디코딩하는 중 오류 발생."

# send_to_slack.py의 내용을 여기에 통합
def send_slack_message(webhook_url, message):
    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return {"statusCode": 200, "body": "Slack 메시지 전송 성공"}
    except requests.exceptions.RequestException as e:
        return {"statusCode": 500, "body": f"Slack 메시지 전송 실패: {e}"}

# Netlify Function의 핸들러
def handler(event, context):
    api_key = os.environ.get("NEIS_API_KEY")
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    if not api_key or not slack_webhook_url:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "환경 변수(NEIS_API_KEY 또는 SLACK_WEBHOOK_URL)가 설정되지 않았습니다."})
        }

    lunch_menu = get_meal_data(api_key)
    
    # Slack 메시지 전송
    slack_result = send_slack_message(slack_webhook_url, f"오늘의 점심 메뉴:\n{lunch_menu}")

    # Kakao 메시지 전송 (main.py에 Kakao 로직이 있다면 여기에 추가)
    # 현재 코드에는 Kakao 로직이 없으므로, 필요하다면 추가해야 합니다.
    # kakao_access_token = os.environ.get("KAKAO_ACCESS_TOKEN")
    # if kakao_access_token:
    #     # send_to_kakao.py의 로직을 여기에 통합하여 Kakao 메시지 전송
    #     pass

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "워크플로우 실행 완료", "slack_status": slack_result["body"]})
    }
