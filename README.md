# RockPro64 Cooling Fan Controller

Python script to control fan on a Pine64 RockPro64 single board computer.

The cooling method is slightly based on [ATS/tuxd3v](https://github.com/tuxd3v/ats). Using LibreELEC I couldn't make use of their work, because LibreELEC does not support LUA. Therefore, this is a Python implementation.

This script is system agnostic. If you find another SBC this script works for let me know and I will make a list. You might have to change the constants the script uses (written down at the end of this file). Feel free to come up with further suggestions.

## Installation

```sh
mkdir fan_controller
```
```sh
wget https://raw.githubusercontent.com/kromsam/FanControlerRockPro64/main/fan_controller.py -O fan_controller/fan_controller.py
```
```sh
python fan_controller/fan_controller.py
```

## Usage

```
usage: fan_controller.py [-h] [--min MIN] [--max MAX] [-l] [-p PATH] [-f [0-100]] [--minpwm [0-100]] [--gpu]

optional arguments:
  -h, --help            show this help message and exit
  --min MIN             Fan will only switch on above set temperature threshold. Default: 40C.
  --max MAX             Fan speed will be maximum from set temperature. Default: 60C.
  -l, --log             Log to a file. Set path with '--path'.
  -p PATH, --path PATH  Set path of logfile. Default: 'fan_controller.log' in folder of script.
  -f [0-100], --force [0-100]
                        Set a static fan speed, values from 0-100.
  --minpwm [0-100]      Set minimum fan speed, values from 0-100. Default: 24 (PWM value: 60).
  --gpu                 Use GPU temperature instead of CPU temperature.
```

### Automatic mode

The fan will be switched on with its minimum speed when the minimum temperature is reached. Fan speed will rise incrementally and will be at full speed from the maximum temperature and above.

#### Configuration

Set up a cronjob with `crontab -e` (in this example the script runs every minute).
```sh
*/1 * * * * python fan_controller/fan_controller.py
```

### Static mode

Instead of basing speed on measured temperature level, set a static speed for the fan. Values from 0-100.

```sh
python fan_controller/fan_controller.py --force 90
```

### Constants

The script uses the following constants.

```python
CPUMONPATH = "/sys/class/thermal/thermal_zone0/temp"
GPUMONPATH = "/sys/class/thermal/thermal_zone1/temp"
PWMMAX = 255
PWMPATH = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"
```

## Troubleshooting

If the script can't find PWM with the default value, it might have a different path. Change `PWMPATH` to the output of the following command.

```sh
find /sys -name pwm1 | grep hwmon
```
