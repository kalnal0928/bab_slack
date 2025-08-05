
import requests
import json

def get_kakao_rest_api_key():
    with open('kakao_rest_api_key.txt', 'r') as f:
        return f.read().strip()

def get_kakao_access_token():
    with open('kakao_access_token.txt', 'r') as f:
        return f.read().strip()


REST_API_KEY = get_kakao_rest_api_key()
ACCESS_TOKEN = get_kakao_access_token()

def send_message_to_me(text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
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

    response = requests.post(url, headers=headers, data=data)

    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

if __name__ == '__main__':
    # 여기에 보내고 싶은 메시지를 입력하세요.
    send_message_to_me("안녕하세요! 카카오톡 API 테스트입니다.")
