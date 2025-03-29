import matplotlib.pyplot as plt
from kivy.app import App
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.clock import Clock
from matplotlib.backend_bases import MouseEvent
import random as r
from kivy.properties import NumericProperty, ObjectProperty, ListProperty

class GraphApp(App):
    time = NumericProperty(0)
    value = ObjectProperty(0)
    x = ListProperty([0])
    y = ListProperty([0])
    def build(self):
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

        
        Clock.schedule_interval(self.update, 1)
        return self.plot

    def update(self, dt):
        # Generate some random data for the plot
        self.time = self.time+1
        self.value = self.value+r.randint(-5,5)
        self.x.append(self.time)
        self.y.append(self.value)
        print(self.x)
        self.line.set_data(self.x, self.y)
        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        self.plot.draw()

    def hover(self, event: MouseEvent):
        if event.inaxes == self.ax:
            x, y = event.xdata, event.ydata
            self.tooltip.set_text("x={:.2f}, y={:.2f}".format(x, y))
            self.tooltip.xy = x, y
            self.tooltip.set_visible(True)
            self.plot.draw()
        else:
            self.tooltip.set_visible(False)

if __name__ == '__main__':
    GraphApp().run()