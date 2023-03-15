# By We Are Groot for PA raspberry pi competition 2023

from time import time

def info_from(info_list):
    length_of_info = len(info_list)
    return info_list[0:length_of_info]


class ElectDevice:
    def __init__(self, device_no: int, no_of_modes: int, name: str, status: bool, max_wattages: list,
                 min_wattages: list, csv_file, fixed=False):
        self.device_no = int(device_no)  # Unique id number for each device
        self.no_of_modes = int(no_of_modes)  # number of modes
        self.name = str(name)  # name of the device
        self.status = bool(status)  # whether the device is currently on or off
        self.max_wattages = list(max_wattages)  # the power usage of the device
        self.min_wattages = list(min_wattages)  # the power usage of the device
        self.accumulated_energy = 0
        self.current_wattage = float(0.0)
        self.mode_on = 0
        self.csv_file = csv_file
        self.significant_wattages = []
        self.significant_times = []
        self.prev_significant_wattage = float(0)
        self.lignite_co2 = float(0)
        self.coal_co2 = float(0)
        self.oil_co2 = float(0)
        self.natural_gas_co2 = float(0)
        self.solar_pv_co2 = float(0)
        self.biomass_co2 = float(0)
        self.nuclear_co2 = float(0)
        self.hydroelectric_co2 = float(0)
        self.wind_co2 = float(0)
        self.fixed = fixed
        
    def updateEmmissions(self):
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
        self.updateEmmissions()
        
    def updateSignificantWattagesWithChange(self):
        self.significant_wattages.append(self.prev_significant_wattage)
        self.significant_times.append(time())
        self.significant_wattages.append(self.current_wattage)
        self.significant_times.append(time())
        self.prev_significant_wattage = self.current_wattage
        
    def updateSignificantWattagesNoChange(self):
        self.significant_wattages.append(self.prev_significant_wattage)
        self.significant_times.append(time())
        
    def changeWattage(self, new_wattage):
        self.current_wattage = new_wattage
        
    def changeIndexOfModeOn(self, new_mode_index):
        self.mode_on = int(new_mode_index)
        
    def changeStatusOff(self) -> None:
        self.status = False
        
    def changeStatusOn(self):
        self.status = True
        
    def writeToCsv(self):
        self.csv_file.writeDeviceWattage(self.current_wattage, self.status, self.accumulated_energy, self.lignite_co2, self.coal_co2, self.oil_co2, self.natural_gas_co2,self.solar_pv_co2, self.biomass_co2, self.nuclear_co2, self.hydroelectric_co2, self.wind_co2)

    def getStatusStr(self) -> str:
        if self.status:
            return "On"
        else:
            return "Off"

    def isInRangeIfOn(self, wattage_to_compare, index):
        if not self.status and not self.fixed:
            if self.min_wattages[index] <= wattage_to_compare <= self.max_wattages[index]:
                return True
            else:
                return False
        elif self.status and not self.fixed:
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

    def addElectDev(self, device_no: int, no_of_modes: int, name: str, status: bool, max_wattages: list,
                    min_wattages: list, csv_file):
        self.append(ElectDevice(device_no, no_of_modes, name, status, max_wattages, min_wattages, csv_file))

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

    def removeElectDevice(self, index) -> None:
        self.pop(index)

    def printAllDevs(self):
        txt = "No:{dev_no}, Name:{n} State:{s}"
        for dev in self:
            print(txt.format(dev_no=dev.device_no, n=dev.name, s=dev.status))
            
    def updateAllDevsWattageLists(self, dev_changed, wattage_change):
        for current_device in self:
            if dev_changed == current_device:
                current_device.updateSignificantWattagesWithChange()
            else:
                current_device.updateSignificantWattagesNoChange()

    def updateAllAccumulated(self, sample_period) -> None:
        for current_device in self:
            current_device.updateAccumulated(sample_period)
            
    def manageNearestMatchToSwitchOn(self, wattage_difference):  # done???
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
            self.updateAllDevsWattageLists(dev, wattage_difference)
            return dev.name, dev.status, dev.current_wattage, dev.accumulated_energy, True
        else:
            return False

    def manageNearestMatchToSwitchOff(self, wattage_difference):  # edit this to fit off
        possible_devices = []  # the names of the devices which are on but the mode could be switched
        possible_device_mode_indexes = []  # the indexes of the modes which could be switched on the devices which are on
        for current_device in self:  # current device refers to the record of the current device being looked at
            for current_dev_mode in range(0, current_device.no_of_modes):  # current_dev_mode can be used as an index in the min_wattages and max_wattages list
                if current_device.isInRangeIfOff(wattage_difference, current_dev_mode):
                    # this if statement checks whether if a mode on a device which is already on is switched, would it fit the wattage increase
                    possible_devices.append(current_device)  # adds the name of the current device to the list of possible modes which could be switched
                    possible_device_mode_indexes.append(current_dev_mode)  # adds the index of the possible mode of this device to the possible modes of devices already on list
        if len(possible_devices) == 1:
            dev = possible_devices[0]
            dev.changeStatusOff()
            dev.changeWattage(0)  # wattage_difference
            dev.writeToCsv()
            self.updateAllDevsWattageLists(dev, wattage_difference)
            return dev.name, dev.status, dev.current_wattage, dev.accumulated_energy, True
        else:
            return False
