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

        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')

        self.poly.subscribe(self.poly.START, self.start, address)

        self.poly.ready()
        self.poly.addNode(self)

    def start(self):
        LOGGER.info('Staring Daikin NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        self.discover()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))
        self.discover()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Daikin Device Discovery")
        discovery = Discovery()
        devices = discovery.poll(stop_if_found=None, ip=None)
        for device in iter(devices):
            device_id = device['mac'][-10:].lower()
            if self.poly.getNode(device_id) is None:
                LOGGER.info("Adding Node {}".format(device_id))
                self.poly.addNode(DaikinNode(self.poly, self.address, device_id, device['name'], device['ip']))
            else:
                daikin_node = self.poly.getNode(device_id)
                daikin_node.query()
                LOGGER.info('Node {} already exists, skipping'.format(device_id))

        LOGGER.info('Finished Node discovery')

    def delete(self):
        LOGGER.info('Deleting Daikin Node Server')

    def stop(self):
        LOGGER.info('Daikin NodeServer stopped.')

    id = 'daikin'
    commands = {
        'DISCOVER': discover
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]