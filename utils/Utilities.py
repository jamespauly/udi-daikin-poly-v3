from datetime import datetime

class Utilities:
    # TODO: Need to switch these to dictionary lookups
    def to_isy_mode_value(mode):
        if mode is None:
            return 0
        elif mode == 3:
            return 2
        elif mode == 0:
            return 3
        elif mode == 4:
            return 1
        elif mode == 10:
            return 0
        elif mode == 2:
            return 8
        elif mode == 7:
            return 3
        elif mode == 1:
            return 3
        else:
            return mode

    def to_daikin_mode_value(mode):
        if mode is None:
            return '0'
        elif mode == '2':
            return '3'
        elif mode == '3':
            return '7'
        elif mode == '1':
            return '4'
        elif mode == '0':
            return '10'
        elif mode == '8':
            return '2'
        else:
            return mode


    def to_isy_fan_mode_value(mode):
        if mode == 'A':
            return 0
        elif mode == 'B':
            return 10
        elif mode == '0':
            return 3
        elif mode == '3' or mode == '4' or mode == '5' or mode == '6' or mode == '7':
            return 1


    def to_isy_fan_mode_detail(mode):
        if mode == 'A':
            return 'Auto'
        elif mode == 'B':
            return 'Quiet'
        elif mode == '3':
            return '1'
        elif mode == '4':
            return '2'
        elif mode == '5':
            return '3'
        elif mode == '6':
            return '4'
        elif mode == '7':
            return '5'


    def to_driver_value(temp, as_int=True):
        if temp is None:
            return 0

        temp = float(temp)

        if as_int:
            return int(round(temp))
        else:
            return round(temp, 1)


    def get_seconds_from_midnight():
        now = datetime.now()
        return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()


    def celsius_to_fahrenheit(celsius, as_int=True):
        celsius = float(celsius)
        if as_int:
            return int(round((celsius * (9 / 5)) + 32))
        else:
            return round((celsius * (9 / 5)) + 32, 1)


    def fahrenheit_to_celsius(fahrenheit, as_int=True):
        fahrenheit = float(fahrenheit)
        if as_int:
            return int(round((fahrenheit - 32) * 5 / 9))
        else:
            return round((fahrenheit - 32) * 5 / 9, 1)
