from .DevicePattern import DevicePattern
from .exceptions import *

def load_patterns():
    devPatterns = DevicePattern()
    devPatterns.add_pattern('arubaswos_farmtec_macaddresstable', "^\s*([a-z0-9]{6}-[a-z0-9]{6})\s*(\S+)\s*(\d)*$")
    devPatterns.add_pattern('arubaswos_farmtec_showint', "^\s{2}(.{8})\s{1}(.{10})\s{1}(.{7})\s{1}(.{13})\s{1}(.{8})\s{1}(.{10})\s{1}(.{6})\s{1}(.{1,8})")
    devPatterns.add_pattern('juniper_farmtec_getarp_old', "^(.{15})\s(.{12})\s*\S*\s*(\S*).*")
    devPatterns.add_pattern('juniper_farmtec_getarp', "^(.{16})\s(.{12})\s*\S*\s*(\S*).*")
    return devPatterns

def parse_arp(text, patternCompiled):
    m = patternCompiled.match(text)
    if not m:
        raise InputException
    else:
        ip = m.group(1).strip()
        mac = normalize_mac_twelve_digits(m.group(2).strip())
        state = m.group(3).strip()
    return mac, ip, state

def read_arps_input(file, devPatterns):
    #input = open(filename, 'r')
    lines = file.readlines()
    file.close()
    arps = {}

    for line in lines:
        mac, ip, state = parse_arp(line, devPatterns.get_pattern_compiled('juniper_farmtec_getarp'))
        if (state in ['VLD', 'STS']):
            arps[mac] = ip
    return arps


def normalize_mac_two_groups(mac):
    return "{}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[7:9], mac[9:11], mac[11:13])

def normalize_mac_twelve_digits(mac):
    return "{}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])