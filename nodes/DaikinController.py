import udi_interface
import logging
import time
from pydaikin.discovery import Discovery

from nodes import DaikinNode

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
        self.poly.ready()
        self.poly.addNode(self)

    def start(self):
        LOGGER.info('Started udi-daikin-poly NodeServer')
        self.discover()
        self.setDriver('ST', 1)

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (controller)')
            pass
        else:
            LOGGER.info('longPoll (controller)')
            self.query()

    def query(self,command=None):
        LOGGER.info("Query sensor {}".format(self.address))

        for node in self.poly.nodes:
            if self.poly.nodes[node] is not self:
                self.poly.nodes[node].query()
            self.poly.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Daikin Device Discovery")
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
        LOGGER.info('Daikin NodeServer stopped.')

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
