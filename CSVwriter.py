import time
from time import time
from ElectricalDevice import ElectDevList


class CsvWriter:
    def __init__(self, file_name: str):
        self.file_name = file_name
        data_file = open(file_name, "w")
        data_file.close()

    def writeString(self, s: str, quoted: bool = True):
        data_file = open(self.file_name, "a")
        if quoted:
            data_file.write('\"' + str(s) + '\"')
        else:
            data_file.write(s)

    def writeNumber(self, number: int):
        data_file = open(self.file_name, "a")
        data_file.write(str(number))

    def writeNumber(self, number: float):
        data_file = open(self.file_name, "a")
        data_file.write(str(number))

    def writeComma(self):
        data_file = open(self.file_name, "a")
        data_file.write(",")

    def writeEndOfLine(self):
        data_file = open(self.file_name, "a")
        data_file.write('\n')


class CsvEventLogger(CsvWriter):
    def __init__(self, file_name: str, start_time: float):
        super().__init__(file_name)
        data_file = open(file_name, "w")
        data_file.close()
        self.file_name = file_name
        self.start_time = start_time
        self.writeColHeaders()

    def writeColHeaders(self):
        self.writeString("Time")
        self.writeComma()
        self.writeString("Dev name")
        self.writeComma()
        self.writeString("Power")
        self.writeComma()
        self.writeString("Status")
        self.writeComma()
        self.writeString("Accumulated energy")
        self.writeEndOfLine()

    def writeRow(self, dev_name: str, dev_status: bool, power: float, accumulated_energy: float):
        self.writeNumber(float(time())-self.start_time)
        self.writeComma()
        self.writeString(dev_name)
        self.writeComma()
        self.writeNumber(power)
        self.writeComma()
        if dev_status:
            self.writeString("On")
        else:
            self.writeString("Off")
        self.writeComma()
        self.writeNumber(accumulated_energy)
        self.writeEndOfLine()


class CsvWriteAllDevData(CsvWriter, ElectDevList):
    def __init__(self, file_name: str, start_time: float):
        super().__init__(file_name)
        self.file_name = file_name
        data_file = open(file_name, "w")
        data_file.close()
        self.start_time = start_time
        self.addHeaders()

    def addHeaders(self):
        self.writeString("Device Number")
        self.writeComma()
        self.writeString("Device Name")
        self.writeComma()
        self.writeString("Status")
        self.writeComma()
        self.writeString("Min wattage")
        self.writeComma()
        self.writeString("Max wattage")
        self.writeComma()
        self.writeString("Current power")
        self.writeComma()
        self.writeString("Accumulated energy")
        self.writeEndOfLine()

    def writeDevData(self):
        for current_device in self:
            self.writeNumber(current_device.device_no)
            self.writeComma()
            self.writeString(current_device.name)
            self.writeComma()
            if current_device.status:
                self.writeString("On")
            else:
                self.writeString("Off")
            self.writeComma()
            self.writeNumber(current_device.min_wattages)
            self.writeComma()
            self.writeNumber(current_device.max_wattages)
            self.writeComma()
            self.writeNumber(current_device.current_wattage)
            self.writeComma()
            self.writeNumber(current_device.accumulated_energy)
            self.writeEndOfLine()


class graphPlottingFile(CsvWriter, ElectDevList):
    def __init__(self, file_name: str, start_time: float):
        super().__init__(file_name)
        self.file_name = file_name
        data_file = open(file_name, "w")
        data_file.close()
        self.start_time = start_time
        self.addHeaders()

    def addHeaders(self):
        self.writeString("Time")
        for current_device in self:
            self.writeComma()
            self.writeString(current_device.name)
        self.writeEndOfLine()

    def writeAllPowers(self):
        f = open(self.file_name, "r")
        headers = f.read()[0]
        index_counter = 1
        for current_device in self:
            if current_device.name == headers[index_counter]:
                continue
            else:
                self.addHeaders()
        self.writeNumber(float(time())-self.start_time)
        for current_device in self:
            self.writeComma()
            self.writeNumber(current_device.current_wattage)
        self.writeEndOfLine()


