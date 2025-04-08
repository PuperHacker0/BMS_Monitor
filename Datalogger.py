#Datalogger class

import threading
import time
from queue import Queue, Empty

'''
To use the datalogger, first create a datalogger instanace
Then use the start() method to start the logging thread
Use the write() method to send data to write. The data needs to be convertible to string type
When done use the stop() method to stop the logger
    Note: stop() does not terminate the datalogger instance itself.
    It just stops the logger thread, so no data will be written to the file from the moment the method is called.
    However, we can still keep using the datalogger instance, for example to write messages to it but not have them stored in a file
    Restarting the logger with the start() method will resume logging to the file
    clear_log() can also be called AFTER stopping() the datalogger thread
The functions marked PRIVATE are not meant to be called by the user.
'''

class Datalogger():
    def __init__(self):
        #Create the inner queue where the data will be stored
        self.buffer = Queue()
        #self.buffer_size = 0 #Use this instead of qsize if needed
        self.buffer_limit = 4 #CHANGE THIS

        #Set the output filename for the log file
        self.output_filename = 'session_log.txt'
        
        #Create the inner thread which will be run when starting the logger
        self.thread = threading.Thread(target = self.PRIVATE_write_to_file)
        self.flush_buffer = False
        self.write_trigger = threading.Event()
        self.threadLock = threading.Lock()
        #If needed we can add an IMMEDIATE_TERMINATE to the while loop to stop the thread without emptying the queue (data will be lost)

        self.buffer_sampling_frequency = 5 #Check the queue for messages 5 times per second
        #Increase for faster sampling, decrease for less CPU hogging

        self.debug_mode = True

    def start(self):
        self.thread.start()
        self.write('Datalogger has started')

        if self.debug_mode:
            print('[DEBUG] Datalogger thread has started')
    
    def stop(self):
        self.flush_buffer = True

    def clear_log(self):
        f = open(self.output_filename, "w")
        f.write("\n")
        f.close()

        if self.debug_mode:
            print("[DEBUG] Log file cleared")

    def write(self, data): #Function to call from outside
        self.buffer.put_nowait((self.PRIVATE_get_timestamp_string(), data)) #A message is the time + the data

        #self.threadLock.acquire()
        #self.buffer_size += 1

        #if self.buffer.qsize() >= self.buffer_limit:
        #if self.buffer_size >= self.buffer_limit:
            #print(f"The buffer size is {self.buffer_size} so we called the logger function")
            #self.write_trigger.set()  # Wake up the thread
        #time.sleep(1)
        #self.threadLock.release()

    def PRIVATE_write_to_file(self): #Thread function to be kept running inside
        #while True: #THIS IS NOT CORRECT! DEBUG ONLY
            #self.write_trigger.wait()  # Wait until signalled by the writer function that the buffer needs to be flushed
            #self.write_trigger.clear() #Clear the trigger and proceed to flush the buffer
        
            #The thread will terminate once the flag is set to true, so we can kill it through the stop function
        while True:
            #if self.buffer_size > self.buffer_limit or self.flush_buffer:
            if self.buffer.qsize() > self.buffer_limit or self.flush_buffer:
                #Write to file when enough messages have come
                f = open(self.output_filename, "a")

                try:
                    while not self.buffer.empty():
                        datum = self.buffer.get_nowait() #Removes AND returns the item from the queue
                        f.write(datum[0] + ' ' + str(datum[1]) + '\n') #Datum[1]'s format can be processed/changed here
                        #data needs to be convertible to string
                except Queue.Empty:
                    pass #Nothing to write, complete this write cycle
                except Exception as e:
                    if self.debug_mode:
                        print(f"[DEBUG] Buffer write FAILED ({e}). Datalogger stopped.")
                    return

                f.close()

                #self.threadLock.acquire()
                #self.buffer_size = 0
                #self.threadLock.release()
                #print("buffer size set to 0")

                if self.debug_mode:
                    print("[DEBUG] Successfully wrote buffer data to file")
                    self.write('[DEBUG] Wrote chunk of size ' + str(self.buffer_limit))


                #Terminate the thread right after the queue has been emptied so that the remaining messages won't be lost
                if self.flush_buffer:
                    self.flush_buffer = False

                    if self.debug_mode:
                        print('[DEBUG] Datalogger thread stopped')
                    return
                    
                    
                #time.sleep(1 / self.buffer_sampling_frequency) #buffer sampling interval

    def PRIVATE_get_timestamp_string(self):
        return time.strftime("[%H:%M:%S]", time.localtime())

#Example use case
if __name__ == "__main__":
    dl = Datalogger()
    dl.start()

    for i in range(20):
        dl.write(i)
        #time.sleep(0.1)
        #print(dl.buffer_size, "")

    #dl.clear_log()
    #time.sleep(1)
    dl.stop() #Important!
    #dl.clear_log()