
import requests
import json
import os

def get_kakao_access_token():
    try:
        with open('kakao_access_token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("오류: 'kakao_access_token.txt' 파일을 찾을 수 없습니다.")
        return None

def send_message_to_me(text):
    ACCESS_TOKEN = get_kakao_access_token()
    if not ACCESS_TOKEN:
        return

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    template = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
    }

    data = {
        "template_object": json.dumps(template)
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # 오류 발생 시 예외를 발생시킴

        # 성공적으로 보냈는지 확인
        if response.json().get('result_code') == 0:
            print('카카오톡 메시지를 성공적으로 보냈습니다.')
        else:
            print(f'카카오톡 메시지 보내기 실패: {response.json()}')

    except requests.exceptions.RequestException as e:
        print(f"카카오톡 API 요청 중 오류가 발생했습니다: {e}")
        # 응답 내용이 있다면 출력
        if e.response:
            print(f"응답 상태 코드: {e.response.status_code}")
            print(f"응답 내용: {e.response.text}")

if __name__ == '__main__':
    send_message_to_me("안녕하세요! 카카오톡 API 코드 수정 테스트입니다.")
