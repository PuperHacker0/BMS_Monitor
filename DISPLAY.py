from imports import*

from kivy.core.window import Window
color_test = [0,0,1,1]
battery_pos = [8,9,7,10,6,11,5,12,4,13,3,14,2,15,1,16,0,17]
battery_pos_x = [9,8,10,7,11,6,12,5,13,4,14,3,15,2,16,1,17,0]
battery_pos_reverse = [17,0,16,1,15,2,14,3,13,4,12,5,11,6,10,7,9,8]
battery_pos_reverse_x = [0,17,1,16,2,15,3,14,4,13,5,12,6,11,7,10,8,9]
# battery_pos = [9,8,10,7,11,6,12,5,13,4,14,3,15,2,16,1,17,0]
# battery_pos_reverse = [0,17,1,16,2,15,3,14,4,13,5,12,6,11,7,10,8,9]
# segment_pos = ["0","1","2","3","7","6","5","4"]
segment_pos = ["0","1","2","3","4","5","6","7"]
segment_pos_reversed = ["8","7","6","5","1","2","3","4"]

selected_tab = 0
battery_id_list = ['1','2','3','4',
                    '5','6','7','8',
                    '9','10','11','12',
                    '13','14','15','16',
                    '17','18']
battery_id_list_reversed = ['18','17','16','15',
                    '14','13','12','11',
                    '10','9','8','7',
                    '6','5','4','3',
                    '2','1']
ids_list = np.chararray((1,128),6, unicode = True)
ids_list.fill('None') 

global PLOT_MANUAL


class FILE_MENU(MDFloatLayout, HoverBehavior):
    pass
class VIEW_MENU(MDFloatLayout, HoverBehavior):
    pass
class BATTERY(ButtonBehavior,MDBoxLayout):
    select_state=[1,1,0,0]
    blink_val = BooleanProperty(False)
    mode = NumericProperty(0)
    balance_state = [0,0,0,1]
    def __init__(self,battery_id,segment_id,value,color,**kwargs ):
        super().__init__(**kwargs)
        
        self.battery_id = battery_id
        self.segment_id = segment_id
        self.full_id = 'S'+str(self.segment_id) + '-' + 'B'+str(self.battery_id)
        self.value = value
        with self.canvas.after:
            self.selection_color = Color(rgba = self.select_state)
            self.selection_points = Line(rectangle = [self.x, self.y, self.width, self.height],width = 3)
    def update_select_state(self,action):
        if action == True:
            # self.select_state
            self.selection_color.rgba=[1,1,0,1]
            
        if action == False:
            # self.select_state
            self.selection_color.rgba = self.colors
        
        # self.selection_color.rgba = self.select_state
        self.selection_points.rectangle =  [self.x, self.y, self.width, self.height]
        self.selection_points.width = 3
    def on_press(self):
        #print("BUTTO")
        pass

    def color_value(self,value,balance,mode):
        self.value = value
        self.mode = mode
        if balance == 1:
            self.ids.balance_id.text_color = 0,0,0,1
        else: 
            self.ids.balance_id.text_color = 0,0,0,0

        if value == None:
            self.colors =[.1,.1,.1,1]
            return
        
        if self.mode == 0:
            if value*4.2 > 4.2:
                self.colors = [1,1,1,1] 
                self.md_bg_color = self.colors
                return
            elif value*4.2 < 2.5:
                self.colors = [0,0,0,1]
                self.md_bg_color = self.colors
                return
            else:
                
                if self.value*4.2 > 2.5 and self.value * 4.2 < 3.50000: 

                    self.colors = [1-self.value,1,0,1]
                    self.md_bg_color = self.colors
                    return
                
                
        if self.mode == 1:
            if value == 255:
                self.colors = [0,0,0,0]

            else:
                if value > 70:
                    self.colors = [0.3, 0, 0, 1]
                elif 30 <= value <= 60:
                    self.colors = [value / 60, value / (2 * 60), 1-(value/60), 1]
                else:
                    self.colors = [value / 60, value / (2 * 60), 1-(value/60), 1]

                


            
            self.md_bg_color = self.colors

        if self.mode == 2:
                
            if self.value == 0 or self.value > 60:
                self.value = 0

            if self.value <= 60:
                value = self.value /100
                self.colors = [1-self.value,1-self.value,self.value,1]
                self.md_bg_color = self.colors
    
    def balance_state(self,value):
        if value == 1:
            self.ids.icon.color = 0,0,0,1
            return
        self.ids.icon.color = 0,0,0,0   

    def blink(self):
        self.blink_val = not self.blink_val      
        if self.blink_val:
            self.select_state = [1,1,0,1]
            temp = 3
        else:    
            self.select_state = self.colors
            temp = 3
        self.selection_color.rgba = self.select_state
        self.selection_points.width = temp

