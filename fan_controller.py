''' controls fan speed on RockPro64 single board computer '''


import sys
import datetime
import argparse

CPUMONPATH = "/sys/class/thermal/thermal_zone0/temp"
GPUMONPATH = "/sys/class/thermal/thermal_zone1/temp"
PWMMAX = 255
PWMPATH = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"


def log_now():
    ''' appends a logline to a logfile'''
    with open(get_log_path(), 'a', encoding="utf-8") as file:
        file.write(str(datetime.datetime.now()) + " - Temperature: " +
                   str(get_temp()) + "C - fanPWM: " + str(get_pwm()) + "\n")


def get_log_path():
    ''' returns path to logfile '''
    if args.path:
        return args.path
    return str(sys.path[0]) + "/fan_controller.log"


def get_pwm():
    ''' returns current PWM value of fan '''
    with open(PWMPATH, 'r', encoding="utf-8") as file:
        return file.readlines()[0].replace('\n', '')


def get_pwm_min():
    ''' returns minimum PWM value '''
    if args.minpwm is not None:
        return percentage_to_pwm(args.minpwm)
    return 60


def get_pwm_new():
    ''' returns new (forced) PWM value '''
    if args.force is not None:
        return percentage_to_pwm(args.force)
    return temperature_to_pwm(get_temp())


def get_temp():
    ''' returns degrees celsius temperature from monitor '''
    with open(get_temp_path(), 'r', encoding="utf-8") as file:
        temperature = int(file.read().replace('\n', ''))
        return temperature / 1000


def get_temp_max():
    ''' returns maximum temperature '''
    if args.max is not None:
        return int(args.max)
    return 60


def get_temp_min():
    ''' returns minimum temperature '''
    if args.min is not None:
        return int(args.min)
    return 40


def get_temp_path():
    ''' returns path to temperature monitor '''
    if args.gpu:
        return GPUMONPATH
    return CPUMONPATH


def percentage_to_pwm(percentage):
    ''' returns percentage as PWM value'''
    if percentage < 0 or percentage > 100:
        message = "Expected 0 <= value <= 100, got value = " + str(percentage)
        raise argparse.ArgumentTypeError(message)
    return round(percentage / 100 * PWMMAX)


def pwm_to_percentage(pwm):
    ''' returns PWM value as percentage'''
    return round(pwm / PWMMAX * 100)


def temperature_to_pwm(temperature):
    ''' returns matching PWM value for a given temperature '''
    try:
        get_temp_min() > get_temp_max()
    except ValueError as exc:
        raise ValueError(
            "Minimum temperature can't be higher than maximum temperature.") from exc
    if temperature >= get_temp_max():
        return PWMMAX
    if temperature < get_temp_min():
        return 0
    return round(PWMMAX / (get_temp_max() - get_temp_min())
                 * (temperature - get_temp_min()))


def write_pwm(pwm):
    ''' writes checked PWM value to PWM file, prints output if not quiet '''
    if args.quiet is False:
        print("Current temperature: " + str(get_temp()) + "C")
    try:
        value = int(pwm)
    except ValueError as err:
        raise ValueError() from err
    if value < 0 or value > PWMMAX:
        raise ValueError("Expected 0 <= value <= " + PWMMAX +
                         ", got value = " + format(value))
    with open(PWMPATH, 'w', encoding="utf-8") as file:
        if get_pwm_min() > pwm > 0:
            file.write(str(get_pwm_min()))
            if args.quiet is False:
                print("Fan set to minimum fan speed: " +
                      str(pwm_to_percentage(get_pwm_min())) +
                      "% (PWM value: " +
                      str(get_pwm_min()) +
                      ")")
            return
        file.write(str(pwm))
        if args.quiet is False:
            print("Fan set to: " + str(pwm_to_percentage(pwm)) +
                  "% (PWM value: " + str(pwm) + ")")


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--force",
    type=int,
    metavar="[0-100]",
    help="Set a static fan speed, values from 0-100.")
parser.add_argument("--gpu", action="store_true",
                    help="Use GPU temperature instead of CPU temperature.")
parser.add_argument("-l", "--log", action="store_true",
                    help="Log to a file. Set path with '--path'.")
parser.add_argument(
    "--max",
    type=int,
    help="Fan speed will be maximum above set temperature. Default: 60C.")
parser.add_argument(
    "--min", type=int,
    help="Fan will only switch on above set temperature threshold. Default: 40C.")
parser.add_argument(
    "--minpwm",
    type=int,
    metavar="[0-100]",
    help="Set minimum fan speed, values from 0-100. Default: 24 (PWM value: 60).")
parser.add_argument(
    "-p",
    "--path",
    help="Set path of logfile. Default: 'fan_controller.log' in folder of script.")
parser.add_argument("-q", "--quiet", action="store_true",
                    help="Run script quietly.")

args = parser.parse_args()

write_pwm(get_pwm_new())

if args.log:
    log_now()
