import json 
import numpy as np
import sys
import os

def convert_accumulator_info(line,file):
    
    if line == '		}]\n':
        print('hi')
        file.write('\t\t}\n')
        return
    print(line)
    file.write(line)
    return

def convert_temperature(line,file):
    if line[5:8].isnumeric():
        print(line[5:8])
        
        file.write('\t\t\t '+line[5:8]+',\n')
        return
    elif line[5:7].isnumeric():
        print(line[5:7])
        if line[5:7] == '79':
            file.write('\t\t\t '+line[5:7]+'\n')
            file.write('\t\t\t '+'		],\n')
            return
        file.write('\t\t\t '+line[5:7]+',\n')
        return
    elif line[5:6].isnumeric():
        print(line[5:6])
        
        file.write('\t\t\t '+line[5:6]+',\n')
        return

def convert_voltages(line,file):
    if line[5:8].isnumeric():
        print(line[5:8])
        if line[5:8] == '143':
            file.write('\t\t\t '+line[5:8]+'\n')
            file.write('\t\t\t '+'		],\n')
            return
        file.write('\t\t\t '+line[5:8]+',\n')
        return
    elif line[5:7].isnumeric():
        print(line[5:7])
        file.write('\t\t\t '+line[5:7]+',\n')
        return
    elif line[5:6].isnumeric():
        print(line[5:6])
        
        file.write('\t\t\t '+line[5:6]+',\n')
        return
#f = open('python\prom_bms\main_project\example.json')

f = open(os.path.join(sys.path[0],"ex.json"), "r")
x = open(os.path.join(sys.path[0],"edit.json"), "w")


mode = 0
for y in f:
    if y == '	"Voltages":	[{\n':
        x.write('{\n')
        x.write('\t"Voltages":[\n')
        mode = 1
        continue

    if y == '	"Temperatures":	[{\n':
        x.write('\t"Temperatures":[\n')
        mode = 2
        continue

    if y == '	"AccumulatorInfo":	[{\n':
        x.write('\t"AccumulatorInfo":{\n')
        mode = 3
        continue
    if mode == 1:
        convert_voltages(y,x)
        continue
    if mode == 2:
        convert_temperature(y,x)
        continue
    if mode == 3:
        convert_accumulator_info(y,x)
        continue


#data = json.load(f)
#print(str(data['AccumulatorInfo']['Imd_Error']))

f.close()
x.close()
    
    
  