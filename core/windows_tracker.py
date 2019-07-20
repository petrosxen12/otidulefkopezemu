from time import sleep
from multiprocessing import Process, Queue
from flask import app, request, escape, Flask

import win32gui as wp

import data_handlers as workers

app = Flask(__name__)

blacklist_file = open("blacklist.txt", "r")
# blacklist = list(blacklist_file.readlines())
blacklist = [x.strip('\n') for x in blacklist_file.readlines()]
print(blacklist)

q = Queue()
p = Process(target=workers.worker, args=(q,))


def is_in_blacklist(windowtitle):
    window_name = windowtitle.lower()
    print(window_name)

    for title in blacklist:
        if title in window_name:
            print("BLACKLIST")
            # q.put(True)
        else:
            pass
            # q.put(False)


def get_active_window():
    # print("test")
    while True:
        window_name = wp.GetWindowText(wp.GetForegroundWindow())
        if(old_window_name is not window_name and is_in_blacklist(window_name)):
            q.put(True)

        old_window_name = wp.GetWindowText(wp.GetForegroundWindow())
        # print("Current window is: %s" % window_name)
        # print(is_in_blacklist(window_name))

        sleep(1)


@app.route('/')
def hello():
    name = request.args.get("name", "hello")
    return f'Hello {escape(name)}'


if __name__ == '__main__':
    p.start()
    get_active_window()
    app.run()
