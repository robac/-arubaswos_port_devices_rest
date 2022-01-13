import argparse
import os
import pprint
import sys

from aruba.ArubaSW import *
from tools import *

MAC_IGNORE_TRESHOLD = 5
EXCEL_OUTPUT_DIR = "c:\\users\\poch\desktop\\farmtec"

def get_arguments():
    parser = argparse.ArgumentParser(description='Aruba SWOS REST tool.')
    parser.add_argument("-i", action="store", dest="ip", required=True, help="switch IP address")
    parser.add_argument("-p", action="store", dest="password", required=True, help="switch password")
    parser.add_argument("-u", action="store", dest="username", required=True, help="switch username")
    parser.add_argument('--ssl', dest='ssl', action='store_true', help="use SSL (default NO)")
    parser.add_argument('--no-ssl', dest='ssl', action='store_false', help = "don't use SS (default NO).")
    parser.set_defaults(ssl=False)
    parser.add_argument(
        '-a', type=argparse.FileType('r'), default=sys.stdin, dest='arp_filename',
        required=True, help="file with ARP records")
    parser.add_argument(
        '-o', required=True, help='output directory', dest='output_dir',
        metavar='DIR', type=lambda x: arghelper.is_valid_directory(parser, x))

    arguments = parser.parse_args()
    print(arguments.output_dir)
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

def get_excel_filename(data, arguments):
    return os.path.join(arguments.output_dir, "{}.{}".format(data['ip'], "xlsx"))

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
        arps = tools.read_arps_input(arguments.arp_filename, devPatterns)
        statuses = aruba.load_status(device)
        ports = aruba.load_ports(device, statuses)
        aruba.load_macs(device, ports, arps)
        excel.export_excel(get_excel_filename(cdata, arguments), ports)
    except Exception as e:
        print(e)
    finally:
        device.logout()

main()


