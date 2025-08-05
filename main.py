from get_meal_data import get_meal_data, format_meal_data
from send_to_slack import send_slack_message
import datetime

def main():
    # Get today's date
    today = datetime.date.today().strftime("%Y년 %m월 %d일")

    # Get meal data
    meal_data = get_meal_data()

    # Check if meal_data is available
    if meal_data:
        # Format the meal data into a message
        message = f"{today} 경덕중학교 급식 정보\n\n{format_meal_data(meal_data)}"
    else:
        message = f"{today} 경덕중학교 급식 정보가 없습니다."

    # Send the message to Slack
    send_slack_message(message)

if __name__ == "__main__":
    main()
