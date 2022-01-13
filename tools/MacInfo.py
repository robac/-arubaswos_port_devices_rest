from .tools import *
from mac_vendor_lookup import MacLookup

class MacInfo:
    macLookup = MacLookup()

    def __init__(self, item):
        global macLookup
        self.mac = normalize_mac_two_groups(item['mac_address'])
        self.port = item['port_id']
        self.ip = None
        try:
            self.vendor = MacInfo.macLookup.lookup(self.mac)
        except:
            self.vendor = "UNKNOWN"

    def setIP(self, ip):
        self.ip = ip
