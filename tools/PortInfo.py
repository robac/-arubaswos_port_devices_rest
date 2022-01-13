class PortInfo:
    def __init__(self, item):
        self.id = item['id']
        self.name = item['name']
        self.macs = []
        self.status = None

    def addMac(self, mac):
        self.macs.append(mac)

    def addStatus(self, status):
        self.status = status