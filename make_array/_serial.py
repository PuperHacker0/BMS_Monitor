import serial
import json 
import numpy as np
import sys
import os



def convert_accumulator_info(line,file):
    
    if line == '		}]\n':

        file.write('\t\t}}\n')
        return

    file.write(line)
    return

def convert_temperature(line,file):
    if line[5:8].isnumeric():

        
        file.write('\t\t\t '+line[12:17]+',\n')
        return
    elif line[5:7].isnumeric():

        if line[5:7] == '79':
            file.write('\t\t\t '+line[11:17]+'\n')
            file.write('\t\t\t '+'		],\n')
            return
        file.write('\t\t\t '+line[11:17]+',\n')
        return
    elif line[5:6].isnumeric():

        
        file.write('\t\t\t '+line[10:16]+',\n')
        return
    
def convert_moisture(line,file):
    if line[5:8].isnumeric():

        
        file.write('\t\t\t '+line[10:17]+',\n')
        return
    elif line[5:7].isnumeric():

        if line[5:7] == '15':
            file.write('\t\t\t '+line[11:17]+'\n')
            file.write('\t\t\t '+'		],\n')
            return
        file.write('\t\t\t '+line[11:16]+',\n')
        return
    elif line[5:6].isnumeric():

        
        file.write('\t\t\t '+line[10:15]+',\n')
        return

def convert_voltages(line,file):
    if line[5:8].isnumeric():

        if line[5:8] == '143':
            file.write('\t\t\t '+line[12:18]+'\n')
            file.write('\t\t\t '+'		],\n')
            return
        file.write('\t\t\t '+line[12:18]+',\n')
        return
    elif line[5:7].isnumeric():

        file.write('\t\t\t '+line[11:17]+',\n')
        return
    elif line[5:6].isnumeric():
        
        file.write('\t\t\t '+line[10:15]+',\n')
        return

def start_conversion(y):
    global mode, volt, moist, temp, accu
    
    if y == '	"Voltages":	[{\n':
        volt = open('BMS_LiveViewer/make_array/voltage.txt', 'w', encoding= 'utf-8')
        volt.write('{\n')
        volt.write('\t"Voltages":[\n')
        mode = 1
        return 
    
    if y == '	"Humidities":	[{\n':
        moist = open('BMS_LiveViewer/make_array/moisture.txt', 'w', encoding= 'utf-8')
        moist.write('\t"Humidities":[\n')
        mode = 2
        return 
    
    if y == '	"Temperatures":	[{\n':
        temp = open('BMS_LiveViewer/make_array/temperature.txt', 'w', encoding= 'utf-8')
        temp.write('\t"Temperatures":[\n')
        mode = 3
        return 

    if y == '	"AccumulatorInfo":	[{\n':
        accu = open('BMS_LiveViewer/make_array/accuinfo.txt', 'w', encoding= 'utf-8')
        accu.write('\t"AccumulatorInfo":{\n')
        mode = 4
        return 

    if mode == 1:
        if y == '}{\n':
            volt.close()
            mode = 0 
            return
        
        convert_voltages(y,volt)
        return 

    if mode == 2:
        if y == '}{\n':
            moist.close()
            mode = 0
            return
       
        convert_moisture(y,moist)
        return 
    
    if mode == 3:
        if y == '}{\n':
            temp.close() 
            mode = 0
            
            return

        convert_temperature(y,temp)
        return 
    
    if mode == 4:
        if y == '}{\n':
            accu.close()
            mode = 0
            filenames = ['BMS_LiveViewer/make_array/voltage.txt', 'BMS_LiveViewer/make_array/moisture.txt', 'BMS_LiveViewer/make_array/temperature.txt', 'BMS_LiveViewer/make_array/accuinfo.txt']
            with open('BMS_LiveViewer/make_array/battery_data.json', 'w') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
            return
        convert_accumulator_info(y,accu)
        return 

print("Connecting...")
key = True
while(key):
    try:
        ser = serial.Serial(port = 'COM10', baudrate= 9600,bytesize=8)
        key = False
        print('Success')
    except serial.serialutil.SerialException:
        key = True
global mode 
mode = 0
i = 0 
while True:
   
    p1 = ser.read_until()
    try:
        p1 = p1.decode('UTF-8')
    except UnicodeDecodeError:
        #i = i+1 #errors 766 5 min
        print(p1)
        continue




print(p1)

    
    
  