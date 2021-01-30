import threading

from lcd_ui import UI
from temp_controller_ui import build_ui

def input_thread(event_queue):
    while True:
        i = input()
        event_queue.put({'type':'input','val':i})

if __name__ == '__main__':
    temp_controller_ui = build_ui()
    ui = UI(temp_controller_ui)

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()

