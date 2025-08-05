
import requests

# Function to read the Slack webhook URL from a file
def get_webhook_url():
    with open('slack_webhook_url.txt', 'r') as f:
        return f.read().strip()

# Function to send a message to Slack
def send_slack_message(message):
    webhook_url = get_webhook_url()
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("슬랙 메시지 전송 성공!")
    except requests.exceptions.RequestException as e:
        print(f"슬랙 메시지 전송 중 오류 발생: {e}")

if __name__ == '__main__':
    # Example usage:
    send_slack_message("안녕하세요! 급식 알림 봇 테스트 메시지입니다.")
