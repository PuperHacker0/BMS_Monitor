import sys
import os
def get_data():

    dict_data = {'Voltages':[],
                'Temperatures':[],
                "AccumulatorInfo":	{
                "Ams_Error": 0 ,
                "Imd_Error": 0 ,
                "AIR_P_Supp": 0 ,
                "AIR_M_Supp": 0 ,
                "AIR_P_State": 0 ,
                "AIR_M_State": 0 ,
                "over60_dclink": 0 ,
                "dc_dc_temp": 0 ,
                "HVroom_humidity": 0 ,
                "precharge_voltage": 0 ,
                "AIR_P_State_Int": 0 
            }
            }

    f = open(os.path.join(sys.path[0],"data.txt"), "r")
    for x in f:
        if x == 'Voltages\n':
            #print('found it')
            i = 1
            continue
        if x == 'AccumulatorInfo\n':
            #print('found it')
            i = 1
            continue
        if x == 'Ams_Error\n':
            i = 2
            continue
        if x == 'Imd_Error\n':
            i = 3
            continue
        if x == 'AIR_P_Supp\n':
            i = 4
            continue
        if x == 'AIR_M_Supp\n':
            i = 5
            continue
        if x == 'AIR_P_State\n':
            i = 6
            continue
        if x == 'AIR_M_State\n':
            i = 7
            continue
        if x == 'over60_dclink\n':
            i = 8
            continue
        if x == 'dc_dc_temp\n':
            i = 9
            continue
        if x == 'HVroom_humidity\n':
            i = 10
            continue
        if x == 'precharge_voltage\n':
            i = 11
            continue
        if x == 'AIR_P_State_Int\n':
            i = 12  
            continue 
        if i == 1: 
            dict_data['Voltages'].append(float(x))
        elif i == 2:
            dict_data['AccumulatorInfo']['Ams_Error'] = float(x)
        elif i == 3:
            dict_data['AccumulatorInfo']['Imd_Error'] = float(x)
        elif i == 4:
            dict_data['AccumulatorInfo']['AIR_P_Supp'] = float(x)
        elif i == 5:
            dict_data['AccumulatorInfo']['AIR_M_Supp'] = float(x)
        elif i == 6:
            dict_data['AccumulatorInfo']['AIR_P_State'] = float(x)
        elif i == 7:
            dict_data['AccumulatorInfo']['AIR_M_State'] = float(x)
        elif i == 8:
            dict_data['AccumulatorInfo']['over60_dclink'] = float(x)
        elif i == 9:
            dict_data['AccumulatorInfo']['dc_dc_temp'] = float(x)
        elif i == 10:
            dict_data['AccumulatorInfo']['HVroom_humidity'] = float(x)
        elif i == 11:
            dict_data['AccumulatorInfo']['precharge_voltage'] = float(x)
        elif i == 12:
            dict_data['AccumulatorInfo']['AIR_P_State_Int'] = float(x)
    f.close()
    return dict_data
