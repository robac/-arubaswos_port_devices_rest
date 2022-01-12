import argparse
import pprint
from aruba.ArubaSW import *
from tools.tools import *

MAC_IGNORE_TRESHOLD = 5
INPUT_ARP_FILENAME = "data/arps.txt"

def get_arguments():
    parser = argparse.ArgumentParser(description='Aruba SWOS REST tool.')
    parser.add_argument("-i", "--ip", action="store", dest="ip", required=True)
    parser.add_argument("-p", "--password", action="store", dest="password", required=True)
    parser.add_argument("-u", "--username", action="store", dest="username", required=True)
    parser.add_argument('--ssl', dest='ssl', action='store_true')
    parser.add_argument('--no-ssl', dest='ssl', action='store_false')
    parser.set_defaults(ssl=False)

    arguments = parser.parse_args()
    return arguments

def conn_data(arguments):
    data = {}
    data['password'] = arguments.password
    data['user'] = arguments.username
    data['ip'] = arguments.ip
    data['ssl'] = arguments.ssl
    return data





def load_macs(device, ports, arps):
    response = device.send_request('/mac-table', 'GET', 'port_element')

    for item in response['mac_table_entry_element']:
        mac = MacInfo(item)
        if mac.mac in arps.keys():
            mac.setIP(arps[mac.mac])
        if mac.port in ports.keys():
            ports[mac.port].addMac(mac)
        else:
            print("Unknown port: {}".format(mac.port))
    return

def read_arps_input(devPatterns):
    input = open(INPUT_ARP_FILENAME, 'r')
    lines = input.readlines()
    arps = {}

    for line in lines:
        mac, ip, state = parse_arp(line, devPatterns.get_pattern_compiled('juniper_farmtec_getarp'))
        if (state in ['VLD', 'STS']):
            arps[mac] = ip
    return arps

def load_ports(device, statuses):
    response = device.send_request('/ports', 'GET', 'port_element')
    ports = {}

    for i in response['port_element']:
        port = PortInfo(i)
        if port.id in statuses:
            port.addStatus(statuses[port.id]['status'])
        ports[port.id] = port
    return ports


def get_mac_ip_text(mac):
    if mac.ip is None:
        return "IP unknown"
    else:
        return "IP: {}".format(mac.ip)


def print_ports(ports):
    for id, port in ports.items():
        if port.status == "OPER_UP":
            print("Port {}".format(port.id))
            if len(port.macs) == 0:
                print("NO MAC ADDRESS")
            elif len(port.macs) > MAC_IGNORE_TRESHOLD:
                print ("TOO MANY ({}) MAC ADDRESSSES".format(len(port.macs)))
            else:
                for mac in port.macs:
                    print("   {}".format(mac.mac))
                    print("   {}".format(mac.vendor))
                    print("   {}".format(get_mac_ip_text(mac)))
                    print()
    return



def load_status(device):
    response = device.send_request('/system/status/switch', 'GET', 'port_element')
    statuses = {}

    for i in response['blades']:
        for port in i['data_ports']:
            id = str(port['port_id'])
            statuses[id] = {}
            statuses[id]['status'] = port['operStatus']
    return statuses

def main():
    arguments = get_arguments()
    device = ArubaSW(conn_data(arguments))
    device.login()

    try:
        """
        response = device.send_request('/system/status/switch', 'GET', 'port_element')
        pprint.pprint(response)
        return
"""
        devPatterns = load_patterns()
        arps = read_arps_input(devPatterns)
        statuses = load_status(device)
        ports = load_ports(device, statuses)
        load_macs(device, ports, arps)
        print_ports(ports)
    except Exception as e:
        print(e)
    finally:
        device.logout()


main()