class SEGMENT(GridLayout):
    
    def __init__(self,segment_id,value, **kwargs):
        super().__init__(**kwargs)
        self.segment_id = segment_id
        self.value = value    
        if int(self.segment_id) < 5:    
            # print("segment ID" + str(self.segment_id))
            for i in battery_pos_reverse_x:
                # print(battery_id_list[i])
                self.b = BATTERY(battery_id_list[i],self.segment_id,None,[.1,.1,.1,1],md_bg_color = [0,0,1,1])
                self.add_widget(self.b)
                self.ids[battery_id_list[i]] = self.b
        else:
            # print("segment ID" + str(self.segment_id))
            for i in battery_pos_x:
                # print(battery_id_list[i])
                self.b = BATTERY(battery_id_list[i],self.segment_id,None,[.1,.1,.1,1],md_bg_color = [0,0,1,1])
                self.add_widget(self.b)
                self.ids[battery_id_list[i]] = self.b

    def set_colors(self,value,balance ,mode):

        #print('value is')
        #print(str(self.value))
       
        for i in battery_pos:
            try:
                if (mode == 2):
                   temp = value 
                else:
                    temp = value[i]
                # print("temp is "+ str(temp))
            except IndexError:
                temp = 0
            self.ids[battery_id_list[i]].color_value(temp,balance[i],mode) 

