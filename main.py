import threading

from acquisition.manager import start as start_ble
from acquisition.udp_receiver import run as run_udp
from acquisition.fake_source import run as run_fake

from analytics.scx import worker as scx_worker

from core.bus import event_bus
from core.buffer import push

from ui.dashboard import run as run_ui


def buffer_worker():
    while True:
        event = event_bus.get()
        # print(event)
        push(event)

def main():
    threading.Thread(target=buffer_worker, daemon=True).start()
    # threading.Thread(target=run_ble, daemon=True).start()
    # threading.Thread(target=run_udp, daemon=True).start()
    # threading.Thread(target=run_fake, daemon=True).start()
    start_ble()
    threading.Thread(target=scx_worker, daemon=True).start()
    run_ui()


if __name__ == "__main__":
    main()