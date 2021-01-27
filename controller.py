import threading

from lcd_ui import UI


def input_thread(event_queue):
    while True:
        i = input()
        event_queue.put({'type':'input','val':i})

if __name__ == '__main__':
    ui = UI()

    ui_t = threading.Thread(target=ui.run)
    input_t = threading.Thread(target=input_thread, args=(ui.event_queue,),daemon=True)

    ui_t.start()
    input_t.start()

    ui_t.join()

