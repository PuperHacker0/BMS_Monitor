from imports import*
from DISPLAY import*
from _update import*
import time
from usbDash import SerialReader as sr
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
Window.size = (1280, 720)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
selected_tab = 0

class TOP_BUTTONS(Button):
    pass
class MENU(MDBoxLayout,HoverBehavior):
    pass
class TOP_BAR(RelativeLayout):
    pass

class BOTTOM_BAR(MDBoxLayout):
    pass

class MainScreen(Screen):
    
    tabs_open = NumericProperty(0)
        
    def open_side_menu(self,caller_id):
        
        self.tabs_open += 1
        if self.tabs_open ==1:
            self.sw = SIDE_WINDOW(caller_id,window = 0)
            self.ids.window_controller.add_widget(self.sw)
            self.ids.window_controller.ids['side_w'] = self.sw
            global selected_tab 
            selected_tab = 1
        else:
            # #print('tabs open '+str(self.tabs_open))
            self.ids.window_controller.ids.side_w.add_tab(caller_id)
              
    def close(self):
        self.tabs_open = 0
        
        for i in range(1,8):
            for z in range(1,18):
                if i == 1 and z == 1:
                    print("here")
                try:
                    print("before "+str(self.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(i)].ids[str(z)].selection_color.rgba))
                    self.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(i)].ids[str(z)].update_select_state(False)
                    #print("after "+str(self.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(i)].ids[str(z)].selection_color.rgba))
                    self.ids.window_controller.ids.viewer.ids.box.ids.self.segments.ids.grid.ids[str(i)].ids[str(z)].update_select_state(False)
                except Exception as e:
                    print(str(e)+ " line 46 main")
        ids_list.fill('None')
        global selected_tab 
        selected_tab = 0
        ##print(ids_list)
        self.ids.window_controller.remove_widget(self.sw)
        #print("closed")
    def minimize(self):
        self.min_sw = MIN_SIDE_WINDOW(window = 0)
        self.ids.window_controller.remove_widget(self.sw)
        self.ids.window_controller.add_widget(self.min_sw)
    def expand(self):
        self.ids.window_controller.remove_widget(self.min_sw)
        self.ids.window_controller.add_widget(self.sw)

