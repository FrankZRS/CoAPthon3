#!/usr/bin/env python
import getopt
import socket
import sys
import cbor
import json

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

__author__ = 'Giacomo Tanganelli'

client = None


def usage():  # pragma: no cover
    print("Command:\tcoapclient.py -o -p [-P]")
    print("Options:")
    print("\t-o, --operation=\tGET|GETNONE|PUT|POST|DELETE|DISCOVER|OBSERVE")
    print("\t-p, --path=\t\t\tPath of the request")
    print("\t-P, --payload=\t\tPayload of the request")
    print("\t-c, --contenttype=\t\tcontenttype of the request")
    print("\t-f, --payload-file=\t\tFile with payload of the request")


def client_callback(response):
    print("Callback")


def client_callback_observe(response):  # pragma: no cover
    global client
    print("Callback_observe")
    check = True
    while check:
        chosen = eval(input("Stop observing? [y/N]: "))
        if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
            print("Unrecognized choose.")
            continue
        elif chosen == "y" or chosen == "Y":
            while True:
                rst = eval(input("Send RST message? [Y/n]: "))
                if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
                    print("Unrecognized choose.")
                    continue
                elif rst == "" or rst == "y" or rst == "Y":
                    client.cancel_observing(response, True)
                else:
                    client.cancel_observing(response, False)
                check = False
                break
        else:
            break


def main():  # pragma: no cover
    global client
    op = None
    path = None
    payload = None
    content_type = None
    #ct = {'content_type': defines.Content_types["application/link-format"]}
    ct = {}
    ct['accept'] = 0
    ct['ocf_accept_content_format_version'] = int(2048)
    ct['ocf_content_format_version'] = int(2048)
    
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:c:", ["help", "operation=", "path=", "payload=",
                                                               "payload_file=","content-type"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print((str(err)))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-o", "--operation"):
            op = a
        elif o in ("-p", "--path"):
            path = a
        elif o in ("-P", "--payload"):
            payload = a
        elif o in ("-c", "--content-type"):
            ct['accept'] = a
            print ("content type request : ", ct)
        elif o in ("-f", "--payload-file"):
            with open(a, 'r') as f:
                payload = f.read()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if op is None:
        print("Operation must be specified")
        usage()
        sys.exit(2)

    if path is None:
        print("Path must be specified")
        usage()
        sys.exit(2)

    if not path.startswith("coap://"):
        print("Path must be conform to coap://host[:port]/path")
        usage()
        sys.exit(2)

    host, port, path = parse_uri(path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))
    if op == "GET":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        response = client.get(path, None, None, **ct)
        print((response.pretty_print()))
        if response.content_type == defines.Content_types["application/json"]:
            json_data = json.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        if response.content_type == defines.Content_types["application/cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        if response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        client.stop()
    elif op == "GETNONE":
        if path is None:
            print("Path cannot be empty for a GET-None request")
            usage()
            sys.exit(2)
        response = client.get_non(path, None, None, **ct)
        print((response.pretty_print()))
        if response.content_type == defines.Content_types["application/json"]:
            json_data = json.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        if response.content_type == defines.Content_types["application/cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        if response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print ("JSON ::")
            print (json_string)
        client.stop()
    elif op == "OBSERVE":
        if path is None:
            print("Path cannot be empty for a GET request")
            usage()
            sys.exit(2)
        client.observe(path, client_callback_observe)
        
    elif op == "DELETE":
        if path is None:
            print("Path cannot be empty for a DELETE request")
            usage()
            sys.exit(2)
        response = client.delete(path)
        print((response.pretty_print()))
        client.stop()
    elif op == "POST":
        if path is None:
            print("Path cannot be empty for a POST request")
            usage()
            sys.exit(2)
        if payload is None:
            print("Payload cannot be empty for a POST request")
            usage()
            sys.exit(2)
        print ( "payload for POST (ascii):", payload )
        print (ct['accept'] )
        if ct['accept'] == str(60):
            print ("hello")
            json_data = json.loads(payload)
            print ( "payload for POST (json):", json_data )
            cbor_data = cbor.dumps(json_data)
            print ( "payload for POST (cbor):", cbor_data )
            payload = bytes(cbor_data)
            print ("binary::")
            print (payload)
        #if ct['accept'] == defines.Content_types["application/vnd.ocf+cbor"]:
        #    json_data = json.loads(payload)
        #    cbor_data = cbor.loads(json_data)
        #    payload = cbor_data
            
        response = client.post(path, payload, None, None, **ct)
        
        print((response.pretty_print()))
        if response.content_type == defines.Content_types["application/cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
        if response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
        client.stop()
    elif op == "PUT":
        if path is None:
            print("Path cannot be empty for a PUT request")
            usage()
            sys.exit(2)
        if payload is None:
            print("Payload cannot be empty for a PUT request")
            usage()
            sys.exit(2)
        response = client.put(path, payload)
        print((response.pretty_print()))
        client.stop()
    elif op == "DISCOVER":
        response = client.discover(None, None, **ct)
        print((response.pretty_print()))
        if response.content_type == defines.Content_types["application/cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
        if response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
        client.stop()
    else:
        print("Operation not recognized")
        usage()
        sys.exit(2)


if __name__ == '__main__':  # pragma: no cover
    main()
