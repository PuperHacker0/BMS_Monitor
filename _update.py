from imports import* 
from read_file import*
from DISPLAY import*


acc_zeros = ['0.000','0.000','0.000','0.000','0.000','0.000',
             '0.000','0.000','0.000','0.000','0.000']
acc_list = ["Ams_Error", "Imd_Error", "AIR_P_Supp", "AIR_M_Supp",
            "AIR_P_State", "AIR_M_State", "over60_dclink", "dc_dc_temp", 
            "HVroom_humidity", "precharge_voltage", "AIR_P_State_Int"]
class OFFSET(MDFloatLayout):
     pass
class ACC_TEXT(MDLabel):
    def __init__(self,label,value, **kwargs):
        super().__init__(**kwargs)
        size_hint_y = None
        height = dp(5)
        
        self.label = label
        self.value = str(value)
        self.text = str(self.label)+': '+str(self.value)
    def update(self,x):
        self.value = x
        self.text = '   > '+ str(self.label)+': '+str(self.value)



def update_battery_color(self): 
        convert_values_to_color(self)
        # #print("volt : " + str(self.volt))
        # #print("temp : " + str(self.temp))
        # #print("hum : " + str(self.hum))
        
        if self.mode == 0:
            for i in range(0,8):
                try: 
                    self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(int(segment_pos[i])+1)].set_colors(self.volt[i],self.balance[i],self.mode)
                except Exception as e:
                    pass
        if self.mode == 1:
            try:
                for i in range(0,8):
                    self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(int(segment_pos[i])+1)].set_colors(self.temp[i],self.balance[i],self.mode)
            except Exception as e:
                pass
        if self.mode == 2:
            z = 0
            for i in range(0,16,2):
                try:      
                    # #print(self.hum)
                    if self.hum[i] == 255:
                        hum = self.hum[i+1]
                        # #print("took +1 " + str(hum))
                    else:
                        hum = self.hum[i] 
                        # #print("took i " + str(hum))
                    self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(int(segment_pos[z])+1)].set_colors(hum,self.balance[z],self.mode)
                    z += 1
                except Exception as e:
                    pass
def convert_values_to_color(self):  
    try:
        np.temp = self.data["Balancing"]
        np.blnc = np.array(self.data["Balancing"])
        np.blnc = np.blnc.reshape(8,18)
        self.balance = np.blnc
    except Exception as e:
        self.balance_error +=1
    try:
        np.temp = self.data['Voltages']
        np.temp = self.Arrdiv5(np.temp)
        np.temp = np.temp.reshape(8,18)
        self.volt = np.temp
    except Exception as e:
        self.voltages_error +=1

    try:
        np.temp = np.array(self.data['Temperatures'])
        # print(np.temp)
        np.temp = np.temp.reshape(8,18)
        self.temp = np.temp
        # print(self.temp)
    except Exception as e:  
        # print(e)
        self.temperature_error +=1          
        
    try:
        self.hum = self.data['Humidities']        
        
    except Exception as e:
        self.humidities_error +=1
            
def div5(x):
    if x == None:
        return 0
    return float(x/4.2)