class GraphController(MDBoxLayout):

    num_lines = NumericProperty(0)
    num_plots = NumericProperty(0)
    plot = [[]]
    manual = {}
    line = [[]]
    x_data = []
    y_data = [[]]
    fig = [[]]
    ax = [[]]
    labels = []

    def add_plot(self,manual,panel_id):
        if manual["Segment ID"] == "ALL":
            self.bar_plot(manual,panel_id)
            return
        self.fig.append([])
        self.ax.append(int(panel_id[5]))
        
        self.fig[int(panel_id[5])], self.ax[int(panel_id[5])] = plt.subplots(figsize=(10, 8))

        self.ax[int(panel_id[5])].set_facecolor('black')
        
        self.fig[int(panel_id[5])].set_figwidth(1) # set the width of the figure
        self.fig[int(panel_id[5])].set_figheight(1) # set the height of the figure
        self.fig[int(panel_id[5])].set_facecolor('#0000') # set the background color of the figure
        self.ax[int(panel_id[5])].spines['bottom'].set_color('white')
        self.ax[int(panel_id[5])].spines['top'].set_color('white') 
        self.ax[int(panel_id[5])].spines['right'].set_color('white')
        self.ax[int(panel_id[5])].spines['left'].set_color('white')
        self.ax[int(panel_id[5])].tick_params(axis='x', colors='white')
        self.ax[int(panel_id[5])].tick_params(axis='y', colors='white')


        if (bool(manual["Cell ID"]) and bool(manual["Segment ID"])) or (bool(manual["Segment ID"]) and bool(manual["Box Info"])) or (bool(manual["Cell ID"]) and bool(manual["Box Info"])):           
            return

        if manual["Cell ID"] != None:
            z = manual["Cell ID"]
        if manual["Segment ID"] != None:
            z = manual["Segment ID"]
        if manual["Box Info"] != None:
            z = manual["Box Info"]
        self.line.append([])
        self.y_data.append([])
        #print(len(self.y_data[int(panel_id[5])]))
        self.line[int(panel_id[5])], = self.ax[int(panel_id[5])].plot(self.x_data, self.y_data[int(panel_id[5])],label = z)
           

        #line, = self.ax.plot(self.x_data, y_data)
        self.fig[int(panel_id[5])].suptitle(manual["Name"])

        # Add the plot to the Kivy app
        
        self.plot.append([]) 
        
        self.plot[int(panel_id[5])] = FigureCanvasKivyAgg(figure=self.fig[int(panel_id[5])])
        self.ids[manual["Screen"]].add_widget(self.plot[int(panel_id[5])])
        self.ids[manual["Screen"]].ids[panel_id] = self.plot[int(panel_id[5])]
        
    def update_all_plots(self,_data):
        ##print(self.x_data)
        if self.manual["Panel1"]["Segment ID"] == "ALL" :
            self.update_bars(_data,self.manual)
            return
        
        if len(self.x_data) == 1000:
            x = np.arange(self.x_data[999], self.x_data[999]+10,1)
            x = x.tolist()
            ##print("x = " + str(x))
            #print("x_data before : " + str(len(self.x_data)))
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            self.x_data.pop(0)
            ##print("x_data before: "+ str(len(self.x_data)))

            #print("x_data during: " + str(len(self.x_data)))
            self.x_data.extend(x)
            #print("x_data after: " + str(len(self.x_data)))
            ##print(self.x_data[0])
        else:     
            x = np.arange(len(self.x_data), len(self.x_data) + 10)

            self.x_data.extend(x)
        for i in range(1,self.num_plots):
 
            self.update_plot(_data,i)
            
    def update_plot(self,data,_id):
        self.data = data

        if _id > self.num_plots:
            return
        #print("_id : " + str(_id))
        # Add the new data to the plot
        if self.manual["Panel"+str(_id)]["Cell ID"] != None:
            j = self.manual["Panel"+str(_id)]["Cell ID"]
            j = (int(j[1])*18) - 18 + int(j[4])
            y = self.data[self.manual["Panel"+str(_id)]["Cell Data Type"]][j]

        if self.manual["Panel"+str(_id)]["Segment ID"] != None:
            j = self.manual["Panel"+str(_id)]["Segment ID"]
            j = (int(j[1])*18) - 18 
            y = 0
            for z in range(1,18):
                y += int(self.data[self.manual["Panel"+str(_id)]["Segment Data Type"]][j+z])
            y /= 18 
        if self.manual["Panel"+str(_id)]["Box Info"] != None:
            y = int(self.data[self.manual["Panel"+str(_id)]["Box Info"]][self.manual["Panel"+str(_id)]["Box Data Type"]])

        self.line[_id].set_xdata(self.x_data)
        if len(self.y_data[_id]) == 1000:
            #print("y_data before: "+ str(len(self.y_data[_id])))
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            self.y_data[_id].pop(0)
            #print("y_data during: "+ str(len(self.y_data[_id])))
            self.y_data[_id].extend([y]*10)
            #print("y_data after: "+ str(len(self.y_data[_id])))
            #print(self.x_data)
        else:
            self.y_data[_id].extend([y]*10)
            #print(len(self.y_data[_id]))
            
        self.line[_id].set_ydata(self.y_data[_id])
        # Redraw the plot
        try:
            self.ax[int(_id)].relim()
        except ValueError:
            print("id : "+ str(_id))
            #print("length : y_data = "+str(len(self.y_data[_id])))
            #print("length : x_data = "+ str(len(self.x_data) ))
            #print("y_data table :")
            #print(self.y_data[_id])
            #print("x_data table :")
            #print(self.x_data)
        self.ax[int(_id)].autoscale_view()
        self.plot[_id].draw()
        # if len(self.y_data[_id]) == 1000:
        #     self.loading.dismiss()
        #     return
        # self.loading.dismiss()
    def bar_plot(self,manual,_id):
        #print(self.ids)
        self.plot = []
        self.fig = []
        self.ax = []
        # #print("in")
        self.fig, self.ax = plt.subplots()
        
        bar_width = 1
        for i in range(1,145):
            self.labels.append("B"+str(i)) 

        # #print(self.labels)
        # self.ax.set_xticks(np.arange(144))
        #print(manual)
        if manual["Segment Data Type"] == "Voltages":
            self.bar1 = self.ax.bar(np.arange(144)  ,0, bar_width,color = 'g')
        elif manual["Segment Data Type"] == "Temperatures": 
            self.bar1 = self.ax.bar(np.arange(144)  ,1, bar_width,color = 'r')
        elif manual["Segment Data Type"] == "Humidities":
            self.bar1 = self.ax.bar(np.arange(16)   ,2, bar_width,color = 'b')
        self.plot =  FigureCanvasKivyAgg(figure=self.fig)
        self.ids["top_left"].add_widget(self.plot)
        self.ids["top_left"].ids["ALL"] = self.plot
        #print(self.ids)


        # #print(self.ids["top_left"].ids)
        self.ax.relim()
        self.ax.autoscale_view()
        self.plot.draw()
        # #print("done")
    def update_bars(self,data,manual):
        
        if manual["Panel1"]["Segment Data Type"] == "Voltages" and data.get("Voltages"):
            ymax = data["Voltages"][0]
            ymin = data["Voltages"][0]
            for i, rect in enumerate(self.bar1):
                if data["Voltages"][i] != 255:
                    rect.set_height(data["Voltages"][i])
                    if data["Voltages"][i] > ymax:
                        ymax = data["Voltages"][i]
                    if data["Voltages"][i] < ymin:
                        ymin = data["Voltages"][i]
                    self.ax.set_ylim([ymin-0.005,ymax+0.005])
                else:
                    rect.set_height(0)
        elif manual["Panel1"]["Segment Data Type"] == "Temperatures" and data.get("Temperatures"): 
            for i, rect in enumerate(self.bar1):
                try:
                    if data["Temperatures"][i] != 255: 
                        rect.set_height(data["Temperatures"][i])
                    else:
                        rect.set_height(0)
                except Exception as e:
                    if e == IndexError or e ==KeyError:
                        rect.set_height(0)
        elif manual["Panel1"]["Segment Data Type"] == "Humidities" and data.get("Humidities"):
            for i, rect in enumerate(self.bar1):
                try:
                    if data["Humidities"][i] != 255:
                        rect.set_height(data["Humidities"][i])
                    else:
                        rect.set_height(0)
                except IndexError:
                        rect.set_height(0)
        self.ax.relim()
        self.ax.autoscale_view()
        self.plot.draw()

