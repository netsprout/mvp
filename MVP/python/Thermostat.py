"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Fan import Fan
from TempSensor import TempSensor

def adjust_thermostat(temp=None, test=False):
    """Adjust the fan depending upon the temperature
           Args:
               temp: current temperature; in None, get from sensor
           Returns:
               None
           Raises:
               None
    """
    if temp == None:
        sensor = TempSensor()
        temp = sensor.check_temperature()
    fan = Fan()
    fan.adjust(temp, test)


def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    print("Test")
    adjust_thermostat(40, True)
    print("Adjust Thermostat 40")
    adjust_thermostat(20, True)
    print("Adjust Thermostat 20")
    adjust_thermostat(None, True)
    print("Adjust Thermostat None")

if __name__ == "__main__":
    adjust_thermostat()
