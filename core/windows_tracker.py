from multiprocessing import Process, Queue
from time import sleep

import data_handlers as workers
import win32gui as wp

blacklist_file = open("blacklist.txt", "r")
# blacklist = list(blacklist_file.readlines())
blacklist = [x.strip('\n') for x in blacklist_file.readlines()]
print(blacklist)

q = Queue()
p = Process(target=workers.worker, args=(q,))


def is_in_blacklist(windowtitle):
    window_name = windowtitle.lower()
    print(window_name)
    in_blacklist = False

    for title in blacklist:
        if title in window_name:
            print("BLACKLIST\n")
            in_blacklist = True
            q.put(True)

    if not in_blacklist:
        print("Not in BLACKLIST")
        q.put(False)


def get_active_window():
    # print("test")
    old_window_name = wp.GetWindowText(wp.GetForegroundWindow())

    while True:
        window_name = wp.GetWindowText(wp.GetForegroundWindow())

        if window_name != old_window_name:
            print("window has changed\n")

            is_in_blacklist(window_name)

            old_window_name = wp.GetWindowText(wp.GetForegroundWindow())

        # print("Current window is: %s" % window_name)
        # print(is_in_blacklist(window_name))

        sleep(1)


# if __name__ == '__main__':
#     p.start()
#     get_active_window()

def run():
    p.start()
    get_active_window()