class SEGMENT_LAYOUT(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in segment_pos:
            self.s = SEGMENT(segment_pos_reversed[int(i)],None)
            self.add_widget(self.s)
            self.ids[segment_pos_reversed[int(i)]] = self.s

class MyScatter(Scatter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mousex, mousey = Window.mouse_pos
        box_pos_x,box_pos_y = self.x*2,self.y*2
         
        self.scale = .3 
        self.x = 230
        self.y = 185
    def on_touch_down(self, touch):
        mousex, mousey = Window.mouse_pos
        box_pos_x,box_pos_y = self.pos
        # Override Scatter's `on_touch_down` behavior for mouse scroll
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                # print('down')
                ## zoom in
                if self.scale < 10:
                    self.scale = self.scale * 1.1
                    self.x = box_pos_x - ((mousex-box_pos_x)*0.1)
                    self.y = box_pos_y - ((mousey-box_pos_y)*0.1)
            elif touch.button == 'scrollup':
                ## zoom out
                # print('up')
                #if self.scale > 1:
                self.scale = self.scale * 0.9
                self.x = box_pos_x - ((mousex-box_pos_x)*(-.1))
                self.y = box_pos_y - ((mousey-box_pos_y)*(-.1))
                # print(str(self.scale))
                # If some other kind of "touch": Fall back on Scatter's behavior
        else:
            super(MyScatter, self).on_touch_down(touch)
            # print(str(self.pos))

class BOX_VIEWER(StencilView, MDBoxLayout):

    def add_menu(self):
        self.menu = FILE_MENU()
        self.add_widget(self.menu)
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BOX_VIEWER, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BOX_VIEWER, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(BOX_VIEWER, self).on_touch_up(touch)

class MyScatterLayout(Scatter):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ms = MyScatter(pos = self.pos)
        self.add_widget(self.ms)
        self.ids['segments'] = self.ms

class SplitterStrip(SplitterStrip):
    pass
class Content(MDBoxLayout):

    def __init__(self,panel_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.panel_number = panel_number 

class CUSTOM_BOTTON(ButtonBehavior,Label):
    pass

class MyToggleButton(MDFlatButton, MDToggleButton):
    pass

class SELECT_TYPE(MDBoxLayout):

    def type_interface(self,x):
        #print('in')
        pass

class OPTIONS(MDBoxLayout):

    panel_number = NumericProperty(0)
    
    def add_panel(self):
        self.panel_number+=1
        self.panel = MDExpansionPanel(
                    icon = "chart-scatter-plot",
                    content=Content(self.panel_number),
                    panel_cls=MDExpansionPanelOneLine(
                        text=str("Panel"+str(self.panel_number))
                    )
                )
        self.ids.select_plot_box.add_widget(self.panel)
        self.ids.select_plot_box.ids['panel'+str(self.panel_number)] = self.panel
    def update_panel_info(self):
        f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'r')
        manual = json.loads(f.read())
        for i in range(1,self.panel_number+1):
            self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.text = manual[i]
            self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.secondary_text = manual["Panel"+str(i)]["Name"]
            if not(bool(manual["Cell ID"]) and bool("Cell Data Type") and bool("Screen")):
                self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.color = 1,0,0,1
                continue
            if not(bool(manual["Segment ID"]) and bool("Segment Data Type") and bool("Screen")):
                self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.color = 1,0,0,1
                continue
            if not(bool(manual["Box Info"]) and bool("Box Data Type") and bool("Screen")):
                self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.color = 1,0,0,1
                continue
            self.ids.select_plot_box.ids['panel'+ str(i)].content.ids.panel_info.color = 0,0,0,1
    def remove_panel(self,x):
        
        for i in range(1,self.panel_number+1):
        
            if self.ids.select_plot_box.ids['panel'+ str(i)].content.panel_number == x:
                temp = self.ids.select_plot_box.ids['panel'+ str(i) ]
                self.ids.select_plot_box.remove_widget(temp)

class PLOT_SETTINGS(ScrollView):

    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.panel_id = id

class MIN_SIDE_WINDOW(MDStackLayout):
    window = NumericProperty(0)

class SIDE_WINDOW(Splitter,BoxLayout):
    window = NumericProperty(0)
    
    def __init__(self,caller_id, **kwargs):
        super().__init__(**kwargs)
        # print(self.window)
        self.i = 0
        self.battery_id = caller_id
        self.bty = Tab(title = f"[ref={caller_id}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]  {caller_id}")
        self.ids.tabs.add_widget(self.bty)
        self.ids.tabs.ids[self.battery_id] = self.bty
        if caller_id == 'BOX_INFO' :
            self.ids.tabs.ids[self.battery_id].add_box_info()
        elif caller_id == 'TOOLS':
            self.ids.tabs.ids[self.battery_id].add_options()
        elif caller_id[0:1] == 'S':
            self.ids.tabs.ids[self.battery_id].add_contents()
        elif caller_id[0:1] == 'P':
            self.ids.tabs.ids[self.battery_id].add_plot_settings(caller_id)
        
        ids_list[0][self.i] = self.battery_id

    def num_children(self):
        print(str(self.children))
    def add_tab(self,caller_id):
        #print(ids_list)
        if caller_id in ids_list:
            return
        self.i += 1
        print(caller_id)
        self.bty = Tab(title = f"[ref={caller_id}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]  {caller_id}")
        ids_list[0][self.i] = caller_id
        self.ids.tabs.add_widget(self.bty)
        self.ids.tabs.ids[caller_id] = self.bty  
        
        self.ids.tabs.switch_tab(f"[ref={caller_id}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]  {caller_id}",search_by = 'title')
        #print(self.ids.tabs.ids[self.battery_id].ids)       

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    voltage_text = StringProperty()      
    

    def add_box_info(self):
        self.scv = MDScrollView()
        self.add_widget(self.scv)
        self.ids['scroll'] = self.scv

        self.controller= MDBoxLayout(orientation = 'vertical', padding = dp(10))
        self.ids.scroll.add_widget(self.controller)
        self.ids.scroll.ids['controller'] = self.controller

        self.Ams_Error_text = 'Ams_Error: -'
        self.Ams_Error = MDLabel(text= self.Ams_Error_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Ams_Error)
        self.ids.scroll.ids.controller.ids['Ams_Error'] = self.Ams_Error

        self.Imd_Error_text = 'Imd_Error: -'
        self.Imd_Error = MDLabel(text= self.Imd_Error_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Imd_Error)
        self.ids.scroll.ids.controller.ids['Imd_Error'] = self.Imd_Error

        self.AIR_P_Supp_text = 'AIR_P_Supp: -'
        self.AIR_P_Supp = MDLabel(text= self.AIR_P_Supp_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.AIR_P_Supp)
        self.ids.scroll.ids.controller.ids['AIR_P_Supp'] = self.AIR_P_Supp

        self.AIR_M_Supp_text = 'Ams_Error: -'
        self.AIR_M_Supp = MDLabel(text= self.AIR_M_Supp_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.AIR_M_Supp)
        self.ids.scroll.ids.controller.ids['AIR_M_Supp'] = self.AIR_M_Supp

        self.AIR_P_State_text = 'AIR_P_State: -'
        self.AIR_P_State = MDLabel(text= self.AIR_P_State_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.AIR_P_State)
        self.ids.scroll.ids.controller.ids['AIR_P_State'] = self.AIR_P_State

        self.AIR_M_State_text = 'AIR_M_State: -'
        self.AIR_M_State = MDLabel(text= self.AIR_M_State_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.AIR_M_State)
        self.ids.scroll.ids.controller.ids['AIR_M_State'] = self.AIR_M_State

        self.over60_dclink_text = 'over60_dclink: -'
        self.over60_dclink = MDLabel(text= self.over60_dclink_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.over60_dclink)
        self.ids.scroll.ids.controller.ids['over60_dclink'] = self.over60_dclink

        self.dc_dc_temp_text = 'dc_dc_temp: -'
        self.dc_dc_temp = MDLabel(text= self.dc_dc_temp_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.dc_dc_temp)
        self.ids.scroll.ids.controller.ids['dc_dc_temp'] = self.dc_dc_temp

        self.HVroom_humidity_text = 'HVroom_humidity: -'
        self.HVroom_humidity = MDLabel(text= self.HVroom_humidity_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.HVroom_humidity)
        self.ids.scroll.ids.controller.ids['HVroom_humidity'] = self.HVroom_humidity

        self.precharge_voltage_text = 'precharge_voltage: -'
        self.precharge_voltage = MDLabel(text= self.precharge_voltage_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.precharge_voltage)
        self.ids.scroll.ids.controller.ids['precharge_voltage'] = self.precharge_voltage

        self.AIR_P_State_Int_text = 'AIR_P_State_Int: -'
        self.AIR_P_State_Int = MDLabel(text= self.AIR_P_State_Int_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.AIR_P_State_Int)
        self.ids.scroll.ids.controller.ids['AIR_P_State_Int'] = self.AIR_P_State_Int

        self.V_Side_Voltage_text = 'V_Side_Voltage: -'
        self.V_Side_Voltage = MDLabel(text= self.V_Side_Voltage_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.V_Side_Voltage)
        self.ids.scroll.ids.controller.ids['V_Side_Voltage'] = self.V_Side_Voltage

        self.Current_text = 'Current: -'
        self.Current = MDLabel(text= self.Current_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Current)
        self.ids.scroll.ids.controller.ids['Current'] = self.Current

        self.Ah_consumed_text = 'Ah_consumed: -'
        self.Ah_consumed = MDLabel(text= self.Ah_consumed_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Ah_consumed)
        self.ids.scroll.ids.controller.ids['Ah_consumed'] = self.Ah_consumed

        self.Energy_Consumed_text = 'Energy Consumed: -'
        self.Energy_Consumed = MDLabel(text= self.Energy_Consumed_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Energy_Consumed)
        self.ids.scroll.ids.controller.ids['Energy_Consumed'] = self.Energy_Consumed

        self.Target_Voltage_text = 'Target_Voltage: -'
        self.Target_Voltage = MDLabel(text= self.Target_Voltage_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Target_Voltage)
        self.ids.scroll.ids.controller.ids['Target_Voltage'] = self.Target_Voltage

        self.Output_Voltage_text = 'Output_Voltage: -'
        self.Output_Voltage = MDLabel(text= self.Output_Voltage_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Output_Voltage)
        self.ids.scroll.ids.controller.ids['Output_Voltage'] = self.Output_Voltage

        self.Target_Current_text = 'Target_Current: -'
        self.Target_Current = MDLabel(text= self.Target_Current_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Target_Current)
        self.ids.scroll.ids.controller.ids['Target_Current'] = self.Target_Current

        self.Output_Current_text = 'Output_Current: -'
        self.Output_Current = MDLabel(text= self.Output_Current_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Output_Current)
        self.ids.scroll.ids.controller.ids['Output_Current'] = self.Output_Current

        self.Elcon_connected_text = 'Elcon_connected: -'
        self.Elcon_connected = MDLabel(text= self.Elcon_connected_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Elcon_connected)
        self.ids.scroll.ids.controller.ids['Elcon_connected'] = self.Elcon_connected

        self.Elcon_AC_input_OK_text = 'Elcon_AC_input_OK: -'
        self.Elcon_AC_input_OK = MDLabel(text= self.Elcon_AC_input_OK_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Elcon_AC_input_OK)
        self.ids.scroll.ids.controller.ids['Elcon_AC_input_OK'] = self.Elcon_AC_input_OK

        self.CANBUS_Error_text = 'CANBUS_Error: -'
        self.CANBUS_Error = MDLabel(text= self.CANBUS_Error_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.CANBUS_Error)
        self.ids.scroll.ids.controller.ids['CANBUS_Error'] = self.CANBUS_Error

        self.Target_charge_state_text = 'Target_charge_state: -'
        self.Target_charge_state = MDLabel(text= self.Target_charge_state_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Target_charge_state)
        self.ids.scroll.ids.controller.ids['Target_charge_state'] = self.Target_charge_state

        self.Elcon_charge_status_text = 'Elcon_charge_status: -'
        self.Elcon_charge_status = MDLabel(text= self.Elcon_charge_status_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Elcon_charge_status)
        self.ids.scroll.ids.controller.ids['Elcon_charge_status'] = self.Elcon_charge_status

        self.Elcon_overtemp_text = 'Elcon_overtemp: -'
        self.Elcon_overtemp = MDLabel(text= self.Elcon_overtemp_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.Elcon_overtemp)
        self.ids.scroll.ids.controller.ids['Elcon_overtemp'] = self.Elcon_overtemp

    def add_contents(self):  
        self.scv = MDScrollView()
        self.add_widget(self.scv)
        self.ids['scroll'] = self.scv

        self.controller= MDBoxLayout(orientation = 'vertical', padding = dp(10))
        self.ids.scroll.add_widget(self.controller)
        self.ids.scroll.ids['controller'] = self.controller
        self.voltage_text = 'Voltages: -'
        self.voltage = MDLabel(text= self.voltage_text,halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.voltage)
        self.ids.scroll.ids.controller.ids['volt_val'] = self.voltage
        
        self.temperature = MDLabel(text='Temperature: ',halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.temperature)
        self.ids.scroll.ids.controller.ids['temp_val'] = self.temperature
        
        self.moisture = MDLabel(text='Moisture: ',halign="left", size_hint=[1,.1],theme_text_color = 'Custom',text_color= [1, 1, 1, 1])
        self.ids.scroll.ids.controller.add_widget(self.moisture)
        self.ids.scroll.ids.controller.ids['moist_val'] = self.moisture # c:

        self.graph_box = MDBoxLayout(orientation = 'vertical',md_bg_color = [.18,.18,.18,1])
        self.ids.scroll.ids.controller.add_widget(self.graph_box)
        self.ids.scroll.ids.controller.ids['graph_box'] = self.graph_box
        
        self.graph = GRAPH_OBJ()
        self.ids.scroll.ids.controller.ids.graph_box.add_widget(self.graph)
        self.ids.scroll.ids.controller.ids.graph_box.ids['graph'] = self.graph
        self.graph.set_values()

    def add_options(self):
        self.scv = MDScrollView()
        self.add_widget(self.scv)
        self.ids['scroll'] = self.scv

        self.controller= MDBoxLayout(orientation = 'vertical', padding = dp(10))
        self.ids.scroll.add_widget(self.controller)
        self.ids.scroll.ids['controller'] = self.controller

        self.options = OPTIONS()
        self.ids.scroll.ids.controller.add_widget(self.options)
        self.ids.scroll.ids.controller.ids['options'] = self.options

    def category_select(self,x):
        print(x)
        if x ==0:
            self.pls.ids.Type.ids.Type_con.type_interface(0) 
        if x == 1:           
            self.pls.ids.Type.ids.Type_con.type_interface(1)
            return
        if x == 2:
            self.pls.ids.Type.ids.Type_con.type_interface(2) 
            return
        
    def on_text(instance, value):
        print('The widget', instance.ids, 'have:', value.hint_text)
        print(str(instance.ids)[2:8])
        print(value.hint_text)
        print(value.text)
        x = str(instance.ids)[2:8]
        y = value.hint_text
        z = value.text 
        f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'r')
        t0 = t1 = t2 = t3 = t4 = t5 = t6 = t7 = None
        try:
            manual = json.loads(f.read())
            f.close()
        except json.decoder.JSONDecodeError:
            f.close()
            f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'w')
            f.write('{\n\n}')
            f.close()
            f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'r')
            manual = json.loads(f.read())
            
            f.close()
       
        if x in manual:
            # print("yew")
            manual[x][y] = z
            f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'w')
            new_f = json.dumps(manual, indent=4)
            f.writelines(new_f)
            print(f)
            f.close()
            
            return
        
        if y == 'Name':
            t0 = z 
        if y == 'Cell ID':
            t1 = z 
        if y == 'Segment ID':
            t2 = z 
        if y == 'Box Info':
            t3 = z 
        if y == 'Cell Data Type':
            t4 = z 
        if y == 'Segment Data Type':
            t5 = z
        if y == 'Box Data Type':
            t6 = z  
        if y == 'Screen':
            t7 = z  
        
        dict = {
                x:{
                "Name"              : t0 ,
                "Cell ID"           : t1 ,
                "Segment ID"        : t2 ,
                "Box Info"          : t3 ,
                "Cell Data Type"    : t4 ,
                "Segment Data Type" : t5 ,
                "Box Data Type"     : t6 ,
                "Screen"            : t7
            }
        }
        
        f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json")), 'w')
        manual.update(dict)
        json.dump(manual,f)
        print(f)
        f.close()
        #value.hint_text = value.text 
        
    def add_plot_settings(self,x):
        self.pls = PLOT_SETTINGS(x)
        self.add_widget(self.pls)
        self.ids[x]= self.pls

