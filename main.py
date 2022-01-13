import argparse
import os
import pprint
import sys

from aruba.ArubaSW import *
from tools import *

MAC_IGNORE_TRESHOLD = 5
INPUT_ARP_FILENAME = "data/arps.txt"
EXCEL_OUTPUT_DIR = "c:\\users\\poch\desktop\\farmtec"

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
                print("   NO MAC ADDRESS")
            elif len(port.macs) > MAC_IGNORE_TRESHOLD:
                print ("   TOO MANY ({}) MAC ADDRESSSES".format(len(port.macs)))
            else:
                for mac in port.macs:
                    print("   {}".format(mac.mac))
                    print("   {}".format(mac.vendor))
                    print("   {}".format(get_mac_ip_text(mac)))
                    print()
    return

def get_excel_filename(data):
    return os.path.join(EXCEL_OUTPUT_DIR, "{}.{}".format(data['ip'], "xlsx"))

def test_get(device, action, endapp=True):
    res = device.send_request('/lldp/local-port', 'GET', '')
    pprint.pprint(res)
    if endapp:
        device.logout()
        sys.exit()
    return

def main():
    arguments = get_arguments()
    cdata = conn_data(arguments)
    device = ArubaSW(cdata)
    device.login()

    #test_get(device, '/lldp/local-port')

    try:
        devPatterns = tools.load_patterns()
        arps = tools.read_arps_input(INPUT_ARP_FILENAME, devPatterns)
        statuses = aruba.load_status(device)
        ports = aruba.load_ports(device, statuses)
        aruba.load_macs(device, ports, arps)
        excel.export_excel(get_excel_filename(cdata), ports)
    except Exception as e:
        print(e)
    finally:
        device.logout()

main()


