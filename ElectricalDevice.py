# By We Are Groot for PA raspberry pi competition 2023

from time import time


class ElectDevice:
    def __init__(self, device_no: int, no_of_modes: int, name: str, max_wattages: list,
                 min_wattages: list, csv_file, fixed=False):
        self.device_no = int(device_no)  # Unique id number for each device
        self.no_of_modes = int(no_of_modes)  # number of modes
        self.name = str(name)  # name of the device
        self.status = False  # whether the device is currently on or off
        self.max_wattages = list(max_wattages)  # the power usage of the device
        self.min_wattages = list(min_wattages)  # the power usage of the device
        self.accumulated_energy = 0  # the devices accumulated energy
        self.current_wattage = float(0.0)  # the current wattage of the device
        self.mode_on = 0  # the index of the mode which is on if the device is on
        self.csv_file = csv_file  # the csv file of the device
        self.significant_wattages = []  # a list of significant wattages (stored when power of device changes)
        self.significant_times = []  # significant times corresponding to significant wattages
        self.prev_significant_wattage = float(0)  # previous significant wattage
        self.lignite_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is lignite
        self.coal_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is coal
        self.oil_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is oil
        self.natural_gas_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is natural gas
        self.solar_pv_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is solar pv
        self.biomass_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is biomass
        self.nuclear_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is nuclear
        self.hydroelectric_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is hydroelectric
        self.wind_co2 = float(0)  # Co2 produced for accumulated energy if the energy source is lignite
        self.fixed = fixed  # whether or not the device is fixed (constantly on)

    def updateEmissions(self):
        self.lignite_co2 = float(self.accumulated_energy * 1.054)
        self.coal_co2 = float(self.accumulated_energy * 0.888)
        self.oil_co2 = float(self.accumulated_energy * 0.733)
        self.natural_gas_co2 = float(self.accumulated_energy * 0.499)
        self.solar_pv_co2 = float(self.accumulated_energy * 0.085)
        self.biomass_co2 = float(self.accumulated_energy * 0.045)
        self.nuclear_co2 = float(self.accumulated_energy * 0.029)
        self.hydroelectric_co2 = float(self.accumulated_energy * 0.026)
        self.wind_co2 = float(self.accumulated_energy * 0.026)

    def updateAccumulated(self, sample_period):
        if self.status:
            self.accumulated_energy += ((self.current_wattage * (sample_period / 3600)) / 1000)
        self.updateEmissions()

    def updateSignificantWattages(self):
        self.significant_wattages.append(self.prev_significant_wattage)
        self.significant_times.append(time())
        if self.prev_significant_wattage != self.current_wattage:
            self.significant_wattages.append(self.current_wattage)
            self.significant_times.append(time())
            self.prev_significant_wattage = self.current_wattage

    def changeWattage(self, new_wattage):
        self.current_wattage = new_wattage

    def changeIndexOfModeOn(self, new_mode_index):
        self.mode_on = int(new_mode_index)

    def changeStatusOff(self) -> None:
        self.status = False

    def changeStatusOn(self):
        self.status = True

    def writeToCsv(self):
        self.csv_file.writeDeviceWattage(self.current_wattage, self.accumulated_energy, self.lignite_co2, self.coal_co2,
                                         self.oil_co2, self.natural_gas_co2, self.solar_pv_co2, self.biomass_co2,
                                         self.nuclear_co2, self.hydroelectric_co2, self.wind_co2)

    def getStatusStr(self) -> str:
        if self.status:
            return "On"
        else:
            return "Off"

    def isInRangeIfOn(self, wattage_to_compare, index):
        if not self.status:
            if self.min_wattages[index] <= wattage_to_compare <= self.max_wattages[index]:
                return True
            else:
                return False
        elif self.status:
            if (self.min_wattages[index] - self.min_wattages[self.mode_on]) <= wattage_to_compare <= (self.max_wattages[index] - self.max_wattages[self.mode_on]):
                return True
            else:
                return False

    def isInRangeIfOff(self, wattage_to_compare, index):
        if self.status and not self.fixed:
            if self.min_wattages[index] <= wattage_to_compare <= self.max_wattages[index]:
                return True
            else:
                return False
        elif self.status and not self.fixed:
            if (self.min_wattages[self.mode_on] - self.min_wattages[index]) <= wattage_to_compare <= (self.max_wattages[self.mode_on] - self.max_wattages[index]):
                return True
            else:
                return False