#------------------------------------------------------------------#
        self.txt = MDTextField(mode = 'rectangle',
                               
                               fill_color_normal = [.5,.5,.5,1],
                               background_color = [1,0,0,1], 
                               helper_text_color_normal = "white",
                                hint_text = "Name",
                               pos_hint={"left": 1, "center_y": 0.5}
                               )
        self.pls.ids.Edit_name.add_widget(self.txt)
        self.txt.bind(on_text_validate=self.on_text)
#------------------------------------------------------------------#

        self.cell_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                hint_text = "Cell ID",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                    )
        self.pls.ids.Edit_id.add_widget(self.cell_id)
        self.cell_id.bind(on_text_validate=self.on_text)
        self.Segment_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                hint_text = "Segment ID",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                    )
        self.pls.ids.Edit_id.add_widget(self.Segment_id)
        self.Segment_id.bind(on_text_validate=self.on_text)
        self.box_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                hint_text = "Box info",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                    )
        self.pls.ids.Edit_id.add_widget(self.box_id)
        self.box_id.bind(on_text_validate=self.on_text)
#------------------------------------------------------------------#
        self.cell_data_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                helper_text_color_normal = "white",
                                hint_text = "Cell Data Type",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                )
        self.pls.ids.Type.add_widget(self.cell_data_id)
        self.cell_data_id.bind(on_text_validate=self.on_text)
        
        self.segment_data_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                hint_text = "Segment Data Type",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                )
        self.pls.ids.Type.add_widget(self.segment_data_id)
        self.segment_data_id.bind(on_text_validate=self.on_text)
        
        self.box_data_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                #line_color_normal =  [1,1,1,1],
                                hint_text = "Box Data Type",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                )
        self.pls.ids.Type.add_widget(self.box_data_id)
        self.box_data_id.bind(on_text_validate=self.on_text)

        self.screen_id = MDTextField(
                                hint_text_color_focus =  "red",
                                
                                #line_color_normal =  [1,1,1,1],
                                hint_text = "Screen",
                                helper_text_color_normal = "white",
                                pos_hint={"left": 1, "center_y": 0.5},
                                size_hint =[1,1]
                                )
        self.pls.ids.Screen.add_widget(self.screen_id)
        self.screen_id.bind(on_text_validate=self.on_text)


    def update_selected(self,volt,temp,hum,_id):
        #self.graph.update(volt)
        
        try:
            self.ids.scroll.ids.controller.ids['volt_val'].text= 'Voltage: ' + str(volt)[:7]
            self.ids.scroll.ids.controller.ids['temp_val'].text= 'Temperature: ' + str(temp)[:8]
            self.ids.scroll.ids.controller.ids['moist_val'].text= 'Humidity: ' + str(hum)[:8]
        except Exception as e:
            print(str(e) + "line 723 DISPLAY")

        
        