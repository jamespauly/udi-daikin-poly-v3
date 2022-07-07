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
        '1': 3,
        '6': 5
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

    def isfloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

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
