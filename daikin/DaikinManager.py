import udi_interface
from utils.Utilities import Utilities
import DaikinInterface

LOGGER = udi_interface.LOGGER

class DaikinManager():
    def __init__(self, ip):
        self.ip = ip

    async def process_fan_mode(self, fan_mode):
        try:
            LOGGER.info('process_fan_mode incoming value: ' + str(fan_mode))
            daikin_control = DaikinInterface(self.ip, False)
            await daikin_control.get_control()
            c_mode = fan_mode
            LOGGER.info('c_mode: ' + str(fan_mode))
            if c_mode == '10':
                c_mode = 'A'
            settings = {'f_rate': c_mode}
            await daikin_control.set(settings)
        except Exception as ex:
            raise

    async def process_mode(self, mode):
        try:
            LOGGER.info('process_mode incoming value: ' + str(mode))
            daikin_control = DaikinInterface(self.ip, False)
            settings = {}
            if int(mode) == 0:
                settings = {'mode': 'off'}
            else:
                settings = {'mode': Utilities.to_daikin_mode_value(mode)}
            print(settings)
            await daikin_control.set(settings)
        except Exception as ex:
            raise

    async def process_temp(self, temp):
        try:
            LOGGER.info('process_temp incoming value: ' + str(temp))
            daikin_control = DaikinInterface(self.ip, False)
            await daikin_control.get_control()
            control = daikin_control.values
            LOGGER.info('Process_temp temp : ' + str(temp))
            LOGGER.info('Process_temp stemp: ' + str(control['stemp']))
            if control['stemp'] != 'M':
                LOGGER.info('process_temp stemp is numeric: ' + str(control['stemp']))
                settings = {'stemp': Utilities.fahrenheit_to_celsius(temp)}
                await daikin_control.set(settings)
        except Exception as ex:
            raise