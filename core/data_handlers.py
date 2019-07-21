import collections
import json
import time
import requests

import math


# import os

# dir_path = os.path.dirname(os.path.realpath(__file__))


def worker(q, study_time):
    datahandler = DataHandler(q, study_time)

    while True:

        datahandler.update()

        if datahandler.exit_status:
            print("exiting")
            print("change_window_times: " + str(datahandler.change_window_times))
            break


class DataHandler:
    raspberry_post_address = 'http://192.168.18.23:5000/'

    change_window_times = []
    exit_status = False

    headers = {'content-type': 'application/json'}

    takkonis_durations = []
    productive_durations = []

    interval_takkonis_durations = collections.defaultdict(lambda: [0])
    interval_productive_durations = collections.defaultdict(lambda: [0])
    interval = 1
    old_interval = 1

    check_point = 0
    last_check_point = 0

    rgb_metric = 0
    matrix_metric = (1,1)
    previous_metric = 0

    takkonis = False

    rgb_metric_graph = []
    dt_graph = 0.5  # in seconds
    duration = 240
    matrix_interval = duration / 16

    def __init__(self, q, study_time):
        self.last_check_point = time.time()
        self.start_time = self.last_check_point
        self.q = q
        self.interval_start_time = self.last_check_point
        self.interval_checkpoint = self.last_check_point
        self.interval_last_checkpoint = self.last_check_point
        self.duration = study_time

        print("DURATION: " + str(self.duration))

        time.sleep(0.001)

    def update(self):
        # print("In update")
        self.check_point = time.time()
        self.interval_checkpoint = self.check_point
        # self.rgb_metric = self.current_productiveness()
        # self.matrix_metric = self.interval_productiveness()

        if not self.q.empty():
            print("----------------")
            print("Queue not empty\n\n")
            if self.takkonis:
                self.takkonis_durations.append(self.check_point - self.last_check_point)
                self.interval_takkonis_durations[self.interval-1].append(self.interval_checkpoint - self.interval_last_checkpoint)

            else:
                self.productive_durations.append(self.check_point - self.last_check_point)
                self.interval_productive_durations[self.interval-1].append(self.interval_checkpoint - self.interval_last_checkpoint)

            # print(str(self.interval_takkonis_durations))
            # print(str(self.interval_productive_durations))

            self.takkonis = self.q.get()
            self.last_check_point = self.check_point
            self.interval_last_checkpoint = self.interval_checkpoint
            # if queue_variable == 'exit':
            #     self.exit_status = True

        #print(self.rgb_metric)
        self.rgb_metric = self.current_productiveness()
        self.matrix_metric = self.interval_productiveness()

        #print(self.matrix_metric)

        if self.interval != self.old_interval:
            norm_height = self.previous_metric

            height = math.ceil((norm_height * 7) + 0.001)

            height -= int(height == 8)

            print(height)
            print("metric: " + str(self.previous_metric) + '\n\n')

            matrix_data = json.dumps({'matrix':height})

            r = requests.post(url=self.raspberry_post_address + "matrixdata", data=matrix_data, headers=self.headers)

            self.old_interval = self.interval



        self.previous_metric = self.matrix_metric[1]

        #print(self.matrix_metric)


        rgb_post = requests.post(url=self.raspberry_post_address + "rgblivedata", data=json.dumps({'rgb':self.rgb_metric}), headers=self.headers)
        # print(self.rgb_metric)
        # print(self.takkonis)








        #print(self.matrix_metric)

    def current_productiveness(self):
        dt = self.check_point - self.last_check_point

        # print("dt: " + str(dt))

        productive_time = sum(self.productive_durations)
        takko_time = sum(self.takkonis_durations)

        total_time = productive_time + takko_time + dt

        return (productive_time + (dt * int(not self.takkonis))) / total_time

    def interval_productiveness(self):
        dt = self.interval_checkpoint - self.interval_last_checkpoint

        productive_time = sum(self.interval_productive_durations[self.interval - 1])
        takko_time = sum(self.interval_takkonis_durations[self.interval - 1])

        if dt + productive_time + takko_time > self.matrix_interval:
            self.interval += 1
            self.interval_start_time = self.check_point
            self.interval_checkpoint = self.check_point
            self.interval_last_checkpoint = self.check_point
            dt = 0


        #print("interval: " + str(self.interval))


        #print(productive_time + dt * (int(not self.takkonis)))

        #print(productive_time )#+ (dt * int(not self.takkonis)))

        # if (productive_time + (dt * int(not self.takkonis))) / self.matrix_interval > 1:
        #     print("greater than zero")

        return (self.interval,(productive_time + (dt * int(not self.takkonis))) / self.matrix_interval )