class GraphView(Screen):
    tabs_open = NumericProperty(0)
    on_ = NumericProperty(0)
    off_ = NumericProperty(0)
    sw_is_open = NumericProperty(0)
    def close_graphs(self):
        pass
    def on_leave(self):
        self.ids.window_controller.clear_widgets()
        self.on_ = 0
        #print("on_ : "+ str(self.on_))
        
    def open_side_menu(self,caller_id):
        self.tabs_open += 1
        if self.tabs_open ==1:
            self.sw = SIDE_WINDOW(caller_id,pos_hint={'right': 1},window = 1)
            self.ids.window_controller.add_widget(self.sw)
            self.ids.window_controller.ids['side_w'] = self.sw
            global selected_tab 
            selected_tab = 1
        else:
            ##print('tabs open '+str(self.tabs_open))
            self.ids.window_controller.ids.side_w.add_tab(caller_id)
    def on_enter(self):
        #print("on enter : " +str(self.on_))
        if self.on_ == 0:
            self.grc = GraphController()
            self.ids.window_controller.add_widget(self.grc)
            self.ids.window_controller.ids['grc'] = self.grc
            #self.grc.add_plot('S1-B2','Voltage','top_right',1)
            #print("in if : " +str(self.on_))
        self.on_ = 1
        #print("on after : " +str(self.on_))
    def check_layout(self):
        try:
            f = open(os.path.dirname(os.path.abspath("PLOT_MANUAL.json"))+"\\PLOT_MANUAL.json", 'r')
            self.manual = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            return 
        self.grc.num_plots = len(self.manual)
        #print('num of plots: '+str(len(self.manual)))
        
        for i in range(1, len(self.manual)+1):
            
            try:
                self.grc.add_plot(self.manual["Panel"+str(i)],"Panel"+str(i))
            except IndexError:
                print(str(i))
        
        self.grc.manual = self.manual
    def close(self):
        self.tabs_open = 0
        self.ids.window_controller.remove_widget(self.sw)
        #print("closed")
    def minimize(self):
        self.min_sw = MIN_SIDE_WINDOW(window = 1)
        self.ids.window_controller.remove_widget(self.sw)
        self.ids.window_controller.add_widget(self.min_sw)
    def expand(self):
        self.ids.window_controller.remove_widget(self.min_sw)
        self.ids.window_controller.add_widget(self.sw)

