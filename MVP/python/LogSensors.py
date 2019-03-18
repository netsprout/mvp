""" Log standard MVP sensors
"""

from TempSensor import TempSensor
from CouchUtil import saveList


def log_sensors(test = False):

    sensor = TempSensor()

    try:
        temp = sensor.check_temperature()

        status = 'Success'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', sensor.SENSOR_TYPE, status, ''])
    except Exception as e:
        status = 'Failure'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', '', 'Farenheight', sensor.SENSOR_TYPE, status, str(e)])

    try:
        humid = sensor.check_humidity()

        status = 'Success'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', "{:10.1f}".format(humid), 'Percent', sensor.SENSOR_TYPE, status, ''])

    except Exception as e:
        status = 'Failure'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', '', 'Percent', sensor.SENSOR_TYPE, status, str(e)])


def test():
    log_sensors(True)

if __name__=="__main__":
    log_sensors()