class SingleWattageGraphFile(CsvWriter):
    def __init__(self, file_name: str, dev_name: str, start_time: float):
        super().__init__(file_name)
        self.file_name = file_name
        data_file = open(file_name, "w")
        data_file.close()
        self.start_time = start_time
        self.prev_wattage = float(0)
        self.writeHeaders(dev_name)
        self.all_wattages_list = []
        self.times_list = []

    def writeTotalPowerW(self, wattage, accumulated, lignite_co2, coal_co2, oil_co2, natural_gas_co2, solar_pv_co2, biomass_co2, nuclear_co2, hydroelectric_co2, wind_co2):
        time_now = time()
        self.writeNumber(float(time_now)-self.start_time)
        self.writeComma()
        self.writeNumber(self.prev_wattage)
        self.writeComma()
        self.writeNumber(accumulated)
        self.writeComma()
        self.writeNumber(lignite_co2)
        self.writeComma()
        self.writeNumber(coal_co2)
        self.writeComma()
        self.writeNumber(oil_co2)
        self.writeComma()
        self.writeNumber(natural_gas_co2)
        self.writeComma()
        self.writeNumber(solar_pv_co2)
        self.writeComma()
        self.writeNumber(biomass_co2)
        self.writeComma()
        self.writeNumber(nuclear_co2)
        self.writeComma()
        self.writeNumber(hydroelectric_co2)
        self.writeComma()
        self.writeNumber(wind_co2)
        self.writeEndOfLine()  # this line is written so that the data can be put into a graph which goes straight up/ down.
        self.times_list.append(time)
        self.prev_wattage = wattage
        self.all_wattages_list.append(self.prev_wattage)
        self.writeNumber(float(time_now)-self.start_time)
        self.writeComma()
        self.writeNumber(wattage)
        self.writeComma()
        self.writeNumber(accumulated)
        self.writeComma()
        self.writeNumber(lignite_co2)
        self.writeComma()
        self.writeNumber(coal_co2)
        self.writeComma()
        self.writeNumber(oil_co2)
        self.writeComma()
        self.writeNumber(natural_gas_co2)
        self.writeComma()
        self.writeNumber(solar_pv_co2)
        self.writeComma()
        self.writeNumber(biomass_co2)
        self.writeComma()
        self.writeNumber(nuclear_co2)
        self.writeComma()
        self.writeNumber(hydroelectric_co2)
        self.writeComma()
        self.writeNumber(wind_co2)
        self.writeEndOfLine()
        self.times_list.append(time)
        self.prev_wattage = wattage
        self.all_wattages_list.append(wattage)

    def writeHeaders(self, dev_name):
        self.writeString("Time")
        self.writeComma()
        self.writeString(str(dev_name)+" wattage")
        self.writeComma()
        self.writeString("Accumulated")
        self.writeComma()
        self.writeString("Lignite CO2")
        self.writeComma()
        self.writeString("Coal CO2")
        self.writeComma()
        self.writeString("Oil CO2")
        self.writeComma()
        self.writeString("Natural Gas CO2")
        self.writeComma()
        self.writeString("Solar PV CO2")
        self.writeComma()
        self.writeString("Biomass CO2")
        self.writeComma()
        self.writeString("Nuclear CO2")
        self.writeComma()
        self.writeString("Hydroelectric CO2")
        self.writeComma()
        self.writeString("Wind CO2")
        # self.writeComma()
        # self.writeString("Accumulated (kWh)")
        # self.writeComma()
        # self.writeString("Lignite CO2")
        self.writeEndOfLine()

    def writeDeviceWattage(self, wattage, status, accumulated, lignite_co2, coal_co2, oil_co2, natural_gas_co2, solar_pv_co2, biomass_co2, nuclear_co2, hydroelectric_co2, wind_co2):
        time_now = time()
        self.writeNumber(float(time_now)-self.start_time)
        self.writeComma()
        self.writeNumber(self.prev_wattage)
        self.writeComma()
        if status == True:
            self.writeString("on")
        else:
            self.writeString("off")
        self.writeComma()
        self.writeNumber(accumulated)
        self.writeComma()
        self.writeNumber(lignite_co2)
        self.writeComma()
        self.writeNumber(coal_co2)
        self.writeComma()
        self.writeNumber(oil_co2)
        self.writeComma()
        self.writeNumber(natural_gas_co2)
        self.writeComma()
        self.writeNumber(solar_pv_co2)
        self.writeComma()
        self.writeNumber(biomass_co2)
        self.writeComma()
        self.writeNumber(nuclear_co2)
        self.writeComma()
        self.writeNumber(hydroelectric_co2)
        self.writeComma()
        self.writeNumber(wind_co2)
        self.writeEndOfLine()
        self.writeEndOfLine()  # this line is written so that the data can be put into a graph which goes straight up/ down.
        self.times_list.append(time)
        self.prev_wattage = wattage
        self.all_wattages_list.append(self.prev_wattage)
        self.writeNumber(float(time_now)-self.start_time)
        self.writeComma()
        self.writeNumber(wattage)
        self.writeComma()
        if status == True:
            self.writeString("on")
        else:
            self.writeString("off")
        self.writeComma()
        self.writeNumber(accumulated)
        self.writeComma()
        self.writeNumber(lignite_co2)
        self.writeComma()
        self.writeNumber(coal_co2)
        self.writeComma()
        self.writeNumber(oil_co2)
        self.writeComma()
        self.writeNumber(natural_gas_co2)
        self.writeComma()
        self.writeNumber(solar_pv_co2)
        self.writeComma()
        self.writeNumber(biomass_co2)
        self.writeComma()
        self.writeNumber(nuclear_co2)
        self.writeComma()
        self.writeNumber(hydroelectric_co2)
        self.writeComma()
        self.writeNumber(wind_co2)
        self.writeEndOfLine()
        self.prev_wattage = wattage
        self.times_list.append(time)
        self.prev_wattage = wattage
        self.all_wattages_list.append(wattage)
"""
a = SingleWattageGraphFile("test2.csv", "a", time())
a.writeDeviceWattage(23)
a.writeDeviceWattage(18)
a.writeDeviceWattage(27)
"""