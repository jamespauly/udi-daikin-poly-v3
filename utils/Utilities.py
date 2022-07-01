from datetime import datetime


class Utilities:
    to_isy_mode = {
        None: 0,
        '3': 2,
        '0': 3,
        '4': 1,
        '10': 0,
        '2': 8,
        '7': 3,
        '1': 3
    }

    to_daikin_mode = {
        None: '0',
        2: '3',
        3: '7',
        1: '4',
        0: '10',
        8: '2'
    }

    to_isy_fan_mode = {
        'A': '0',
        'B': '10',
        '0': '3',
        '3': '1',
        '4': '1',
        '5': '1',
        '6': '1',
        '7': '1'
    }

    to_isy_fan_mode_detail = {
        'A': 'Auto',
        'B': 'Quiet',
        3: 1,
        4: 2,
        5: 3,
        6: 4,
        7: 5
    }

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
