import asyncio

import udi_interface
from utils.Utilities import Utilities
from daikin.DaikinInterface import DaikinInterface
from daikin.DaikinManager import DaikinManager

LOGGER = udi_interface.LOGGER

class DaikinNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, ip):
        super(DaikinNode, self).__init__(polyglot, primary, address, name)
        self.ip = ip
        self.address = address
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.daikin_manager = DaikinManager()

    async def process_fan_mode(self, fan_mode):
        try:
            await self.daikin_manager.process_fan_mode(fan_mode, self.ip)
            self.setDriver("GV3", fan_mode, True)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)

    async def process_mode(self, mode):
        try:
            await self.daikin_manager.process_mode(mode, self.ip)
            self.setDriver('CLIMD', mode, True)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)

    async def process_temp(self, temp):
        try:
            await self.daikin_manager.process_temp(temp, self.ip)
            self.setDriver("CLISPC", temp, True)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)

    async def process(self):
        try:
            daikin_sensor = DaikinInterface(self.ip, False)
            await daikin_sensor.get_sensor()
            sensor = daikin_sensor.values
            daikin_control = DaikinInterface(self.ip, False)
            await daikin_control.get_control()
            control = daikin_control.values
            LOGGER.info('Inside Temp: ' + str(Utilities.celsius_to_fahrenheit(sensor['htemp'])))
            self.setDriver('CC', Utilities.celsius_to_fahrenheit(sensor['htemp']), True)
            LOGGER.info('stemp: ' + str(control['stemp']))
            if control['stemp'] != 'M':
                self.setDriver('CLISPC', Utilities.celsius_to_fahrenheit(control['stemp']), True)
                LOGGER.info('Set Temp: ' + str(control['stemp']))
            LOGGER.info('Process Mode: ' + str(control['mode']))
            LOGGER.info('ISY process mode: ' + str(Utilities.to_isy_mode_value(control['mode'])))
            if int(control['pow']) == 1:
                self.setDriver('CLIMD', Utilities.to_isy_mode_value(int(control['mode'])), True)
            else:
                self.setDriver('CLIMD', 0, True)
            LOGGER.info('Fan Speed: ' + str(control['f_rate']))
            LOGGER.info('ISY Fan Speed: ' + str(Utilities.to_isy_fan_mode_value(control['f_rate'])))
            c_mode = control['f_rate']
            if c_mode == 'A':
                c_mode = 10
            LOGGER.info('c_mode: ' + str(c_mode))
            self.setDriver('GV3', c_mode, True)
        except Exception as ex:
            LOGGER.exception("Could not refresh diakin sensor %s because %s", self.address, ex)

    def cmd_set_temp(self, cmd):
        asyncio.run(self.process_temp(cmd['value']))

    def cmd_set_mode(self, cmd):
        asyncio.run(self.process_mode(cmd['value']))

    def cmd_set_fan_mode(self, cmd):
        asyncio.run(self.process_fan_mode(cmd['value']))

    def query(self):
        LOGGER.info("Query sensor {}".format(self.address))
        asyncio.run(self.process())
        for node in self.poly.nodes:
            self.poly.nodes[node].reportDrivers()

    def start(self):
        self.query()

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info("shortPoll (%s)", self.address)
            self.query()
        else:
            LOGGER.info("longPoll (%s)", self.address)
            pass

    drivers = [{'driver': 'CC', 'value': 0, 'uom': '17'},  # Current Temp
               {'driver': 'CLISPC', 'value': 0, 'uom': '17'},  # Set Cool Point
               {'driver': 'CLIMD', 'value': 0, 'uom': '67'},  # Current Mode
               {'driver': 'GV3', 'value': 0, 'uom': '25'}  # Set Fan Mode
               ]

    commands = {
        'SET_TEMP': cmd_set_temp,
        'SET_MODE': cmd_set_mode,
        'SET_FAN_MODE': cmd_set_fan_mode
    }

    id = 'daikinnode'