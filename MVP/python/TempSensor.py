"""
Abstracted humidity and temperature sensor
Technical notes of commands and operation and from:
https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf
"""
SENSOR_TYPE = 'AM2315'

import time

if SENSOR_TYPE == 'AM2315':
  from AM2315 import *
else:
  from SI7021 import SI7021

class TempSensor(object):

   def __init__(self):
      self.new_type = new_sensor(self)
      self.current_sensor = set_sensor(self)

   def sensor(self):
      return self.current_sensor

   def new_sensor(self):
     return True if (SENSOR_TYPE == 'AM2315') else False

   def set_sensor(self):
     return AM2315() if self.new_type() else SI7021()

   def check_celsius(self):
     if self.new_type:
       return self.sensor.temperature()
     else:
       return self.sensor.get_tempC()

   def check_fahrenheit(self):
     return (get_celsius(self.sensor) * 9/5) + 32

   def check_humidity(self):
     if self.new_type:
       return self.sensor.humidity()
     else:
       return self.sensor.get_humidity()

   def calc_humidity(self, read):
      """Calculate relative humidity from sensor reading
           Args:
               read: the sensor value
           Returns:
               rh: calculated relative humidity
           Raises:
               None
      """
      rh = ((125.0*read)/65536.0)-6.0
      return rh

   def calc_temp(self, read):
      """Calculate relative humidity from sensor reading
           Args:
               read: the sensor value
           Returns:
               tempC: calculated temperature in Centigrade
           Raises:
               None
      """
      tempC = ((175.72*read)/65536.0)-46.85
      return tempC

   def get_tempC_prior(self):
       """Get the temperature from the prior humidity reading
           Args:
               None
           Returns:
               tempC: calculated temperature in Centigrade
           Raises:
               None
       """

       print("\nGet Temp - get previous")
       msgs = self._i2c.get_msg([previous_temp], 3)
       if msgs == None:
           return None
       else:
           value = bytesToWord(msgs[1].data[0],msgs[1].data[1])
           tempC = self.calc_temp(value)
           return tempC

   def get_humidity(self):
       """Get the humidity
           Args:
               None
           Returns:
               rh: calculated relative humidity
           Raises:
                None
       """
       print("\nGet Humidity - no hold split")
       msgs = self._i2c.msg_write([rh_no_hold])
       # need a pause here between sending the request and getting the data
       time.sleep(0.03)
       msgs = self._i2c.msg_read(3)
       if msgs == None:
           return None
       else:
           value = bytesToWord(msgs[0].data[0], msgs[0].data[1])
           rh = self.calc_humidity(value)
           return rh

   def get_tempC(self):
       """Get the temperature (new reading)
           Args:
               None
           Returns:
               tempC: calculated temperature in Centigrade
           Raises:
               None
       """
   #    print("\nGet Temp - no hold split")
       msgs = self._i2c.msg_write([temp_no_hold])
       # need a pause here between sending the request and getting the data
       time.sleep(0.03)
       msgs = self._i2c.msg_read(3)
       if msgs == None:
           return None
       else:
           value = bytesToWord(msgs[0].data[0], msgs[0].data[1])
           return self.calc_temp(value)


   def get_rev(self):
       """Get the firmware revision number
           Args:
               None
           Returns:
               rev: coded revision number
           Raises:
               None
       """
       print("\nGet Revision")
       msgs = self._i2c.get_msg([firm_rev_1_1, firm_rev_1_2], 3)
       # Need to test, may error out on some conditions
       rev = None
       if not ((msgs is None) or (msgs[1].data is None)):
          rev = msgs[1].data[0]
          if rev == 0xFF:
              print("version 1.0")
          elif rev == 0x20:
              print("version 2.0")
          else:
              print("Unknown")
       else:
          print("No Revision Data Available")
          return rev

   def get_id1(self):
       """Print the first part of the chips unique id
           Args:
               None
           Returns:
               None
           Raises:
                None
       """
       print("\nGet ID 1")
       msgs = self._i2c.get_msg([read_id_1_1, read_id_1_2], 4)
       ret= msgs[1].data
       for data in ret:
           print("ID", hex(data))

   def get_id2(self):
       """Print the second part of the chips unique id
           The device version is in SNA_3
           Args:
               None
           Returns:
               None
           Raises:
               None
       """

       print("\nGet ID 2")
       msgs = self._i2c.get_msg([read_id_2_1, read_id_2_2], 4)
       ret= msgs[1].data
       for data in ret:
           print("ID", hex(data))
       sna3 = msgs[1].data[0]
       if sna3 == 0x00:
           print("Device: Engineering Sample")
       elif sna3 == 0xFF:
           print("Device: Engineering Sample"        )
       elif sna3 == 0x14:
           print("Device: SI7020")
       elif sna3 == 0x15:
           print("Device: SI7021")
       else:
           print("Unknown")

   def reset(self):
       """Reset the device
           Args:
               None
           Returns:
               None
           Raises:
               None
       """

       print("\nReset")
       rev_1 = self._i2c.msg_write([reset_cmd])
       print("Reset: ", rev_1)

def test():
    """Test the SI7021 functions
        Args:
            None
        Returns:
            None
        Raises:
            None
   """
    si = SI7021()
    print("\nTest Humidity - split")
    rh = si.get_humidity()
    if rh != None:
        print('Humidity : %.2f %%' % rh)
    else:
        print("Error getting Humidity")

    print("\nTest Temp - split")
    temp = si.get_tempC()
    if temp == None:
        print("Error getting Temp")
    else:
        print('Temp C: %.2f C' % temp)


    print("\nTest Temp - previous")
    temp = si.get_tempC_prior()
    if temp == None:
        print("Error getting Temp")
    else:
        print('Temp C: %.2f C' % temp)

    si.reset()
    si.get_rev()
    si.get_id1()
    si.get_id2()

if __name__ == "__main__":
    test()
