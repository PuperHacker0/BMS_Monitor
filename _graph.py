import matplotlib.pyplot as plt
from backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.style as mplstyle
from matplotlib.backend_bases import MouseEvent
from kivy.uix.widget import Widget
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty
from kivy.clock import Clock
class GRAPH_OBJ(BoxLayout):
    time = ObjectProperty(0)
    value = ObjectProperty(0.0)
    hor = ListProperty([0])
    ver = ListProperty([0.0])

    def test(self):
        # initializing the data
        x = [10, 20, 30, 40]
        y = [20, 30, 40, 50]
        
        # plotting the data
        plt.plot(x, y)
        
        # Adding the title
        plt.title("Simple Plot")
        
        # Adding the labels
        plt.ylabel("y-axis")
        plt.xlabel("x-axis")
        self.graph = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(self.graph)
        
    def set_values(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], label='Line Plot')
        self.plot = FigureCanvasKivyAgg(self.fig)
        self.tooltip = self.ax.annotate("", xy=(0,0), xytext=(0,20), textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w"),
                                    arrowprops=dict(arrowstyle="->"))
        self.tooltip.set_visible(False)
        self.ax.legend(loc='upper left')
        self.ax.grid(True)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('My Graph')
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)
        Clock.schedule_once(self.update_now)
        return self.plot
    def update_now(self,dt):
        # Generate some random data for the plot

        self.time = self.time+1
        self.hor.append(self.time)
        self.ver.append(self.value)
       
        self.line.set_data(self.hor, self.ver)
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        self.plot.draw()

    def update(self,volt):
        # Generate some random data for the plot
        self.time = self.time+1
        
        self.value = volt
        
        self.hor.append(self.time)
       
        self.ver.append(self.value)
        self.line.set_data(self.hor, self.ver)
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        self.plot.draw()

    def hover(self, event: MouseEvent):
        if event.inaxes == self.ax:
            hover_x, hover_y = event.xdata, event.ydata
            self.tooltip.set_text("x={:.2f}, y={:.2f}".format(hover_x, hover_y))
            self.tooltip.xy = hover_x, hover_y
            self.tooltip.set_visible(True)
            self.canvas.draw()
        else:
            self.tooltip.set_visible(False)
         
def blif_test(self):
    self.x = np.linspace(0,50., num=100)
    self.fig = plt.figure()
    ax2 = self.fig.add_subplot(2, 1, 2)
    line, = ax2.plot([], lw=3)
    text = ax2.text(0.8,0.5, "")
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim([-1.1, 1.1])
    self.fig.canvas.draw()
    ax2background = self.fig.canvas.copy_from_bbox(ax2.bbox)
    plt.show(block=False)

    k=0.
    for i in np.arange(1000):
        
        line.set_data(self.x, np.sin(self.x/3.+k))

        #print tx
    k+=0.11

    self.fig.canvas.restore_region(ax2background)
    ax2.draw_artist(line)
    self.fig.canvas.blit(ax2.bbox)
    self.fig.canvas.flush_events()