class ScreenController(ScreenManager):

    def switch_screen(self):
        if self.current == 'main':
            self.current='graphv'
            return
        self.current='main'
        return

class App(MDApp):
    graph_segment_id = StringProperty("None")
    menu_open = NumericProperty(0)
    mode = NumericProperty(0)
    plot = NumericProperty(0)
    balance_error = NumericProperty(0)
    voltages_error = NumericProperty(0)
    temperature_error = NumericProperty(0)
    humidities_error = NumericProperty(0)
    first = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen= Builder.load_file("Layout.kv")
        self.count = 0

        self.bvw = BOX_VIEWER()
        self.screen.ids.main.ids.window_controller.add_widget(self.bvw)
        self.screen.ids.main.ids.window_controller.ids['viewer'] = self.bvw
        self.data = {}
        
        
        self.Arrdiv5=np.vectorize(div5)
        Clock.schedule_interval(self.update,1/60)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
    
        x = instance_tab.title[5:13]

        if x[0:1] == 'S':

            a = bytearray(instance_tab.title[6:7], encoding='UTF-8')
            b = bytearray(instance_tab.title[9:11], encoding='UTF-8')
            b = b.decode('UTF-8')
            a = a.decode('UTF-8')    
            if not b.isnumeric():
                b = bytearray(instance_tab.title[9:10], encoding='UTF-8')
                b = b.decode('UTF-8')
            
            self.c = 'S'+a+'-'+'B'+b
            self.graph_segment_id = a
            self.graph_battery_id = b 
        elif x[0:1] == 'P':
            
            a = bytearray(instance_tab.title[10:11], encoding='UTF-8')
            a = a.decode('UTF-8')    
            if not a.isnumeric():
                a= bytearray(instance_tab.title[10:11], encoding='UTF-8')
                a = a.decode('UTF-8')
            ##print(a)
            self.c = 'Panel'+ a
            self.graph_segment_id = 'None'
            self.graph_battery_id = 'None'
            
        elif x[0:1] == 'T':
            self.c = 'TOOLS'
            self.graph_segment_id = 'None'
            self.graph_battery_id = 'None'
        elif x == 'BOX_INFO':
            self.c = x
            self.graph_segment_id = 'None'
            self.graph_battery_id = 'None'
        ##print("Welcome to "+self.c+" tab")
        y = 0
        try:
            if self.screen.ids.main.ids.window_controller.ids.side_w.i > self.screen.ids.graphv.ids.window_controller.ids.side_w.i:
                    self.screen.ids.graphv.ids.window_controller.ids.side_w.i = self.screen.ids.main.ids.window_controller.ids.side_w.i
            else:
                self.screen.ids.main.ids.window_controller.ids.side_w.i = self.screen.ids.graphv.ids.window_controller.ids.side_w.i
        except AttributeError:
            pass
        try:
            y = self.screen.ids.main.ids.window_controller.ids.side_w.i
        except AttributeError:
            pass
        try:
            y = self.screen.ids.graphv.ids.window_controller.ids.side_w.i
        except AttributeError:
            print('error')
        
        for i in range(0,y + 1):
            
            if ids_list[0][i] == self.c :
                if (self.c[0:1] == 'S') :
                    self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids[ids_list[0][i]].add_contents()
                    continue
                if self.c[0:1] == 'P':
                    self.screen.ids.graphv.ids.window_controller.ids.side_w.ids.tabs.ids[ids_list[0][i]].add_plot_settings(self.c)
                continue
            print(self.c[:6])
            
            if ids_list[0][i] == self.c[:6] :
                if (ids_list[0][i] == 'BOX_IN') :
                    self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids['BOX_INFO'].add_box_info()
                    continue
                continue

            try:
                if ids_list[0][i] == 'BOX_IN':
                    #print(ids_list)
                    self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids['BOX_INFO'].clear_widgets()
                    continue
                    
                if ids_list[0][i][0:1] == 'S':
                    self.screen.ids.main.ids.window_controller.ids.side_w.ids.tabs.ids[ids_list[0][i]].clear_widgets()
                
                    try:

                        
                        self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[ids_list[0][i][1:2]].ids[ids_list[0][i][4:6]].selection_color.rgba = [1,1,0,1]
                        self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[ids_list[0][i][1:2]].ids[ids_list[0][i][4:6]].selection_points.width = 3       
                        # #print("last")
                    except Exception as e:
                        #print(str(e)+"line 472 main")
                        #print(self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[int(ids_list[0][i][1:2])].ids[ids_list[0][i][4:6]])
                        break
                    
                if ids_list[0][i][0:1] == 'P':
                    #self.screen.ids.graphv.ids.window_controller.ids.side_w.ids.tabs.ids[ids_list[0][i]].clear_widgets()           
                    continue
            except KeyError:
                ##print(ids_list[0][i])
                for i in range(1,8):
                    for z in range(1,18):
                        if z == 18:
                            print("yes")
                        self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(i)].ids[str(z)].update_select_state(False)
                #print('No address on_switch')    

    def on_ref_press(self,instance_tabs,instance_tab_label,instance_tab,instance_tab_bar,instance_carousel,):
        self.selected = 1
        
        x = instance_tab.title[5:13]
        #print(x)
        if x[0:1] == 'S':
            a = bytearray(instance_tab.title[6:7], encoding='UTF-8')
            b = bytearray(instance_tab.title[9:11], encoding='UTF-8')
            b = b.decode('UTF-8')
            a = a.decode('UTF-8')    
            if not b.isnumeric():
                b = bytearray(instance_tab.title[9:10], encoding='UTF-8')
                b = b.decode('UTF-8')
                
            c = 'S'+a+'-'+'B'+b
        elif x[0:1] == 'P':
            a = bytearray(instance_tab.title[6:8], encoding='UTF-8')
            a = a.decode('UTF-8')    
            if not a.isnumeric():
                a= bytearray(instance_tab.title[6:7], encoding='UTF-8')
                a = a.decode('UTF-8')
            c = a
        elif x[0:1] == 'T':
            c = 'TOOLS'
            self.graph_segment_id = 'None'
            self.graph_battery_id = 'None'
        elif x[0:1] == 'B':
            c = x
        

        for instance_tab in instance_carousel.slides:
            if instance_tab.title == instance_tab_label.text:
                
                #print(ids_list)
                #print(c)
                x = np.where(ids_list== str(c))
                if c != 'BOX_INFO' and c != 'TOOLS' and c[0:1] != 'P':
                    #print(c)
                    try:
                        self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.self.segments.ids.grid.ids[a].ids[b].update_select_state(False)
                        #print("yo")
                    except AttributeError:
                        print("no")
                ids_list[x] = 'None'
                    
            
                #self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.self.segments.ids.grid.ids[instance_tab.title[1:2]].ids[instance_tab.title[4:6]].update_select_state(False)
                if c == 'BOX_INFO' and c == 'TOOLS' and c[0:1] == 'P':
                    return
                instance_tabs.remove_widget(instance_tab_label)
                break
    def side_window(self,caller_id):
        if caller_id == 'TOOLS':
            self.screen.ids.graphv.open_side_menu('TOOLS')
            return
        if caller_id[0:1] == 'P':
            self.screen.ids.graphv.open_side_menu(caller_id)
            return
        if caller_id == 'SD':
            self.send_command("read_sd")
            return
        self.screen.ids.main.open_side_menu(caller_id)
    def send_command(self,cmd):
        dict = {"Commands": {
            "read_sd": "False", 
            "command1": "False", 
            "command2": "False", 
            "command3": "False", 
            "command4": "False",
            "command5": "False"}
            }

        f = open(os.path.dirname(os.path.abspath("queue.json")),"r")
        commands = json.loads(f.read())
        f.close()
        dict["Commands"][cmd] = True
        commands.update(dict)
        f = open(os.path.dirname(os.path.abspath("queue.json")),"w")
        json.dump(commands, f)
        f.close()

    def minimize_sw(self,window):
        if window == 1:
            self.screen.ids.graphv.minimize()
            return
        self.screen.ids.main.minimize()
    def expand_sw(self,window):
        if window == 1:
            self.screen.ids.graphv.expand()
            return
        self.screen.ids.main.expand()       
    def close_sw(self,window):
        if window == 1:
            self.screen.ids.graphv.close()
            return
        self.screen.ids.main.close()
        for i in range(1,9):
            for z in range(1,19):
                if z == 18:
                    print("yes")
                self.screen.ids.main.ids.window_controller.ids.viewer.ids.box.ids.segments.ids.grid.ids[str(i)].ids[str(z)].update_select_state(False)

    def file_menu(self,menu_pos):
        self.x = menu_pos
        self.menu_open += 1
        if self.screen.current == 'main':
            if self.x==1:
                if self.menu_open == 1:
                    self.fm = FILE_MENU()
                    self.screen.ids.main.ids.floating.add_widget(self.fm)
                    self.screen.ids.main.ids.floating.ids['file'] = self.fm
                    
            if self.x==2:
                if self.menu_open == 1:
                    self.vm = VIEW_MENU()
                    self.screen.ids.main.ids.floating.add_widget(self.vm)
                    self.screen.ids.main.ids.floating.ids['view'] = self.vm

        if self.screen.current == 'graphv':    
            if self.x==1:
                
                if self.menu_open == 1:
                    self.fm = FILE_MENU()
                    self.screen.ids.graphv.ids.floating.add_widget(self.fm)
                    self.screen.ids.graphv.ids.floating.ids['file'] = self.fm
                    
            if self.x==2:
                if self.menu_open == 1:
                    self.vm = VIEW_MENU()
                    self.screen.ids.graphv.ids.floating.add_widget(self.vm)
    def switch_window(self):
        self.screen.switch_screen()
        self.menu_open = 0
        return 
    def make_plot(self):
        self.screen.ids.graphv.check_layout()
    def update(self,dt):
        # f = open(os.path.dirname(os.path.abspath("battery_data.json"))+"\\make_array\\battery_data.json","r")
        # try:
        #     self.data = json.loads(f.read())
            
        # except json.decoder.JSONDecodeError:
        #     pass

        y = serial_reader.get_data()
        if len(y) == 0:
            return
        else:
            json_string = y[0]  # Extract the string from the list
            try:
                self.data = json.loads(json_string) 
            except Exception as e:
                print("EEEERRRRRROOOORRRR"+json_string)
        if  self.data.get("Voltages") or self.data.get("Temperatures") or self.data.get("Humidities") or self.data.get("Balancing"):
            # print(self.data.get("Voltages"))
            update_battery_color(self)

        try:
            #self.screen.ids.graphv.grc.update_plot(self.data)
            pass
        except AttributeError:
            pass
        ##print(self.graph_segment_id)
        if 'BOX_IN' in ids_list:
           
                update_acc_data(self,self.data)
            
        if selected_tab == 1 and self.graph_segment_id != 'None' and self.graph_battery_id != 'None':
            
            update_tab(self,self.graph_segment_id,self.graph_battery_id)


        if self.plot == 1:
            self.screen.ids.graphv.grc.update_all_plots(self.data)
    def on_enter(instance, value):
       pass
       # #print('User pressed enter in', instance, value)
    def build(self):
        
        return self.screen
    


#Window.clearcolor=(.3,.3,.3,1)
if __name__== '__main__':
    serial_reader = sr()
    serial_reader.start()
    App().run()
   
#print("exit")