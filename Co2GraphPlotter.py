# By We Are Groot for PA raspberry pi competition 2023

import matplotlib.pyplot as plt
import time

class Co2Graph:  # creates the class "Co2GraphPlotter"
    def __init__(self, dev_name):
        self.dev_name = dev_name
        self.lignite = float(0.0)
        self.coal = float(0.0)
        self.oil = float(0.0)
        self.natural_gas = float(0.0)
        self.solar_pv = float(0.0)
        self.biomass = float(0.0)
        self.nuclear = float(0.0)
        self.hydroelectric = float(0.0)
        self.wind = float(0.0)
        self.CO2_text = (u'CO\u2082')
        self.source = ['brown coal (lignite)', 'coal', 'Oil', 'Natural Gas', 'Solar PV', 'Biomass', 'Nuclear', 'Hydroelectric', 'Wind']
        self.plotCo2Graph(12)
        

    def plotCo2Graph(self, energy):  # this function can be called inside the class to draw the graph
        self.lignite = float(energy * 1.054)  
        self.coal = float(energy * 0.888)
        self.oil = float(energy * 0.733)
        self.natural_gas = float(energy * 0.499)
        self.solar_pv = float(energy * 0.085)
        self.biomass = float(energy * 0.045)
        self.nuclear = float(energy * 0.029)
        self.hydroelectric = float(energy * 0.026)
        self.wind = float(energy * 0.026)
        emissions = [self.lignite, self.coal, self.oil, self.natural_gas, self.solar_pv, self.biomass, self.nuclear, self.hydroelectric, self.wind]
        a = plt.barh(self.source, emissions)
        plt.title(u'source of energy Vs CO\u2082 emissions for {dev_name}'.format(dev_name=self.dev_name))
        plt.ylabel('Source  of energy')
        plt.xlabel(u'CO\u2082 emissions/kg')
        plt.draw()
        plt.show(block=False)
        plt.style.use('ggplot')
        plt.pause(0.00001)
        
    
    def updateCo2Graph(self, energy):  # this clears and re-draws the origional graph to update it
        plt.clf()
        self.plotCo2Graph(energy)
        plt.pause(0.00001)

#  
