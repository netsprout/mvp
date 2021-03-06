# MVP III

Latest Release: 3.1.8

Chanage Log: 2018/11/24
 - Fix CouchDB binary download to modify ownership to couchdb
 - Chanage ownership of log files to fix write problem
 - Add java script to index.html to give charts a unique name (Chrome caching problem fix)

Change Log: 2018/10/2
 - Added binary CouchDB to get around build problems
 - NOTE: Fuxton is not included in this binary

Change Log: 2018/09/24
 - add chmod to Startup.sh so logs always have the correct write permission

Change Log: 2018/09/21
  - Correct typo in Startup.sh

Change Log: 2018/07/05
  - Major change to the data JSON structure, this should be the final version
  - Removed SI7021 dependency on smbus, replaced with python-periphery
  - Added StartUp.py to check state of lights when reboot
  - Added HeartBeat.py to check CouchDB is up and running, or else will reboot automatically to reset the system
  - Removed web access to CouchDB
  - File and method name changes for consistency with the python code standard
  - Add standard Python logging
  - Removed retreival of geo information due to API deprecation

## Background 

Code and instructions for building the 'brain' of the controled environment hydroponics unit.
It is mostly a collection of python code that runs on a Raspberry Pi (or similar device).  See the OpenAg [forums](http://forum.openag.media.mit.edu/) for discussion and issues:

The MVP (Minimal Viable Product) is a simplified version of the MIT OpenAg Food Computer.

## Assumptions

 - Follows the instructions for building a Raspbian (Noobs) system.
 - Configure the environment (see below).  Turn VNC on, this is the easiest way to view multiple Raspberry Pis without needing separate keyboards and monitors for each.  You can view all the Raspberries on your local network through one Raspberry, or download VNC to a PC and access them through a PC.
 
 ## Building multiple MVPs
  - Once you have configured one SD card, from the main menu, use the Accessories/SD Card Copier to replicate the system for the other MVPs.  Just be sure to run the following so that a unique ID will be created for each MVP
  
  > python /home/pi/MVP/python/Environment.py

## Architecture:
The MVP brain is mostly python scripts involed using cron as the scheduler.  
Python and cron are built into the Raspbian OS, and the Raspberry library to manipulate GPIO pins is already loaded.

The Python is modular so additions and changes can easily be made without affecting the whole system.

- Scheduling Control (cron)
  - Image capture (Webcam.sh)
  - Log Sensors (LogSensors.py)
  - Turn lights On (LightOn.py)
  - Tirm lights Off (LightOff.py)
  - Check Temperature (Thermostat.py)
  - Refresh charts and picture for the UI (Render.sh)

CouchDB is the main data storage system, and will provide easy replication to the cloud in the future.

For more information on Cron [see:](https://docs.oracle.com/cd/E23824_01/html/821-1451/sysrescron-24589.html)

## Hardware Build:

**Fan:**
There are two fans, one for circulation and one for exhausting excess heat  These can run off the Raspberry's 5V or from a external 12V transformer

**Temperature/Humidity Sensor**
A SI7021 sensor on an I2C bus is used for temperature and humidity.  See the following for (instructions)[https://learn.adafruit.com/adafruit-si7021-temperature-plus-humidity-sensor/overview] on use and wiring.

**Webcam**
A standard USB camera is used for imaging (though the Raspberry Pi camera is an option).  See [here](https://www.raspberrypi.org/documentation/usage/webcams/) for instructions

**Relay**
A set of relays controled by GPIO pins is used to turn lights on and off (120V), and the exhaust fan (12V)

# Pin Assignment:
Refer to the following [diagram](https://docs.particle.io/datasheets/raspberrypi-datasheet/#pin-out-diagram) for the Raspberry's pin names:

Code follows the board number convention.

- '3 - SDA to SI7021'
- '5 - SCL to SI7021'
- '29 - light relay (relay #4)'
- '31 - (reserved for relay #3)'
- '33 - (reserved for relay #2)'
- '35 - GPIO13 fan control (relay #1)'


## Build Activities
### Assumptions:
1. NOOB install of Raspbian on Raspberry Pi
2. The Raspbian system has been configured 
    - for localization (time, timezone)
    - wifi is established and connected
    - I2C has been enabled
    - VNC is enabled for easy remote access
    - Screen resolution is set to Mode 16 for proper VNC viewing
    
2. 32G SD card to hold data
3. Sensors and relay are wired to the Pi.  If you try to run the code without sensors, some of it will error out (I/O Error, I noticed in the get_tempC() function).  This will ripple up to error out the cron job for LogSensor.py.
>
### Software Build

The build scripts are the documentation.  If you want to build things yourself, follow the scripts (/home/pi/MVP/setup).
Download the initial build script, change its permissions, and run it.  This script will call other scripts that manage partricular parts of the system.  From a command prompt, run the following three commands:

```
wget raw.github.com/futureag/mvp/master/MVP/setup/Build.sh
chmod +x /home/pi/Build.sh
/home/pi/Build.sh
```
## Manual Build
The following scripts (in /home/pi/MVP/scripts) can be run separately and in sequence if any errors are encountered.  Look within the scripts for single commands.

- releaseScript.sh calls the following scripts:
- releaseScript_DB.sh - installs the CouchDB code
- releaseScript_Local.sh - builds libraries, starts the database and initializes things
- releaseScript_Test.sh - calls Validate.sh to test the system
- releaseScript_Final.sh - configures start-up and loads cron

## To Do:
1. Add a watchdog to the Raspberry
2. Fix the cron email notifications

## Future Development (in no priority):
- GUI interface for setting persistent variables (could be local)
- Add a pump for when have to be away for a while and need to refill the reservoir.
- Light control for controlable LEDs
