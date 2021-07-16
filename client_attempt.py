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
    path ="oic/res"

    #ct = {'content_type': defines.Content_types["application/link-format"]}
    ct = {}
    ct['accept'] = 10000
    ct['ocf_accept_content_format_version'] = int(2048)
    ct['ocf_content_format_version'] = int(2048)

    client = HelperClient(server=(host, port))

    response = client.get_non(path, None, None, **ct)
    uuid = '--uuid=' + response
    print("UUID is: " + response)
    client.stop()

    ## Get IP address ##
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 1))

    ip_address = s.getsockname()[0]
    print("IP address is: " + ip_address)
    ip = 'http://' + ip_address + ':32000'

    s.close()

    ## Run OCF CTT ##
    # Option 1: Run full test #
    # subprocess.Popen([r'C:\Program Files (x86)\OCF Conformance Test Tool\CTT_CLI.exe', r'--enableAutomation', 
    #                     r'--apiEndpoint', ip, 
    #                     r'--oicserver', r'--profile=Server', 
    #                     r'-pics=C:\Program Files (x86)\OCF Conformance Test Tool\PICS_module.json', 
    #                     uuid])
    
    # Option 2: Run selected tests #
    subprocess.Popen([r'C:\Program Files (x86)\OCF Conformance Test Tool\CTT_CLI.exe', 
                        r'-s', r'--profile=C:\Users\frank\Documents\autoctt-main\OCF_profile.xml', 
                        r'-pics=C:\Program Files (x86)\OCF Conformance Test Tool\PICS_module.json', 
                        uuid])

if __name__ == '__main__':  # pragma: no cover
    main()