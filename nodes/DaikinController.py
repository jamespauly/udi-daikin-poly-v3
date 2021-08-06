import udi_interface
import logging
from pydaikin.discovery import Discovery
import asyncio
from nodes import DaikinNode
from simplekv.memory import DictStore
from daikin.DaikinManager import DaikinManager
import re
import time

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER


class DaikinController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(DaikinController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.ready()
        self.poly.addNode(self)
        self.base_store = DictStore()

    def parameterHandler(self, params):
        self.Notices.clear()
        self.Parameters.load(params)
        self.ips_defined = False

        if self.Parameters['IPs'] is not None:
            ip_valid = True
            ip_list = self.Parameters['IPs'].split(",")
            for ip in ip_list:
                if re.search(
                        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                        ip, re.M) == None:
                    LOGGER.error('IP {} invalid.'.format(ip))
                    self.Notices['ip'] = 'IP Address {} must be in correct format.'.format(ip)
                    ip_valid = False
                    break
            if ip_valid:
                self.ips_defined = True

            if self.Parameters.isChanged('IPs'):
                self.discover()

    def start(self):
        LOGGER.info('Staring udi-daikin-poly NodeServer')
        # self.poly.updateProfile()
        # self.poly.setCustomParamsDoc()
        while not self.configured:
            time.sleep(10)
        self.discover()

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (controller)')
            pass
        else:
            LOGGER.info('longPoll (controller)')
            self.query()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))

        for node in self.poly.nodes:
            if self.poly.nodes[node] is not self:
                self.poly.nodes[node].query()
                LOGGER.debug('Query All - Node Name: ' + self.poly.nodes[node].name)
            self.poly.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Daikin Device Discovery")
        discovery = Discovery()
        devices = discovery.poll(stop_if_found=None, ip=None)
        device_ips = ""
        LOGGER.critical(devices)
        key_num = 0
        for device in iter(devices):
            end_ip = device['ip'][device['ip'].rfind('.') + 1:]
            LOGGER.critical("Adding Node {}".format(end_ip))
            self.poly.addNode(DaikinNode(self.poly, self.address, end_ip, device['name'], device['ip']))
            device_ips = device_ips + ',' + device['ip']
            key_num = key_num + 1
            self.base_store.put(str(key_num), bytes(device['ip'].encode()))

    def delete(self):
        LOGGER.info('Deleting Daikin Node Server')

    def stop(self):
        LOGGER.info('Daikin NodeServer stopped.')

    def cmd_set_temp(self, cmd):
        for key in self.base_store.keys():
            ip = self.base_store.d.get(key).decode('utf-8')
            asyncio.run(DaikinManager.process_temp(cmd['value'], ip))
        self.query()

    def cmd_set_mode(self, cmd):
        for key in self.base_store.keys():
            ip = self.base_store.d.get(key).decode('utf-8')
            asyncio.run(DaikinManager.process_mode(cmd['value'], ip))
        self.query()

    def cmd_set_fan_mode(self, cmd):
        for key in self.base_store.keys():
            ip = self.base_store.d.get(key).decode('utf-8')
            asyncio.run(DaikinManager.process_fan_mode(cmd['value'], ip))
        self.query()

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'SET_TEMP': cmd_set_temp,
        'SET_MODE': cmd_set_mode,
        'SET_FAN_MODE': cmd_set_fan_mode
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
