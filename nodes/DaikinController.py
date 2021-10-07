import udi_interface
from pydaikin.discovery import Discovery
from nodes import DaikinNode
from daikin.DaikinManager import DaikinManager
import re

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

class DaikinController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(DaikinController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address
        self.daikin_manager = DaikinManager()
        self.broadcastIpList = []
        self.broadcastIpsDefined = False

        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameter_handler)

        self.poly.ready()
        self.poly.addNode(self)

    def get_driver_value(self, driver):
        for d in self.drivers:
            if d['driver'] == driver:
                return d['value']
        LOGGER.error('{} not found in drivers array'.format(driver))
        return -1

    def parameter_handler(self, params):
        self.Notices.clear()
        self.Parameters.load(params)

        if self.Parameters['broadcast_ips'] is not None and self.Parameters['broadcast_ips'].strip() != '':
            ip_valid = True
            self.broadcastIpList = self.Parameters['broadcast_ips'].split(",")
            if len(self.broadcastIpList) > 0 and (self.Parameters.isChanged('broadcast_ips') or self.Parameters.isNew('broadcast_ips')):
                for ip in self.broadcastIpList:
                    if re.search(
                            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                            ip, re.M) == None:
                        LOGGER.error('IP {} invalid.'.format(ip))
                        self.Notices['ip'] = 'IP Address {} must be in correct format ex. (10.1.0.255)'.format(ip)
                        ip_valid = False
                        break
                if ip_valid:
                    self.broadcastIpsDefined = True
                else:
                    return
        self.discover()

    def start(self):
        LOGGER.info('Staring udi-daikin-poly NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        # self.discover()

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (controller)')
            pass
        else:
            LOGGER.info('longPoll (controller)')
            self.query()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))

        if self.getDriver("CLISPC") is not None:
            LOGGER.debug('Driver CLISPC: ' + self.get_driver_value("CLISPC"))
        else:
            self.setDriver("CLISPC", "72")
            LOGGER.debug('Driver None CLISPC: ' + self.get_driver_value("CLISPC"))

        for node in self.poly.nodes:
            if self.poly.nodes[node] is not self:
                self.poly.nodes[node].query()
                LOGGER.debug('Query All - Node Name: ' + self.poly.nodes[node].name)
            self.poly.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Daikin Device Discovery")
        discovery = Discovery()
        device = None
        if self.broadcastIpsDefined:
            for broadcastIp in self.broadcastIpList:
                devices = discovery.poll(stop_if_found=None, ip=broadcastIp)
                for device in iter(devices):
                    #end_ip = device['ip'][device['ip'].rfind('.') + 1:]
                    deviceNode = self.poly.getNode(device['ip'])
                    if deviceNode is None:
                        LOGGER.critical("Adding Node {}".format(device['ip']))
                        self.poly.addNode(DaikinNode(self.poly, self.address, device['ip'], device['name'], device['ip']))
        else:
            devices = discovery.poll(stop_if_found=None, ip=None)
            for device in iter(devices):
                #end_ip = device['ip'][device['ip'].rfind('.') + 1:]
                deviceNode = self.poly.getNode(device['ip'])
                if deviceNode is None:
                    LOGGER.critical("Adding Node {}".format(device['ip']))
                    self.poly.addNode(DaikinNode(self.poly, self.address, device['ip'], device['name'], device['ip']))

        self.query()

    def delete(self):
        LOGGER.info('Deleting Daikin Node Server')

    def stop(self):
        LOGGER.info('Daikin NodeServer stopped.')

    def cmd_set_temp(self, cmd):
        LOGGER.debug('Start cmd_set_temp set temp ' + str(cmd))
        for node in self.poly.nodes:
            LOGGER.debug('cmd_set_temp node name ' + self.poly.nodes[node].name)
            if self.poly.nodes[node] is not self:
                LOGGER.debug('cmd_set_temp set temp ' + str(cmd))
                self.poly.nodes[node].cmd_set_temp(cmd)
                self.poly.nodes[node].query()

    def cmd_set_mode(self, cmd):
        LOGGER.debug('Start cmd_set_mode set mode ' + str(cmd))
        for node in self.poly.nodes:
            LOGGER.debug('cmd_set_mode node name ' + self.poly.nodes[node].name)
            if self.poly.nodes[node] is not self:
                LOGGER.debug('cmd_set_mode set mode ' + str(cmd))
                self.poly.nodes[node].cmd_set_mode(cmd)
                self.poly.nodes[node].query()

    def cmd_set_fan_mode(self, cmd):
        LOGGER.debug('Start cmd_set_fan_mode set mode ' + str(cmd))
        for node in self.poly.nodes:
            LOGGER.debug('cmd_set_fan_mode node name ' + self.poly.nodes[node].name)
            if self.poly.nodes[node] is not self:
                LOGGER.debug('cmd_set_fan_mode set mode ' + str(cmd))
                self.poly.nodes[node].cmd_set_fan_mode(cmd)
                self.poly.nodes[node].query()

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'SET_TEMP': cmd_set_temp,
        'SET_MODE': cmd_set_mode,
        'SET_FAN_MODE': cmd_set_fan_mode
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'CLISPC', 'value': 70, 'uom': '17'},  # Set Cool Point
        {'driver': 'CLIMD', 'value': 2, 'uom': '67'},  # Current Mode
        {'driver': 'GV3', 'value': 10, 'uom': '25'}
    ]