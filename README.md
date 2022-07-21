# RockPro64 Cooling Fan Controller

Python script to control fan on a Pine64 RockPro64 single board computer. Useful on LibreELEC.

## Installation

```
mkdir fan_controller
```
```
wget https://raw.githubusercontent.com/kromsam/FanControlerRockPro64/master/fan_controller.py -O fan_controller/fan_controller.py
```
```
python fan_controller/fan_controller.py
```

## Usage

```
usage: fan_controller.py [-h] [--min MIN] [--max MAX] [-l] [-p PATH] [-f [0-100]] [--minpwm [0-100]] [--gpu]

optional arguments:
  -h, --help            show this help message and exit
  --min MIN             Fan will only switch on above set temperature threshold. Default: 40C.
  --max MAX             Fan speed will be maximum above set temperature. Default: 60C.
  -l, --log             Log to a file. Set path with '--path'.
  -p PATH, --path PATH  Set path of logfile. Default: 'fan_controller.log' in folder as script.
  -f [0-100], --force [0-100]
                        Set a static fan speed, values from 0-100.
  --minpwm [0-100]      Set minimum fan speed. Default: 24 percent (fanPWM: 60).
  --gpu                 Use GPU temperature instead of CPU temperature.
```

### Automatic mode

Enables fan if temperature is between tempMax = 70 and tempMin = 35 where tempMax is 100% fan speed and tempMin is 23%.

#### Configuration

Set up a cronjob (updates every minute in this example).
```
*/1 * * * * python fan_controller/fan_controller.py
```

### Static mode

Static fan speed to desired strengh 0-100:

```
python fan_controller/fan_controller.py force 90
```
