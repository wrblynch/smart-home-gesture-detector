from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

class Idle_Detector:
    __num_samples = 250  # 2 seconds of data @ 50Hz
    __serial_name = ""
    __baud_rate = 115200
    __comms = None

    def __init__(self, __num_samples = None, __serial_name = None, __baud_rate = None, __comms = None):
        self.__num_samples = __num_samples 
        self.__serial_name = __serial_name
        self.__baud_rate = __baud_rate
        self.times = CircularList([], self.__num_samples)
        self.ax = CircularList([], self.__num_samples)
        self.ay = CircularList([], self.__num_samples)
        self.az = CircularList([], self.__num_samples)
        self.avg_x = CircularList([], self.__num_samples)

    def run(self):
        comms = Communication(self.__serial_name, self.__baud_rate)
        refresh_time = 0.1
        comms.clear()                   # just in case any junk is in the pipes
        comms.send_message("wearable")
        try:
            previous_time = 0
            while(True):
                message = comms.receive_message()
                if(message != None):
                    try:
                        (m1, m2, m3, m4) = message.split(',')
                    except ValueError:        # if corrupted data, skip the sample
                        continue

                    # add the new values to the circular lists
                    self.times.add(int(m1))
                    self.ax.add(int(m2))
                    self.ay.add(int(m3))
                    self.az.add(int(m4))
                    self.avg_x.add(np.average(self.ax[-50:]))

                    # if enough time has elapsed, clear the axis, and plot everything
                    current_time = time()
                    if (current_time - previous_time >= 5 and (self.avg_x[-1] < 1950 or self.avg_x[-1] > 1750)):
                        previous_time = current_time
                        comms.send_message("inactive")
                    elif (self.avg_x[-1] > 1950 or self.avg_x[-1] < 1750):
                        previous_time = current_time
                        comms.send_message("movement")
                    if (current_time - previous_time > refresh_time):
                        plt.clf()
                        plt.subplot(311)
                        plt.plot(self.ax)
                        plt.subplot(312)
                        plt.plot(self.ay)
                        plt.subplot(313)
                        plt.plot(self.az)
                        plt.show(block = False)
                        plt.pause(0.001)
        except(Exception, KeyboardInterrupt) as e:
            print(e)                     # Exiting the program due to exception
        finally:
            comms.send_message("sleep")  # stop sending data
            comms.close()