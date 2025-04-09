import requests
import time
import random

THINGSPEAK_API_KEY = "X6PKV4KQCRUDUIAQ"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

BOT_TOKEN = "7700164579:AAGn-SiojOmPQha2TGOQLY3zLAXkNOJKDOQ"
CHAT_ID = "5699715536"

# 허용 범위 설정
TEMP_MIN = 20.0
TEMP_MAX = 28.0
HUM_MIN = 40.0
HUM_MAX = 65.0

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.get(url, params=params)
    print("📨 텔레그램 전송 결과:", response.text)

while True:
    
    temperature = round(random.uniform(18.0, 32.0), 1)
    humidity = round(random.uniform(35.0, 75.0), 1)

    print(f"📡 온도: {temperature}°C, 습도: {humidity}%")

    
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': temperature,
        'field2': humidity
    }

    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        print("✅ Thingspeak 응답:", response.text)
    except Exception as e:
        print("❌ Thingspeak 전송 실패:", e)

    # 텔레그램 경고 조건
    if temperature < TEMP_MIN:
        send_telegram_message(f"🌡️ 온도 낮음! 현재 {temperature}℃ (허용: {TEMP_MIN}℃ 이상)")
    elif temperature > TEMP_MAX:
        send_telegram_message(f"🌡️ 온도 높음! 현재 {temperature}℃ (허용: {TEMP_MAX}℃ 이하)")

    if humidity < HUM_MIN:
        send_telegram_message(f"💧 습도 낮음! 현재 {humidity}% (허용: {HUM_MIN}% 이상)")
    elif humidity > HUM_MAX:
        send_telegram_message(f"💧 습도 높음! 현재 {humidity}% (허용: {HUM_MAX}% 이하)")

    time.sleep(15)