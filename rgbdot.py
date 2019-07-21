from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from multiprocessing import Process, Queue

import RPi.GPIO as GPIO
import time
from flask import request, Flask

app = Flask(__name__)

serial = spi(port = 0, device = 0, gpio = noop())
device = max7219(serial, cascaded=2)

green = 18
blue = 12
red = 13

freq = 100
GPIO.setmode(GPIO.BCM)
GPIO.setup(blue,GPIO.OUT)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GREEN = GPIO.PWM(green,freq)
BLUE = GPIO.PWM(blue,freq)
RED = GPIO.PWM(red,freq)

def setrgb(rgb):
    RGB = rgb*100
    RUNNING = True
    GREEN.start(RGB)
    BLUE.start(1)
    RED.start(100-RGB)
    
@app.route('/matrixdata', methods=['POST'])
def matrix_data():                              #used for both
    if request.method == 'POST':
        data = request.get_json()               
        matrix = float(data.get('matrix'))
        print("MATRIX DATA: %f" % matrix)
        q.put(matrix)
        return 'matrix'
    

@app.route('/rgblivedata', methods=['POST'])
def rgb_data():
    if request.method == 'POST':
        data = request.get_json()
        rgb = float(data.get('rgb'))
        #print("RGB VALUE: %f" % rgb)
        setrgb(rgb)
        return 'rgb'
    
def inf_loop(q):
    #buffer = 0
    l = [0] * 16
    while True:                
        if not q.empty():
            buffer = q.get() #buffer is a single value og the last column to be given
            l.insert(0,buffer)
            del l[-1]
            if 0 not in l:
                show_message(device, "Break Time!", fill="white", font=proportional(CP437_FONT),scroll_delay = 0.1)
            print(l)
        with canvas(device) as draw:
            for i in range(16):
                draw.text((-2+i,5-l[i]),"|", fill = "white")
                
q = Queue()
p = Process(target=inf_loop, args = (q,))

        
if __name__ == '__main__':
    p.start()
    app.run(debug=True,host='0.0.0.0')
    
