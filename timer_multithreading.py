import telegram_notifications
import time

def start_timer(stop_event, sec=10):
    for i in range(sec, -1, -1):
        time.sleep(1)
        print("Timer: {}".format(i))
        if i == 0: 
            telegram_notifications.send_notifications()
        if stop_event.is_set():
            break
