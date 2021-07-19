#!/usr/bin/env python
import getopt
import socket
import sys
import cbor
import json
import time
import traceback
import subprocess

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

__author__ = 'Giacomo Tanganelli'

client = None

def main():  # pragma: no cover
    ## Get UUID ##
    host = "ff05::158"
    port = 5683
    path ="oic/d"

    #ct = {'content_type': defines.Content_types["application/link-format"]}
    ct = {}
    ct['accept'] = 10000
    ct['ocf_accept_content_format_version'] = int(2048)
    ct['ocf_content_format_version'] = int(2048)

    client = HelperClient(server=(host, port))

    response = client.get_non(path, None, None, **ct)
    payload = str(response.payload)
    print(payload)
    pos1 = payload.find("$")
    uuid = payload[(pos1 + 1):(pos1 + 37)]
    print("UUID is: " + uuid)

    client.stop()

    ## Get IP address ##
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 1))

    ip_address = s.getsockname()[0]
    print("IP address is: " + ip_address)

    s.close()

    ## Run OCF CTT ##
    # Option 1: Run full test #
    # subprocess.Popen([r'C:\Program Files (x86)\OCF Conformance Test Tool\CTT_CLI.exe', 
    #                     r'--enableAutomation', 
    #                     r'--apiEndpoint', r'http://' + ip_address + r':32001', 
    #                     r'--oicserver', r'--profile=Server', 
    #                     r'-pics=C:\Program Files (x86)\OCF Conformance Test Tool\PICS_module.json', 
    #                     r'--uuid=' + uuid])
    
    # Option 2: Run selected tests #
    subprocess.Popen([r'C:\Program Files (x86)\OCF Conformance Test Tool\CTT_CLI.exe', 
                        r'--enableAutomation', 
                        r'--apiEndpoint', r'http://' + ip_address + r':32001', 
                        #r'--enableAutomation', r'--apiEndpoint=http://192.168.12.60:32001', 
                        r'--enableExtendedAutomation', 
                        r'--extendedApiEndpoint', r'http://' + ip_address + r':32001', 
                        r'-s', r'--profile=C:\Users\frank\Documents\autoctt-main\full_run.xml', 
                        r'-pics=C:\Program Files (x86)\OCF Conformance Test Tool\PICS_module.json', 
                        r'--uuid=' + uuid])

if __name__ == '__main__':  # pragma: no cover
    main()