def update_acc_data(self,data):
    label_link = self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids.BOX_INFO.ids.scroll.ids.controller.ids
    ##print(self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids.BOX_INFO.ids.scroll.ids.controller.ids)
    try:
        label_link.Imd_Error.text = "Imd_Error: " + str(data["AccumulatorInfo"]["Imd_Error"]) 
        label_link.Ams_Error.text = "Ams_Error: " + str(data["AccumulatorInfo"]["Ams_Error"]) 
        label_link.AIR_P_Supp.text = "AIR_P_Supp: " + str(data["AccumulatorInfo"]["AIR_P_Supp"]) 
        label_link.AIR_M_Supp.text = "AIR_M_Supp: " + str(data["AccumulatorInfo"]["AIR_M_Supp"]) 
        label_link.AIR_P_State.text = "AIR_P_State: " + str(data["AccumulatorInfo"]["AIR_P_State"]) 
        label_link.AIR_M_State.text = "AIR_M_State: " + str(data["AccumulatorInfo"]["AIR_M_State"]) 
        label_link.over60_dclink.text = "over60_dclink: " + str(data["AccumulatorInfo"]["over60_dclink"]) 
        label_link.dc_dc_temp.text = "dc_dc_temp: " + str(data["AccumulatorInfo"]["dc_dc_temp"]) 
        label_link.HVroom_humidity.text = "HVroom_humidity: " + str(data["AccumulatorInfo"]["HVroom_humidity"]) 
        label_link.precharge_voltage.text = "precharge_voltage: " + str(data["AccumulatorInfo"]["precharge_voltage"]) 
        label_link.AIR_P_State_Int.text = "AIR_P_State_Int: " + str(data["AccumulatorInfo"]["AIR_P_State_Int"]) 
    except Exception as e:
        pass
    try:
        label_link.V_Side_Voltage.text = "V_Side_Voltage: " + str(data["Isabelle Info"]["V_Side_Voltage"]) 
        label_link.Current.text = "Current: " + str(data["Isabelle Info"]["Current"]) 
        label_link.Ah_consumed.text = "Ah_consumed: " + str(data["Isabelle Info"]["Ah_consumed"]) 
        label_link.Energy_Consumed.text = "Energy_Consumed: " + str(data["Isabelle Info"]["Energy Consumed"]) 
    except Exception as e:
        pass
    try:
        label_link.Target_Voltage.text = "Target_Voltage: " + str(data["Elcon Info"]["Target_Voltage"]) 
        label_link.Output_Voltage.text = "Output_Voltage: " + str(data["Elcon Info"]["Output_Voltage"]) 
        label_link.Target_Current.text = "Target_Current: " + str(data["Elcon Info"]["Target_Current"]) 
        label_link.Output_Current.text = "Output_Current: " + str(data["Elcon Info"]["Output_Current"]) 
        label_link.Elcon_connected.text = "Elcon_connected: " + str(data["Elcon Info"]["Elcon_connected"]) 
        label_link.Elcon_AC_input_OK.text = "Elcon_AC_input_OK: " + str(data["Elcon Info"]["Elcon_AC_input_OK"]) 
        label_link.CANBUS_Error.text = "CANBUS_Error: " + str(data["Elcon Info"]["CANBUS_Error"]) 
        label_link.Target_charge_state.text = "Target_charge_state: " + str(data["Elcon Info"]["Target_charge_state"]) 
        label_link.Elcon_charge_status.text = "Elcon_charge_status: " + str(data["Elcon Info"]["Elcon_charge_status"]) 
        label_link.Elcon_overtemp.text = "Elcon_overtemp: " + str(data["Elcon Info"]["Elcon_overtemp"]) 
    except Exception as e:
        pass



def update_tab(self,seg,bat):
    

    
    try:
        if self.temp[int(seg)-1][int(bat)-1] == 255:
            temp_address = 0.000
        else:
            temp_address = self.temp[int(seg)-1][int(bat)-1]
    except Exception as e:
        pass
       
    try:
        temp_seg = int(seg)
        if temp_seg == 2:
            temp_seg = 3
        elif temp_seg == 3:
            temp_seg = 5
        elif temp_seg == 4:
            temp_seg = 7
        elif temp_seg == 5:
            temp_seg = 9
        elif temp_seg == 6:
            temp_seg = 11
        elif temp_seg == 7:
            temp_seg = 13
        elif temp_seg == 8:
            temp_seg = 15

        if self.hum[int(temp_seg)-1] == 255:
            hum_address = self.hum[int(temp_seg)]
        else:
            hum_address = self.hum[int(temp_seg)-1]

    except Exception as e:
        pass
        #print(str(e)+"line 165 _update")
        # hum_address = "Error"
    try:
        self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids['S'+ str(seg) + '-' + 'B'+str(bat)].update_selected(self.volt[int(seg)-1][int(bat)-1]*4.2,temp_address,hum_address,self.c)
        # self.count+=1
        
       
    except Exception as e:
        #print(str(e)+" line 177 _update")
        pass


    