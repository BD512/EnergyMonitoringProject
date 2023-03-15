import matplotlib.pyplot as plt
from ElectricalDevice import ElectDevList
import numpy as np
import sys

class OneDevWattageGraph:
    def __init__(self, dev_name):
        self.dev_name = dev_name
        
    def plotGraph(self, wattages, times):
        x_times = np.array(times)
        y_wattages = np.array(wattages)
        plt.plot(x_times, y_wattages)
        plt.title(u'{dev_name} power usage of'.format(dev_name=self.dev_name))
        plt.ylabel('Power usage/W')
        plt.xlabel(u'Time')
        plt.draw()
        plt.show(block=False)
        plt.pause(0.00001)
        #  plt.savefig(sys.stdout.buffer)
        #  sys.stdout.flush()
    
    def updateGraph(self, wattages, times):
        plt.clf()
        self.plotGraph(wattages, times)
        

class AllDevsWattageGraph():
    def __init__(self, elect_devs, dev_name="all devs"):
        self.elect_devs = elect_devs
        self.dev_name = dev_name
        
    def plotGraph(self):
        for current_device in self.elect_devs:
            x_times = np.array(list(current_device.significant_times))
            y_wattages = np.array(list(current_device.significant_wattages))
            plt.plot(x_times, y_wattages, label=current_device.name)
            plt.legend(loc="upper left")
        plt.title(u'{dev_name} power usage'.format(dev_name=self.dev_name))
        plt.ylabel('Power usage/W')
        plt.xlabel(u'Time')
        plt.draw()
        plt.show(block=False)
        plt.pause(0.00001)
    
    def updateGraph(self):
        plt.clf()
        self.plotGraph()