import udi_interface
from utils.Utilities import Utilities
import DaikinInterface

LOGGER = udi_interface.LOGGER

class DaikinManager():
    async def process_fan_mode(self, mode, ip):
        try:
            LOGGER.info('Process_fan_mode incoming value: ' + str(mode))
            daikin_control = DaikinInterface(ip, False)
            await daikin_control.get_control()
            c_mode = mode
            LOGGER.info('c_mode: ' + str(mode))
            if c_mode == '10':
                c_mode = 'A'
            settings = {'f_rate': c_mode}
            await daikin_control.set(settings)
            #self.setDriver("GV3", mode)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)
            raise

    async def process_mode(self, mode, ip):
        try:
            LOGGER.info('Process_mode incoming value: ' + str(mode))
            daikin_control = DaikinInterface(ip, False)
            settings = {}
            if int(mode) == 0:
                settings = {'mode': 'off'}
            else:
                settings = {'mode': Utilities.to_daikin_mode_value(mode)}
            print(settings)
            await daikin_control.set(settings)
            #self.setDriver('CLIMD', mode)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)
            raise

    async def process_temp(self, temp, ip):
        try:
            daikin_control = DaikinInterface(ip, False)
            await daikin_control.get_control()
            control = daikin_control.values
            LOGGER.info('Process_temp temp : ' + str(temp))
            LOGGER.info('Process_temp stemp: ' + str(control['stemp']))
            if control['stemp'] != 'M':
                LOGGER.info('process_temp stemp is numeric: ' + str(control['stemp']))
                settings = {'stemp': Utilities.fahrenheit_to_celsius(temp)}
                await daikin_control.set(settings)
                self.setDriver("CLISPC", temp)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)
            raise