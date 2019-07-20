from flask import Flask, request
from multiprocessing import Process, Queue
from time import sleep
import data_handlers as workers

app = Flask(__name__)

@app.route('/dataendpoint', methods=['POST'])
def getFormData():
    if request.method == 'POST':
        data = request.form
        print(data)
        print('currently in pre process')

        return data
    else:
        return "Post endpoint."

q = Queue()
p = Process(target=workers.worker, args=(q,))

def run():
    p.start()
    getFormData()