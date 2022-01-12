import argparse
import pprint
from arubaswos.loginOs import *

MAC_IGNORE_TRESHOLD = 5

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




"""
def read_macs_input(ports, arps, devPatterns, data):
    input = open(INPUT_MAC_FILENAME, 'r')
    lines = input.readlines()

    for line in lines:
        mac = MacInfo(line, devPatterns.get_pattern_compiled('arubaswos_farmtec_macaddresstable'))
        if mac.mac in arps.keys():
            mac.setIP(arps[mac.mac])
        if mac.port in ports.keys():
            ports[mac.port].addMac(mac)
        else:
            print("Unknown port: {}".format(mac.port))
    return
"""
"""
def read_arps_input(devPatterns):
    input = open(INPUT_ARP_FILENAME, 'r')
    lines = input.readlines()
    arps = {}

    for line in lines:
        mac, ip, state = parse_arp(line, devPatterns.get_pattern_compiled('juniper_farmtec_getarp'))
        if (state in ['VLD', 'STS']):
            arps[mac] = ip
    return arps
"""
"""
def read_ports_input(devPatterns):
    ports = {}

    for line in lines:
        port = PortInfo(line, devPatterns.get_pattern_compiled('arubaswos_farmtec_showint'))
        ports[port.port] = port
    return ports
"""
"""
def print_ports(ports):
    for id, port in ports.items():
        if port.status == "Up":
            print("Port {}".format(port.port))
            if len(port.macs) == 0:
                print("NO MAC ADDRESS")
            elif len(port.macs) > MAC_IGNORE_TRESHOLD:
                print ("TOO MANY ({}) MAC ADDRESSSES".format(len(port.macs)))
            else:
                for mac in port.macs:
                    print("   {}".format(mac.mac))
                    print("     {}".format(mac.vendor))
                    if mac.ip is None:
                        print("     IP unknown")
                    else:
                        print("     IP: {}".format(mac.ip))
    return


def main():
    devPatterns = load_patterns()
    arps = read_arps_input(devPatterns)
    ports = read_ports_input(devPatterns)
    read_macs_input(ports, arps, devPatterns)
    print_ports(ports)

"""
def main():
    arguments = get_arguments()
    data = conn_data(arguments)
    login_os(data)

    try:
        response = send_get_request(data, 'ports', 'port_element')
        #for item in response:
        #    print(item['mac_address'])
        pprint.pprint(response)
    except:
        pass

    logout(data)


main()


