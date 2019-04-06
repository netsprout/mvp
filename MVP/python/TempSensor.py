"""
Abstracted humidity and temperature sensors
"""
import time
from AM2315 import *
from SI7021 import SI7021

class TempSensor(object):
   SENSOR_TYPE = 'AM2315' # SI7021

   def __init__(self):
      self.new_type = True if (self.SENSOR_TYPE == 'AM2315') else False
      self.current_sensor = self.set_sensor()

   def sensor(self):
      return self.current_sensor

   def set_sensor(self):
     return AM2315() if self.new_type else SI7021()

   def check_temperature(self):
     if self.new_type:
        return self.check_celsius()
     else:
        return self.sensor().get_tempC()

   def check_celsius(self):
     if self.new_type:
       return self.sensor().temperature()
     else:
       return self.sensor().get_tempC()

   def check_fahrenheit(self):
     return (self.check_celsius() * 9/5) + 32

   def check_humidity(self):
     if self.new_type:
       return self.sensor().humidity()
     else:
       return self.sensor().get_humidity()
