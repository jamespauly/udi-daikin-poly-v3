import udi_interface
from utils.Utilities import Utilities
from daikin.DaikinInterface import DaikinInterface
import json

LOGGER = udi_interface.LOGGER

class DaikinManager():
    async def process_fan_mode(self, fan_mode, ip):
        try:
            LOGGER.info('process_fan_mode incoming value: ' + str(fan_mode))
            daikin_control = DaikinInterface(ip, False)
            await daikin_control.get_control()
            c_mode = fan_mode
            LOGGER.info('c_mode: ' + str(fan_mode))
            if c_mode == '10':
                c_mode = 'A'
            settings = {'f_rate': c_mode}
            await daikin_control.set(settings)
        except Exception as ex:
            raise

    async def process_mode(self, mode, ip):
        try:
            LOGGER.info('process_mode incoming value: ' + str(mode))
            daikin_control = DaikinInterface(ip, False)
            settings = {}
            if mode == 10:
                settings = {'mode': 'off', 'pow': '0'}
            else:
                settings = {'mode': str(mode)}
            LOGGER.debug('Process Mode Settings: ' + json.dumps(settings))
            await daikin_control.set(settings)
        except Exception as ex:
            raise

    async def process_temp(self, temp, ip):
        try:
            LOGGER.info('process_temp incoming value: ' + str(temp))
            daikin_control = DaikinInterface(ip, False)
            await daikin_control.get_control()
            control = daikin_control.values
            LOGGER.info('Process_temp temp : ' + str(temp))
            LOGGER.info('Process_temp stemp: ' + control['stemp'])
            if Utilities.isfloat(control['stemp']):
                LOGGER.info('process_temp stemp is numeric: ' + control['stemp'])
                settings = {'stemp': Utilities.fahrenheit_to_celsius(temp)}
                await daikin_control.set(settings)
        except Exception as ex:
            raise