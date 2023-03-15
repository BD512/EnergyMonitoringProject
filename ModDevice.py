# works


import struct
from ModbusByOrgTechLtd import Modbus


class OwenMeter(Modbus):
    def __init__(self, slave_id):
        super().__init__(slave_id)  # this shares the variable slave_id with Modbus
        self.slave_id = slave_id  # slave_id refers to the id of the owen module
        # self.serial = serial.Serial ("COM3", 9600)

    def getVoltage(self) -> float:
        results = self.readInputRegisters2(starting_address=0x10, quantity=4)
        status = results[0]  # bool
        data = results[1]  # list
        voltage = self.getFloat(data)
        return self.to2DecimalPlaces(voltage)  # float

    def getFrequency(self) -> float:
        results = self.readInputRegisters2(starting_address=0x4E, quantity=4)
        status = results[0]
        data = results[1]
        frequency = self.getFloat(data)
        return self.to2DecimalPlaces(frequency)

    def getCurrent(self) -> float:  # amps
        results = self.readInputRegisters2(starting_address=0x52, quantity=4)
        status = results[0]
        data = results[1]
        current = self.getFloat(data)
        return self.to2DecimalPlaces(current)

    def getKilowattHours(self) -> float:  # kilowatt hours
        results = self.readInputRegisters2(starting_address=0x0800, quantity=4)
        status = results[0]
        data = results[1]
        Kilowatts = self.getFloat(data)
        return Kilowatts

    def getPowerFactor(self) -> float:
        results = self.readInputRegisters2(starting_address=0x152, quantity=4)
        status = results[0]
        data = results[1]
        power_factor = self.getFloat(data)
        return self.to2DecimalPlaces(power_factor)

    def getTotalActiveEnergy(self) -> float:
        results = self.readInputRegisters2(starting_address=0x0618, quantity=4)
        status = results[0]
        data = results[1]
        total_active_energy = self.getFloat(data)
        return total_active_energy

    def getWattage(self) -> float:  # Watts
        results = self.readInputRegisters2(starting_address=0x92, quantity=4)
        status = results[0]
        data = results[1]
        wattage = self.getFloat(data)
        return self.to2DecimalPlaces(wattage)

    def getFloat(self, data) -> float:
        data_bytes = bytearray([(data[0] & 0xFF00) >> 8, data[0] & 0xFF, (data[1] & 0xFF00) >> 8, data[1] & 0xFF])
        val = struct.unpack('>f', data_bytes)  # big endian
        return val[0]

    def to2DecimalPlaces(self, val):
        return round(val, 2)