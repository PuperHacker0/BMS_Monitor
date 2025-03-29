import serial
import json 

import sys
import os
dict = {"Commands": {
              "read_sd":  False, 
              "command1": False, 
              "command2": False, 
              "command3": False, 
              "command4": False, 
              "command5": False
              }}

def read_usb(ser):
    x = 0
    buffer = []
    z = 0
    while True:
        if z == 100:
            f = open(os.path.dirname(os.path.abspath("queue.json")),"r")
            cmd = json.loads(f.read())
            f.close()
            send_command(ser,cmd)
            f = open(os.path.dirname(os.path.abspath("queue.json")),"w")
            cmd.update(dict)
            f = open(os.path.dirname(os.path.abspath("queue.json")),"w")
            json.dump(cmd, f)
            f.close()
            z = 0
        z+=1
        try:
            p1 = ser.read_until()
        except Exception as e:
            print(e)
            break

        try:
            p1 = p1.decode('UTF-8')
        except Exception as e:
            print(e)
            continue

        print(p1)
        if p1 =='}{\n':
            x +=1
            
            if x == 9:
                x = 1
                buffer.append('}\n')
                f = open(os.path.dirname(os.path.abspath("battery_data.json")),'w')
                f.writelines(buffer)
                f.close()
                del buffer[:]
            
            if x == 1:
                buffer.append('{\n')
                continue
            buffer.append(',\n')
            continue

        if x != 0:
            buffer.append(p1)



def send_command(usb,cmd):
    

    if cmd["Commands"]["read_sd"] == True:
        usb.write("\n"+str(cmd))
        
    if cmd["Commands"]["command1"] == True:
        usb.write("\n"+cmd)
        
    if cmd["Commands"]["command2"] == True:
        usb.write("\n"+cmd)
        
    if cmd["Commands"]["command3"] == True:
        usb.write("\n"+cmd)
        
    if cmd["Commands"]["command4"] == True:
        usb.write("\n"+cmd)
    

try:     
    while(True):

        print("Connecting...")
        key = True
        i = 0
        while(key):
            
            try:
                ser = serial.Serial(port = 'COM'+str(i), baudrate= 9600,bytesize=8)
                key = False
                print('Success')
            except Exception as e:
                key = True
            i += 1
            if i == 20:
                i = 0
        read_usb(ser)
except Exception as e:
    print(e)
    input('Press ENTER to exit')