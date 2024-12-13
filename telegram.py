import requests

BOT_TOKEN = "6637153495:AAEhbedK3Wuez0sQzlYD2CyP_FOQtqm72Po"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates(offset):
    try:
        response = requests.get(f"{BASE_URL}/getUpdates?offset={offset}", timeout=10)
        response.raise_for_status()
        return response.json()["result"]
    except requests.RequestException as e:
        print(f"Telegram API error: {e}")
        return []

def delete_message(chat_id, message_id):
    try:
        response = requests.get(
            f"{BASE_URL}/deleteMessage?chat_id={chat_id}&message_id={message_id}",
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to delete message {message_id}: {e}")
