import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        
        self.plot = []
        self.fig = []
        self.ax = []
        self.labels = []
        print("in")
        self.fig, self.ax = plt.subplots()
        
        bar_width = 0.4
        for i in range(1, 146):
            self.labels.append("B"+str(i)) 



        bar1 = self.ax.bar(np.arange(144), 0, bar_width, color='g')
        bar2 = self.ax.bar(np.arange(144)+bar_width, 1, bar_width, color='r')
        bar3 = self.ax.bar(np.arange(144)+(2*bar_width), 2, bar_width, color='b')
        
        self.plot = FigureCanvasKivyAgg(figure=self.fig)
        self.add_widget(self.plot)
        print(self.ids)

        
        self.ax.relim()
        self.ax.autoscale_view()
        self.plot.draw()

        print("done")

class MyApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == '__main__':
    MyApp().run()
