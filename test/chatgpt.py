import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock

import matplotlib.pyplot as plt
import numpy as np


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        # Create the figure and axis objects
        self.fig, self.ax = plt.subplots()
        self.x_data = []
        self.y_data = []

        # Create the line object that will be updated
        self.line, = self.ax.plot(self.x_data, self.y_data)

        # Add the plot to the Kivy app
        self.plot = FigureCanvasKivyAgg(figure=self.fig)
        self.add_widget(self.plot)

        # Start the clock to update the plot
        Clock.schedule_interval(self.update_plot, 1.0 / 30.0)

    def update_plot(self, dt):
        # Generate new data for the plot
        x = np.arange(len(self.x_data), len(self.x_data) + 10)
        y = np.random.rand(10)

        # Add the new data to the plot
        self.x_data.extend(x)
        self.y_data.extend(y)
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)

        # Redraw the plot
        self.ax.relim()
        self.ax.autoscale_view()
        self.plot.draw()


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
