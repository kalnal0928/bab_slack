
import requests
import datetime

# Function to read API key from api.txt
def get_api_key():
    with open('api.txt', 'r') as f:
        return f.read().strip()

# Function to get meal data from the NEIS API
def get_meal_data():
    today = datetime.date.today().strftime("%Y%m%d")
    api_key = get_api_key()
    atpt_ofcdc_sc_code = "R10"
    sd_schul_code = "7681026"

    if not api_key:
        print("API 키를 찾을 수 없습니다.")
        return None

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        'KEY': api_key,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDC_SC_CODE': atpt_ofcdc_sc_code,
        'SD_SCHUL_CODE': sd_schul_code,
        'MLSV_YMD': today
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "mealServiceDietInfo" in data:
            return data["mealServiceDietInfo"][1]["row"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return None

# Function to format the meal data into a readable string
def format_meal_data(meal_data):
    if not meal_data:
        return "급식 정보가 없습니다."

    message = ""
    for meal in meal_data:
        message += f"[{meal['MMEAL_SC_NM']}]\n"
        # Replace <br/> with newline characters for better readability
        menu_items = meal['DDISH_NM'].replace("<br/>", "\n")
        message += f"{menu_items}\n\n"
    return message.strip()

if __name__ == '__main__':
    # Example usage:
    meal_info = get_meal_data()
    if meal_info:
        print(format_meal_data(meal_info))
    else:
        print("오늘 급식 정보가 없습니다.")

