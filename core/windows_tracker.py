from time import sleep
from multiprocessing import Process, Queue

import win32gui as wp

import data_handlers as workers

blacklist_file = open("blacklist.txt", "r")
# blacklist = list(blacklist_file.readlines())
blacklist = [x.strip('\n') for x in blacklist_file.readlines()]
print(blacklist)

q = Queue()
p = Process(target=workers.worker, args=(q,))
p.start()


def is_in_blacklist(windowtitle):
    window_name = windowtitle.lower()
    print(window_name)

    for title in blacklist:
        if title in window_name:
            print("BLACKLIST")
            q.put(True)


def get_active_window():
    # print("test")
    while True:
        window_name = wp.GetWindowText(wp.GetForegroundWindow())
        print("Current window is: %s" % window_name)
        print(is_in_blacklist(window_name))
        sleep(1)


if __name__ == '__main__':
    get_active_window()
