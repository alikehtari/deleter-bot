import time
import signal
import sys
from database import get_latest_update_id, save_update_id, connect_to_database
from telegram import get_updates, delete_message

def process_updates():
    latest_update_id = get_latest_update_id() + 1

    while True:
        updates = get_updates(latest_update_id)  # Assuming this fetches updates from an API
        if updates:
            for update in updates:
                update_id = update.get("update_id")
                
                # Use .get() for null-safe access
                message = update.get("message", {})
                chat = message.get("chat", {})
                message_id = message.get("message_id")
                chat_id = chat.get("id")

                if update_id is not None:  # Ensure update_id is valid
                    save_update_id(update_id)  # Save update_id to database
                    
                    # Proceed only if both chat_id and message_id are valid
                    if chat_id and message_id:
                        delete_message(chat_id, message_id)  # Delete the message

                    # Update the offset for the next API call
                    latest_update_id = update_id + 1

        time.sleep(2)  # Adjust interval as needed

def handle_exit(signal, frame):
    print("Exiting gracefully...")
    if connect_to_database():
        connect_to_database().close()
    sys.exit(0)

if __name__ == "__main__":
    # Signal handling for graceful termination
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        process_updates()
    except Exception as e:
        print(f"Unexpected error: {e}")
        handle_exit(None, None)
