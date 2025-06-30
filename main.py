import requests
import time
import os
from telegram import Bot
from keep_alive import keep_alive

PINNACLE_API_URL = "https://api.pinnacle.com/v1/odds?sportId=12&oddsFormat=Decimal&market=moneyline"
PINNACLE_AUTH = os.environ.get("PINNACLE_AUTH")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

DROP_PERCENTAGE = 10
CHECK_INTERVAL = 60

bot = Bot(token=TELEGRAM_TOKEN)
bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="🤖 Bot iniciado com sucesso!")

old_odds = {}

def get_odds():
    headers = {
        "Authorization": f"Basic {PINNACLE_AUTH}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(PINNACLE_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro: {e}")
        return None

def check_drops():
    global old_odds
    data = get_odds()
    if not data:
        return

    for league in data.get("leagues", []):
        for event in league.get("events", []):
            event_id = event["id"]
            for period in event.get("periods", []):
                for team, odd in period.get("moneyline", {}).items():
                    key = f"{event_id}_{team}"
                    if key in old_odds:
                        old = old_odds[key]
                        drop = ((old - odd) / old) * 100
                        if drop >= DROP_PERCENTAGE:
                            bot.send_message(
                                chat_id=TELEGRAM_CHAT_ID,
                                text=f"📉 Drop detectado!\nEquipe: {team}\nOdd antiga: {old}\nOdd nova: {odd}\n⏬ Queda: {drop:.2f}%"
                            )
                    old_odds[key] = odd

def main_loop():
    while True:
        check_drops()
        time.sleep(CHECK_INTERVAL)

keep_alive()
main_loop()