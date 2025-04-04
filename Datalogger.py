#Datalogger class

import threading
import time
from queue import Queue, Empty

class Datalogger():
    def __init__(self):
        #Create the inner queue where the data will be stored
        self.buffer = Queue()
        self.buffer_size = 0
        self.buffer_limit = 10
        self.output_filename = 'session_log.txt'
        
        #Create the inner thread which will be run
        self.thread = threading.Thread(target = self.write_to_file)
        self.expired = False

    def start(self):
        self.thread.start()
        self.write('Datalogger has started')

    def write_to_file(self): #Thread function to be kept running inside
        while not self.expired: #Hopefully this will allow the thread to terminate on its own
            if self.buffer_size > self.buffer_limit: #Write to file when enough messages have come
                #Start writing to the file
                f = open(self.output_filename, "a")

                try:
                    while not self.buffer.empty():
                        datum = self.buffer.get_nowait() #Removes AND returns the item from the queue
                        f.write(datum[0] + ' ' + str(datum[1]) + '\n') #Datum[1]'s format can be processed/changed here
                        #data needs to be convertible to string
                except Exception as e:
                    print("[DEB] Buffer write FAILED")
                    return

                f.close()
                print("[DEB] Successfully wrote buffer data to file")
                self.buffer_size = 0
                
    def clear_log():
        f = open(self.output_filename, "w")
        f.write("\n")
        f.close()

    def get_timestamp_string(self):
        return time.strftime("[%H:%M:%S]", time.localtime())

    def stop(self):
        self.expired = True

    def write(self, data): #Function to call from outside
        self.buffer.put_nowait((self.get_timestamp_string(), data)) #A message is the time + the data
        self.buffer_size += 1

if __name__ == "__main__":
    dl = Datalogger()
    dl.start()

    for i in range(16):
        dl.write(i)

    dl.stop()