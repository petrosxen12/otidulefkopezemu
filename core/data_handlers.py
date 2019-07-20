import time


# import os

# dir_path = os.path.dirname(os.path.realpath(__file__))


def worker(q):
    # hello hello
    datahandler = DataHandler(q)

    while True:

        datahandler.update()

        if datahandler.exit_status:
            print("exiting")
            print("change_window_times: " + str(datahandler.change_window_times))
            break


class DataHandler:
    change_window_times = []
    exit_status = False

    takkonis_durations = []
    productive_durations = []

    check_point = 0
    last_check_point = 0

    rgb_metric = 0

    takkonis = False

    rgb_metric_graph = []
    dt_graph = 0.5  # in seconds

    def __init__(self, q):
        self.last_check_point = time.time()
        self.q = q

        time.sleep(0.001)

    def update(self):
        # print("In update")
        self.check_point = time.time()
        self.rgb_metric = self.current_productiveness()

        if not self.q.empty():
            print("----------------")
            print("Queue not empty\n\n")
            if self.takkonis:
                self.takkonis_durations.append(self.check_point - self.last_check_point)

            else:
                self.productive_durations.append(self.check_point - self.last_check_point)

            self.takkonis = self.q.get()
            self.last_check_point = self.check_point
            # if queue_variable == 'exit':
            #     self.exit_status = True

        print(self.rgb_metric)

    def current_productiveness(self):
        dt = self.check_point - self.last_check_point

        # print("dt: " + str(dt))

        productive_time = sum(self.productive_durations)
        takko_time = sum(self.takkonis_durations)

        total_time = productive_time + takko_time + dt

        return (productive_time + (dt * int(not self.takkonis))) / total_time
