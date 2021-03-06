import datetime as dt
import time as tm
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from queue import Queue
import threading
import random as rd


class Radar:

    def __init__(self, delay: int = 1, motion_pin: int = 20, stop_event: object = object, queue_object :object = None):
        if queue_object is not None: self.queue_object = queue_object.put
        self.delay = delay
        self.radar_object = MotionSensor(motion_pin)
        self.stop_event = stop_event
        self.thread_name = "Radar"

    def run_simple(self):
        while True:
            self.radar_object.wait_for_inactive()
            Message = "[Radar]: Motion detected at [{}]".format(dt.datetime.now())
            Arguments = [True, dt.datetime.now().strftime("%Y%m%d %H:%M:%S")]
            print(Message, Arguments)
            tm.sleep(self.delay)

    def run(self):
        while not self.stop_event.is_set():
            self.radar_object.wait_for_inactive()
            Message = "[Radar]: Motion detected at [{}]".format(dt.datetime.now())
            Arguments = [True, dt.datetime.now().strftime("%Y%m%d %H:%M:%S")]
            self.queue_object([self.thread_name, Message, Arguments])
            tm.sleep(self.delay)

            if self.stop_event.is_set():
                self.clean_up
                break
        
    def run_simulated(self):
        while not self.stop_event.is_set():
            tm.sleep(rd.randint(0,15)/10)
            Message = "[Radar]: Motion detected at [{}]".format(dt.datetime.now())
            Arguments = [True, dt.datetime.now().strftime("%Y%m%d %H:%M:%S")]
            self.queue_object([self.thread_name, Message, Arguments])
            tm.sleep(self.delay)

            if self.stop_event.is_set():
                self.clean_up
                break
    

    def clean_up(self):
        GPIO.cleanup()   

if __name__ == '__main__':
    process = Radar()
    process.run_simple()

    # queue_object = Queue(maxsize=100)
    # stop_event= threading.Event()
    # process = Radar(stop_event=stop_event, queue_object=queue_object)

    # radar_thread = threading.Thread(target=process.run)
    # radar_thread.daemon = True
    # radar_thread.start()
    
    # for x in range(0, 10):
    #     item = queue_object.get()
    #     print(item)
    #     queue_object.task_done()
    #     tm.sleep(1)

    # print("End program")
    # stop_event.set()