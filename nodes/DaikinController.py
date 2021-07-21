import udi_interface
import logging
import time
from pydaikin.discovery import Discovery

from nodes import DaikinNode

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
LOG_HANDLER.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')
LOG_HANDLER.set_basic_config(True, logging.DEBUG)

class DaikinController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(DaikinController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll, address)
        #self.poly.subscribe(self.poly.CONFIG, self.configHandler)
        #self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.ready()
        self.poly.addNode(self)

    # def parameterHandler(self, params):
    #     pass
    #
    # def configHandler(self, config):
    #     pass

    def start(self):
        #serverdata = self.poly.get_server_data(check_profile=True)
        #LOGGER.info('Started udi-daikin-poly NodeServer {}'.format(serverdata['version']))
        LOGGER.info('Started udi-daikin-poly NodeServer')

        # self.poly.updateProfile()
        # self.poly.setCustomParamsDoc()

        LOGGER.critical('Calling Discovery from start')
        self.discover()
        self.setDriver('ST', 1)
        self.set_debug_level(self.getDriver('GV1'))

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.debug('shortPoll (controller)')
            self.query()
        else:
            LOGGER.debug('longPoll (controller)')
            self.query()

    def query(self,command=None):
        LOGGER.debug("Query sensor {}".format(self.address))

        for node in self.poly.nodes:
            if self.poly.nodes[node] is not self:
                self.poly.nodes[node].query()
            self.poly.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        LOGGER.critical('In Discovery Method')
        discovery = Discovery()
        devices = discovery.poll(stop_if_found=None, ip=None)
        LOGGER.critical(devices)
        for device in iter(devices):
            end_ip = device['ip'][device['ip'].rfind('.') + 1:]
            LOGGER.critical("Adding Node {}".format(end_ip))
            self.poly.addNode(DaikinNode(self.poly, self.address, end_ip, device['name'], device['ip']))

    def delete(self):
        LOGGER.info('Deleting Daikin controller node.  Deleting sub-nodes...')
        for node in self.poly.nodes:
            if node.address != self.address:
                self.poly.nodes[node].delete()

    def stop(self):
        LOGGER.debug('Daikin NodeServer stopped.')

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    def set_debug_level(self,level):
        LOGGER.info('set_debug_level: {}'.format(level))
        if level is None:
            level = 30
        level = int(level)
        if level == 0:
            level = 30

        LOGGER.info('set_debug_level: Set GV1 to {}'.format(level))
        self.setDriver('GV1', level)
        # 0=All 10=Debug are the same because 0 (NOTSET) doesn't show everything.
        if level <= 10:
            LOGGER.setLevel(logging.DEBUG)
        elif level == 20:
            LOGGER.setLevel(logging.INFO)
        elif level == 30:
            LOGGER.setLevel(logging.WARNING)
        elif level == 40:
            LOGGER.setLevel(logging.ERROR)
        elif level == 50:
            LOGGER.setLevel(logging.CRITICAL)
        else:
            LOGGER.debug("set_debug_level: Unknown level {}".format(level))
        if level <= 10:
            LOG_HANDLER.set_basic_config(True,logging.DEBUG)
        else:
            # This is the polyinterface default
            LOG_HANDLER.set_basic_config(True,logging.WARNING)

    def cmd_set_debug_mode(self,command):
        val = int(command.get('value'))
        LOGGER.debug("cmd_set_debug_mode: {}".format(val))
        self.set_debug_level(val)

    def remove_notices_all(self, command):
        self.Notices.clear()

    id = 'controller'
    commands = {
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'QUERY': query,
        'DISCOVER': discover,
        'SET_DM': cmd_set_debug_mode
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 10, 'uom': 25} # Debug (Log) Mode, default=10=Debug
    ]
