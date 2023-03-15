###########################################################
#
# File: ModbusByOrgTechLtd.py
#   Modbus data comms driver
#   Provided by Organised Technology Ltd
#
# Authors:
#   Based on examples found in the umodbus RTU documentation.
#   Adapeted for use on an OTL project by Stephen Dickinson - Organised Technology Ltd
#
# History:
#   20/11/2020 SJD - last updated
#
# Copyright:
#   Organised Technology Ltd 2019-2020 - all rights reserved
#
###########################################################

from serial import Serial, PARITY_NONE, SerialException
from umodbus.client.serial import rtu
from Errors import *

class Modbus(ModbusError):

    # ERROR BIT MASK
    ERR_SERIAL_PORT=   0x0001
    ERR_DEVICE_ACCESS= 0x0002

    BROADCAST_ADDRESS=  0
    MIN_MODULE_ADDRESS= 1
    MAX_MODULE_ADDRESS= 247

    ser_port_dev_name=  "/dev/ttyUSB0"
    ser_port_baud=      9600 # 115200
    ser_port_parity=    PARITY_NONE
    ser_port_stop_bits= 2
    ser_port_byte_size= 8
    ser_port_timeout=   1

    ser_port_error= False
    # modbus_error= 0

    def __init__(self, slave_id):
        self.m_slave_id= slave_id
        self.device_access_error= False

    def clearSerialPortError(self):
        Modbus.ser_port_error = False

    def testSerialPort(self) -> bool:
        self.clearSerialPortError()
        serial_port = self.openSerialPort()
        if serial_port is None:
            return False
        else:
            serial_port.close()

        if Modbus.ser_port_error:
            return False
        else:
            return True

    def testModuleAccessable(self) -> bool:
        return True

    def isDeviceOnline(self) -> bool:
        return not (Modbus.ser_port_error or self.device_access_error)

    def writeSingleRegister(self, address: int, value: int) -> bool:
        if self.isDeviceOnline():
            serial_port = None
            message = rtu.write_single_register(slave_id=self.m_slave_id, address=address, value=value)
            serial_port = self.openSerialPort()

            if serial_port is not None:
                try:
                    rtu.send_message(message, serial_port)
                except ValueError:
                    # ML.postMessage(ML.MD_POPUP, ML.ML_ERROR, "Modbus Error", "Unable to write to device:address <%d:%d>" % (self.m_slave_id, address))
                    self.device_access_error= True
                    serial_port.close()
                    print("Modbus::writeSingleRegister: ValueError")
                    return False
                    # sys.exit()
                except TypeError:
                    self.device_access_error = True
                    serial_port.close()
                    print("Modbus::writeSingleRegister:  TypeError")
                    return False

                serial_port.close()
                return True
        return False

    def writeMultipleRegisters(self, starting_address: int, values) -> bool:
        if self.isDeviceOnline():
            message= rtu.write_multiple_registers(slave_id=self.m_slave_id, starting_address=starting_address, values=values)
            serial_port = self.openSerialPort()

            if serial_port is not None:
                try:
                    rtu.send_message(message, serial_port)
                except ValueError:
                    # ML.postMessage(ML.MD_POPUP, ML.ML_ERROR, "Modbus Error", "Unable to write to device:address <%d:%d>" % (self.m_slave_id, address))
                    self.device_access_error = True
                    serial_port.close()
                    print("Modbus::writeMultipleRegisters: ValueError")
                    return False
                    #sys.exit()
                except TypeError:
                    self.device_access_error = True
                    serial_port.close()
                    print("Modbus::writeMultipleRegisters:  TypeError")
                    return False

                serial_port.close()
        return True

    def readInputRegisters2(self, starting_address: int, quantity: int):#starting_address: str
        if self.isDeviceOnline():
            message = rtu.read_input_registers(slave_id=self.m_slave_id, starting_address=starting_address, quantity=quantity)
            serial_port = self.openSerialPort()

            if serial_port is not None:
                try:
                    response = rtu.send_message(message, serial_port)
                except ValueError:
                    # ML.postMessage(ML.MD_POPUP, ML.ML_ERROR, "Modbus Error", "Unable to read from device:address <%d:%d>" % (self.m_slave_id, address))
                    self.device_access_error = True
                    serial_port.close()
                    print("Modbus::readInputRegisters: ValueError")
                    return False, [0]
                    # sys.exit()
                except TypeError:
                    self.device_access_error = True
                    serial_port.close()
                    print("Modbus::readInputRegisters:  TypeError")
                    return False, [0]

                serial_port.close()
                return len(response) == quantity, response
        return False, [0]

    def openSerialPort(self):
        """ Return serial.Serial instance, ready to use for RS485."""
        # port = Serial(port='/dev/ttyS1', baudrate=9600, parity=PARITY_NONE, stopbits=1, bytesize=8, timeout=1)

        try:
            port= Serial(port=Modbus.ser_port_dev_name,
                         baudrate=Modbus.ser_port_baud,
                         parity=Modbus.ser_port_parity,
                         stopbits=Modbus.ser_port_stop_bits,
                         bytesize=Modbus.ser_port_byte_size,
                         timeout=Modbus.ser_port_timeout)
        except SerialException:
            # ML.postMessage(ML.MD_POPUP, ML.ML_ERROR, "Modbus Error", "Unable to open RS485 serial port <%s>" % self.ser_port_dev_name)
            Modbus.ser_port_error= True
            return None
            # sys.exit()

        return port

    def test1(self):
        serial_port= self.openSerialPort()

        # message= rtu.write_multiple_coils(slave_id=2, starting_address=816, values=[1, 0, 0, 0, 0, 1, 1, 1])
        message = rtu.write_single_coil(slave_id=2, address=816, value=0)

        # Response depends on Modbus function code. This particular returns the
        # amount of coils written, in this case it is.
        response= rtu.send_message(message, serial_port)
        serial_port.close()

        print("MODBUS Rx:", response)

    def test2(self):
        serial_port= self.openSerialPort()

        # message= rtu.write_multiple_coils(slave_id=2, starting_address=816, values=[1, 0, 0, 0, 0, 1, 1, 1])
        message = rtu.write_single_coil(slave_id=2, address=816, value=1)

        # Response depends on Modbus function code. This particular returns the
        # amount of coils written, in this case it is.
        response= rtu.send_message(message, serial_port)
        serial_port.close()

        print("MODBUS Rx:", response)
        
