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

    subprocess.Popen(['C:\Program Files (x86)\OCF Conformance Test Tool\CTT_CLI.exe', '--enableAutomation', 
                        '--apiEndpoint', 'http://192.168.12.60:32000', 
                        '--oicserver', '--profile=Server', 
                        '-pics=C:\Program Files (x86)\OCF Conformance Test Tool\PICS_module.json', 
                        uuid])

if __name__ == '__main__':  # pragma: no cover
    main()