class ElectDevList(list):
    def __init__(self, max_length: int):
        super().__init__()
        self.max_length = int(max_length)

    def addElectDev(self, device_no: int, no_of_modes: int, name: str, max_wattages: list,
                    min_wattages: list, csv_file):
        self.append(ElectDevice(device_no, no_of_modes, name, max_wattages, min_wattages, csv_file))

    def getDevsWhichAreOn(self) -> list:
        devices_on = []
        for dev in self:
            if dev.status:
                devices_on.append(dev.name)
        return devices_on

    def getIndexOfDevice(self, name) -> int:
        current_index = 0
        for current_device in self:
            if current_device.name == name:
                return current_index
            current_index += 1
        return False

    def removeElectDevice(self, index) -> None:
        self.pop(index)

    def printAllDevs(self):
        txt = "No:{dev_no}, Name:{n} State:{s}"
        for dev in self:
            print(txt.format(dev_no=dev.device_no, n=dev.name, s=dev.status))

    def updateAllDevsWattageLists(self):
        for current_device in self:
            current_device.updateSignificantWattages()

    def updateAllAccumulated(self, sample_period) -> None:
        for current_device in self:
            current_device.updateAccumulated(sample_period)

    def manageNearestMatchToSwitchOn(self, wattage_difference):  # take  in the significant wattage difference which needs to be investigated
        possible_devices = []  # the names of the devices which are on but the mode could be switched
        possible_device_mode_indexes = []  # the indexes of the modes which could be switched on the devices which are on
        for current_device in self:  # current device refers to the record of the current device being looked at
            for current_dev_mode in range(0, current_device.no_of_modes):  # current_dev_mode can be used as an index in the min_wattages and max_wattages list
                if current_device.isInRangeIfOn(wattage_difference, current_dev_mode):
                    # this if statement checks whether if a mode on a device which is already on is switched, would it fit the wattage increase
                    possible_devices.append(current_device)  # adds the name of the current device to the list of possible modes which could be switched
                    possible_device_mode_indexes.append(current_dev_mode)  # adds the index of the possible mode of this device to the possible modes of devices already on list
        if len(possible_devices) == 1:
            dev = possible_devices[0]
            dev.changeStatusOn()
            dev.changeIndexOfModeOn(possible_device_mode_indexes[0])
            dev.changeWattage(wattage_difference)
            dev.writeToCsv()
            self.updateAllDevsWattageLists()
            return dev.name, dev.status, dev.current_wattage, dev.accumulated_energy, True
        else:
            return False

    def manageNearestMatchToSwitchOff(self, wattage_difference):  # take  in the significant wattage difference which needs to be investigated
        possible_devices = []  # the names of the devices which are on but the mode could be switched
        possible_device_mode_indexes = []  # the indexes of the modes which could be switched on the devices which are on
        for current_device in self:  # current device refers to the record of the current device being looked at
            for current_dev_mode in range(0, current_device.no_of_modes):  # current_dev_mode can be used as an index in the min_wattages and max_wattages list
                if current_device.isInRangeIfOff(wattage_difference, current_dev_mode):
                    # this if statement checks whether if a mode on a device which is already on is switched, would it fit the wattage increase
                    possible_devices.append(current_device)  # adds the name of the current device to the list of possible modes which could be switched
                    possible_device_mode_indexes.append(current_dev_mode)  # adds the index of the possible mode of this device to the possible modes of devices already on list
        if len(possible_devices) == 1:  # checks whether a single possible device has been found which could fit the wattage difference
            dev = possible_devices[0]  # sets dev to this device which has been found
            dev.changeStatusOff()  # changes the devices status to off (False)
            dev.changeWattage(0)  # sets the devices wattage to 0 (as it will be off)
            dev.writeToCsv()  # writes this change in wattage to the device's CSV file
            self.updateAllDevsWattageLists()  # updates the wattage list used to plot the graph with this change
            return dev.name, dev.status, dev.current_wattage, dev.accumulated_energy, True  # returns information on the device which has found to have been switched off
        else:
            return False  # returns False if the program hasn't found a single possible device.

