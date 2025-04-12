import threading
from queue import Queue, Empty
import serial
import time

class SerialReader(threading.Thread):
    def __init__(self):
        super().__init__()
        
        self.running = True
        self.queue = Queue()
        self.t1 = 0
        self.t2 = 0
        self.dt = 0
        self.com = "COM9"
        self.lock_com = None
        self.start_searching()
        self.thread = threading.Thread(target=self.read_from_port)
        
    def start(self):
        self.running = True
        self.thread.start()
    
    def read_from_port(self):
        while self.running:
            try:
                
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.read_until(b'\n').decode('utf-8').strip()
                    
                    if len(data) != 0:
                        # print(data)
                        self.queue.put(data)
                    else:
                        self.t1 = time.time()
                        self.dt = self.t1-self.t2
                        self.t2 = time.time()
                        if self.dt > 10 :
                            print(1)
                            print(self.dt)
                            raise Exception("Didn't receive message for over 10 seconds")
            except Exception as e:
                print(e)
                self.start_searching()
            time.sleep(0.001)
    def write_to_port(self,msg):
        if msg == None:
            return
        self.serial_port.write(msg)
    def start_searching(self):
        try:
            self.serial_port.close()
        except Exception as e:
            pass
        self.t2 = time.time()
        try:     
            print("Connecting...")
            key = True
            i = 0
            while(key):
                try:
                    if(self.lock_com == None):
                        self.com = 'COM'+str(i)
                    
                    self.serial_port = serial.Serial(port = 'COM'+str(i), baudrate= 112500, bytesize=8)

                    key = False
                    print('Success')
                    break
                except Exception as e:
                    key = True
                i += 1
                if i == 50:
                    i = 0
        
        except Exception as e:
            print(e) 
    def stop(self):
        self.running = False
        try:    
            self.serial_port.close()
        except Exception as e:
                print("lost connection")
                self.start_searching()
    def get_data(self):
        data_list = []
        while True:
            try:
                data = self.queue.get_nowait()
                data_list.append(data)
            except Empty:
                break
        return data_list
    
        

def example():
    serial_reader = SerialReader()
    serial_reader.start()

    try:
        print("Main thread is running...")
        
        while True:
            serial_reader.write_to_port(b'hi')
            data = serial_reader.get_data()
            if data:
                for item in data:
                    print(f"Main thread received: {item}")
            else:
                pass
            
            
            time.sleep(0.001)
    except KeyboardInterrupt:
        serial_reader.stop()
        print("Stopped serial reader...")

if __name__ == "__main__":
    example()