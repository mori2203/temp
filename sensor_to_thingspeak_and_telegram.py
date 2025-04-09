import Adafruit_DHT
import requests
import time

DHT_SENSOR = Adafruit_DHT.DHT22  
DHT_PIN = 4  # GPIO4

THINGSPEAK_API_KEY = "aaaaaaaaaaa"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

BOT_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaa"
CHAT_ID = "5699715536"

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
    try:
        response = requests.get(url, params=params)
        print("📨 텔레그램 전송 결과:", response.text)
    except Exception as e:
        print("❌ 텔레그램 전송 실패:", e)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        temperature = round(temperature, 1)
        humidity = round(humidity, 1)

        print(f"📡 측정 → 온도: {temperature}°C, 습도: {humidity}%")

        try:
            payload = {
                "api_key": THINGSPEAK_API_KEY,
                "field1": temperature,
                "field2": humidity
            }
            response = requests.get(THINGSPEAK_URL, params=payload)
            print("✅ Thingspeak 응답:", response.text)
        except Exception as e:
            print("❌ Thingspeak 전송 실패:", e)

        if temperature < TEMP_MIN:
            send_telegram_message(f"🌡️ 온도 낮음! 현재 {temperature}℃ (허용: {TEMP_MIN}℃ 이상)")
        elif temperature > TEMP_MAX:
            send_telegram_message(f"🌡️ 온도 높음! 현재 {temperature}℃ (허용: {TEMP_MAX}℃ 이하)")

        if humidity < HUM_MIN:
            send_telegram_message(f"💧 습도 낮음! 현재 {humidity}% (허용: {HUM_MIN}% 이상)")
        elif humidity > HUM_MAX:
            send_telegram_message(f"💧 습도 높음! 현재 {humidity}% (허용: {HUM_MAX}% 이하)")
    else:
        print("⚠️ 센서 읽기 실패")

    time.sleep(15) 
