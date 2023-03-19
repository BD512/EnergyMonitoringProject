# By We Are Groot for PA raspberry pi competition 2023

import datetime
import time
from GlobalVariables import *
from CSVwriter import CsvEventLogger, SingleWattageCsvFile
from Co2GraphPlotter import *
from PowerGraphPlotter import *

# make use of CsvWriteAllDevData, GraphPlottingFile
# make each devices co2 be shown


class TheApp:

    def __init__(self):
        self.initial_start_time = float(0.0)
        self.sampling_period = float(0.05)  # in seconds
        self.next_app_sample_time = float(0)
        self.next_display_time = float(0)
        self.display_update_period = float(0.1)
        self.app_run_duration = float(360)  # in seconds
        self.prev_power_reading = float(0)
        self.latest_power_reading = float(0)
        self.total_accumulated_energy_kwh = float(0)
        self.wattage_difference = float(0)
        self.skipped_transition = bool(False)
        self.prev_wattage_for_transition_calc = float(0)
        self.count_transition_check = int(0)
        self.change_detected = bool(False)
        self.ready = bool(False)
        self.devices_logger = None
        self.devices_list_file = None
        self.total_wattage_csv = None
        self.graph_type = str()
        self.graph = None
        self.graph_update_period = float(1.0)
        self.next_update_co2_graph = float(0)
        self.next_update_wattages_graph = True
        self.wattages = list()
        self.times = list()
        self.prev_change_wattage = float(0)

    def getTotalCo2(self):
        return [float(self.total_accumulated_energy_kwh * 1.054), float(self.total_accumulated_energy_kwh * 0.888),
                float(self.total_accumulated_energy_kwh * 0.733), float(self.total_accumulated_energy_kwh * 0.499),
                float(self.total_accumulated_energy_kwh * 0.085), float(self.total_accumulated_energy_kwh * 0.045),
                float(self.total_accumulated_energy_kwh * 0.029), float(self.total_accumulated_energy_kwh * 0.026),
                float(self.total_accumulated_energy_kwh * 0.026)]

    def initaliseGraph(self):
        if self.graph_type == "a":
            graph = OneDevWattageGraph("total")
        elif self.graph_type == "b":
            graph = Co2Graph("total")
        elif self.graph_type == "c":
            graph = AllDevsWattageGraph(elect_dev_list, "all devices")
        else:
            graph = None
        return graph

    def updateGraph(self):
        if self.graph is not None and self.graph_type == "a":
            self.graph.updateGraph(self.wattages, self.times)
        elif self.graph is not None and self.graph_type == "b":
            self.graph.updateCo2Graph(self.total_accumulated_energy_kwh)
        elif self.graph is not None and self.graph_type == "c":
            self.graph.updateGraph()

    def initialiseElectDevList(self):  # device names must be individual!  # make more exact
        elect_dev_list.addElectDev(device_no=0, no_of_modes=1, name="25W bulb", max_wattages=[28],
                                   min_wattages=[18], csv_file=self.createCsvFiles("25W bulb")[1]),
        elect_dev_list.addElectDev(device_no=1, no_of_modes=1, name="60W bulb", max_wattages=[65],
                                   min_wattages=[55], csv_file=self.createCsvFiles("60W bulb")[1]),
        elect_dev_list.addElectDev(device_no=2, no_of_modes=1, name="100W Bulb", max_wattages=[110],
                                   min_wattages=[93],
                                   csv_file=self.createCsvFiles("100W Bulb")[1]),
        elect_dev_list.addElectDev(device_no=3, no_of_modes=1, name="40W Bulb", max_wattages=[50],
                                   min_wattages=[35],
                                   csv_file=self.createCsvFiles("40W Bulb")[1])

    def createCsvFiles(self, dev_name):
        dev_name.strip()
        today = datetime.date.today()

        file_name = "{dev_name}{date}{time}.csv".format(dev_name=dev_name, date=today, time=round(time.time()))
        file = SingleWattageCsvFile(file_name, dev_name, self.initial_start_time)
        return file_name, file

    def createCsvFileName(self, name):
        name.strip()
        today = datetime.date.today()
        file_name = "{dev_name}{date}{time}.csv".format(dev_name=name, date=today, time=round(time.time()))
        return file_name

    def showUpdates(self, name, status, wattage, accumulated):
        self.devices_logger.writeRow(name, status, wattage, accumulated)
        if status:
            display_status = "on"
        else:
            display_status = "off"
        print("Dev name:{name}, Status:{status}, Wattage:{wattage}, Accumulated(kWh):{kWh}".format(
            name=name, status=display_status, wattage=wattage,
            kWh=accumulated))

    def getAppRunTime(self) -> float:
        return time.time() - self.initial_start_time

    def accumulateTotalEnergy(self):
        average_slot_power_w = (self.prev_power_reading + self.latest_power_reading) / 2.0
        slot_energy_kwh = average_slot_power_w * self.sampling_period / (3600.0 * 1000.0)
        self.total_accumulated_energy_kwh += slot_energy_kwh

    def displayReadings(self):
        txt = "Current power {power:.2f}W Energy {energy:.4f}kWh"
        print(txt.format(power=self.latest_power_reading, energy=self.total_accumulated_energy_kwh))

    def updateWattagesList(self):
        time_now = time.time()
        power_now = owen_meter.getWattage()
        self.wattages.append(self.prev_change_wattage)
        self.times.append(time_now)
        self.wattages.append(power_now)
        self.times.append(time_now)
        self.prev_change_wattage = power_now

    def run(self) -> bool:
        print("Please switch all devices off")
        self.graph_type = input(
            "Would you like a graph of the total energy usage over time to be printed or the amount of CO2 produced? For total energy usage type \"a\" OR for the CO2 graph type \"b\" OR for a graph showing individual devices, \"c\" OR for no graph type \"d\"(the processing is quicker so more accurate without showing a real time graaph - the data can still be viewed in the CSV files afterwards:").lower()
        self.graph = self.initaliseGraph()
        self.latest_power_reading = owen_meter.getWattage()
        self.prev_power_reading = self.latest_power_reading
        self.initial_start_time = time.time()
        self.initialiseElectDevList()
        self.devices_logger = CsvEventLogger(self.createCsvFileName("devs_log"), time.time())
        self.total_wattage_csv = SingleWattageCsvFile(self.createCsvFileName("total"), "Total", time.time())
        while True:
            app_run_time = self.getAppRunTime()
            if app_run_time >= self.app_run_duration:
                return True  # Finished ok
            if app_run_time >= self.next_app_sample_time:
                self.latest_power_reading = owen_meter.getWattage()
                self.wattage_difference = self.latest_power_reading - self.prev_power_reading
                if self.wattage_difference < 0 and self.wattage_difference * -1 > (
                        self.prev_power_reading + 0.01) * 0.05 and not adding:
                    if self.ready:
                        # print("Lower")
                        self.total_wattage_csv.writeTotalPowerW(owen_meter.getWattage(), self.total_accumulated_energy_kwh, self.getTotalCo2()[0], self.getTotalCo2()[1], self.getTotalCo2()[2], self.getTotalCo2()[3], self.getTotalCo2()[4], self.getTotalCo2()[5], self.getTotalCo2()[6], self.getTotalCo2()[7], self.getTotalCo2()[8])
                        self.updateWattagesList()
                        new_dev_info = elect_dev_list.manageNearestMatchToSwitchOff(self.wattage_difference * -1)
                        if not new_dev_info:
                            pass
                            # print("No devs fit")
                        else:
                            self.skipped_transition = False
                            self.showUpdates(new_dev_info[0], new_dev_info[1], new_dev_info[2], new_dev_info[3])
                            self.prev_power_reading = self.latest_power_reading
                            self.next_update_wattages_graph = True
                        self.ready = False
                    else:
                        if round(self.latest_power_reading) == round(
                                self.prev_wattage_for_transition_calc) and self.count_transition_check == 2:
                            self.prev_wattage_for_transition_calc = 0
                            self.ready = True
                            self.count_transition_check = 0
                        elif round(self.latest_power_reading) == round(self.prev_wattage_for_transition_calc):
                            self.count_transition_check += 1
                            self.prev_wattage_for_transition_calc = self.latest_power_reading
                        else:
                            self.count_transition_check = 0
                            self.prev_wattage_for_transition_calc = self.latest_power_reading
                elif self.wattage_difference > 0 and self.wattage_difference > (
                        self.prev_power_reading + 0.1) * 0.05 and not adding:
                    if self.ready:
                        self.total_wattage_csv.writeTotalPowerW(owen_meter.getWattage(), self.total_accumulated_energy_kwh, self.getTotalCo2()[0], self.getTotalCo2()[1], self.getTotalCo2()[2], self.getTotalCo2()[3], self.getTotalCo2()[4], self.getTotalCo2()[5], self.getTotalCo2()[6], self.getTotalCo2()[7], self.getTotalCo2()[8])
                        self.updateWattagesList()
                        new_dev_info = elect_dev_list.manageNearestMatchToSwitchOn(self.wattage_difference)
                        self.wattage_difference = self.latest_power_reading - self.prev_power_reading
                        if not new_dev_info:
                            pass
                            # print("No devs fit")
                        else:
                            self.skipped_transition = False
                            self.showUpdates(new_dev_info[0], new_dev_info[1], new_dev_info[2], new_dev_info[3])
                            self.prev_power_reading = self.latest_power_reading
                            self.next_update_wattages_graph = True
                        self.ready = False
                    else:
                        if round(self.latest_power_reading) == round(
                                self.prev_wattage_for_transition_calc) and self.count_transition_check == 2:
                            self.prev_wattage_for_transition_calc = 0
                            self.ready = True
                            self.count_transition_check = 0
                        elif round(self.latest_power_reading) == round(self.prev_wattage_for_transition_calc):
                            self.count_transition_check += 1
                            self.prev_wattage_for_transition_calc = self.latest_power_reading
                        else:
                            self.count_transition_check = 0
                            self.prev_wattage_for_transition_calc = self.latest_power_reading

                else:
                    self.prev_power_reading = self.latest_power_reading
                elect_dev_list.updateAllAccumulated(self.sampling_period)
                self.accumulateTotalEnergy()
                self.devices_list_file.writeDevData()
                # self.latest_power_reading = owen_meter.getWattage()
                # self.accumulateTotalEnergy()
                # self.next_app_sample_time += self.sampling_period
            if app_run_time >= self.next_update_co2_graph and not self.change_detected and self.graph_type == "b":
                # only updates when no change to keep up speed of data
                self.updateGraph()
                self.next_update_co2_graph += self.graph_update_period
            elif self.next_update_wattages_graph and (self.graph_type == "a" or self.graph_type == "c"):
                self.updateGraph()
                self.next_update_wattages_graph = False

            time.sleep(0.01)


the_app = TheApp()  # Create the App
the_app.run()  # Run the app

# initialiseElectDevList()
