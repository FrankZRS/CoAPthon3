#!/usr/bin/env python
import getopt
import socket
import sys
import cbor
#from cbor2 import dumps, loads
import json
import time
import traceback

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

__author__ = 'Giacomo Tanganelli'

client = None
paths = {}
paths_extend = {}


def usage():  # pragma: no cover
    print("Command:\tknxcoapclient.py -o -p [-P]")
    print("Options:")
    print("\t-o, --operation=\tGET|GETNONE|PUT|POST|DELETE|DISCOVER|OBSERVE")
    print("\t-p, --path=\t\t\tPath of the request")
    print("\t-P, --payload=\t\tPayload of the request")
    print("\t-c, --contenttype=\t\tcontenttype of the request")
    print("\t-f, --payload-file=\t\tFile with payload of the request")


def get_url(line):
    data = line.split(">")
    url = data[0]
    return url[1:]

def get_ct(line):
    tagvalues = line.split(";")
    for tag in tagvalues:
       if tag.startswith("ct"):
          ct_value_all = tag.split("=")
          ct_value = ct_value_all[1].split(",")
          return ct_value[0]
    return ""

def get_base(url):
    # python3 knxcoapclient.py -o GET -p coap://[fe80::6513:3050:71a7:5b98]:63914/a -c 50
    my_url = url.replace("coap://","")
    mybase = my_url.split("/")
    return mybase[0]

def convertlinkformat2links(payload):
    print("convertlinkformat2links\n")
    global paths
    global paths_extend
    lines = payload.splitlines()
    
    # add the 
    if len(paths) == 0:
        my_base = get_base(get_url(lines[0]))
        #print ("\n")
        #print ("python3 knxcoapclient.py -o GET -p coap://{}/dev -c 40".format(my_base))
        #print ("python3 knxcoapclient.py -o GET -p coap://{}/swu -c 40".format(my_base))
        #print ("python3 knxcoapclient.py -o GET -p coap://{}/.well-known/knx -c 50".format(my_base))
        my_str = "coap://"+my_base+"/dev/iid"
        my_str = "coap://"+my_base+"/dev/ia"
        #paths[my_str] = 60
        
        my_str = "coap://"+my_base+"/dev"
        #paths[my_str] = 40
        my_str = "coap://"+my_base+"/swu"
        #paths[my_str] = 40
        my_str = "coap://"+my_base+"/.well-known/knx"
        #paths[my_str] = 50
        
        my_str = "coap://"+my_base+"/fp/gm"
        paths[my_str] = 40
        my_str = "coap://"+my_base+"/fp/gm/1"
        paths[my_str] = 60
        
        my_str = "coap://"+my_base+"/fp/g"
        paths[my_str] = 40
        my_str = "coap://"+my_base+"/fp/g/1"
        paths[my_str] = 60
        
        
        my_str = "coap://"+my_base+"/fp/r"
        paths[my_str] = 40
        my_str = "coap://"+my_base+"/fp/r/1"
        paths[my_str] = 60
    
    
        my_str = "coap://"+my_base+"/fp/p"
        paths[my_str] = 40
        my_str = "coap://"+my_base+"/fp/p/1"
        paths[my_str] = 60
    
    
        # return
        
        for line in lines:
            url = get_url(line)
            ct = get_ct(line)
            #print ("python3 knxcoapclient.py -o GET -p {} -c {}".format(url,ct))
            try:
              paths[url] = ct
            except:
              paths_extend[url] = ct
              print ("==>url not added to paths_extend:", url, ct)
    else:
       for line in lines:
            print (line)
            url = get_url(line)
            ct = get_ct(line)
            #print ("python3 knxcoapclient.py -o GET -p {} -c {}".format(url,ct))
            #print ("setting url")
            paths_extend[url] = ct
            print ("==>url added to paths_extend:", url, ct)
          

def client_callback(response, checkdata=None):
    print(" --- Callback ---")
    if response is not None:
        print ("response code:",response.code)
        print ("response type:",response.content_type)
        if response.code > 100:
            print("+++returned error+++")
            return
        #print(response.pretty_print())
        if response.content_type == defines.Content_types["application/cbor"]:
            print (type(response.payload), len(response.payload))
            print ("=========")
            print (response.payload)
            print ("=========")
            #json_data = loads(response.payload)
            #print(json_data)
            #print ("=========")
            json_data = cbor.loads(response.payload)
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
            print ("===+++===")
            if checkdata is not None:
               check_data = cbor.loads(checkdata)
               check_string = json.dumps(check_data, indent=2, sort_keys=True)
               print("  check: ")
               print (check_string)
               if check_string == json_string:
                  print("  =+++===> OK  ")
               else:
                  print("  =+++===> NOT OK  ")
            
            print (json_string)
        elif response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("application/vnd.ocf+cbor")
            try:
                print (type(response.payload), len(response.payload))
                print ("=========")
                print (response.payload)
                print ("=========")
                json_data = cbor.loads(response.payload)
                print (json_data)
                print ("---------")
            except:
                traceback.print_exc()
            json_string = json.dumps(json_data, indent=2, sort_keys=True)
            print (json_string)
        elif response.content_type == defines.Content_types["application/link-format"]:
            print (response.payload.decode())
            convertlinkformat2links(response.payload.decode())
        else:
            if response.payload is not None:
              print ("type, len", type(response.payload), len(response.payload))
              print (response.payload)
            else:
                print ("    not handled: ", response)
    else:
        print (" Response : None")
    #check = True
    #while check:
    #    chosen = eval(input("Stop observing? [y/N]: "))
    #    if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
    #        print("Unrecognized choose.")
    #        continue


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


def execute_list():
    global paths
    global paths_extend
    for path, ct_value  in paths.items():
        execute_get(path, ct_value)
        execute_put(path, ct_value)
        execute_post(path, ct_value)
        execute_del(path, ct_value)
    
    #return
    print("=======EXTENDED=======")
    for path, ct_value  in paths_extend.items():
        execute_get(path, ct_value)
        execute_put(path, ct_value)
        execute_post(path, ct_value)
        execute_del(path, ct_value)

def execute_get(mypath, ct_value):
      print ("---------------------------")
      print ("execute_get: ", ct_value, mypath)
      print (type(mypath))
      
      if (mypath is None or len(mypath) < 5):
        return
      if mypath.startswith("coap://") == False:
        print(" not executing: ", mypath);
        return;

      ct = {}
      ct['accept'] = ct_value
      host, port, path = parse_uri(mypath)
      try:
        tmp = socket.gethostbyname(host)
        host = tmp
      except socket.gaierror:
        pass
      nclient = HelperClient(server=(host, port))
      response = nclient.get(path, None, None, **ct)
      client_callback(response)
      nclient.stop()

def execute_del(mypath, ct_value):
      #print ("---------------------------")
      #print ("execute_del: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = ct_value
      ct['content_type'] = ct_value
      
      if mypath.startswith("coap://") == False:
        #print(" not executing: ", mypath);
        return;
      
      host, port, path = parse_uri(mypath)
      try:
        tmp = socket.gethostbyname(host)
        host = tmp
      except socket.gaierror:
        pass
      nclient = HelperClient(server=(host, port))
      nclientcheck = HelperClient(server=(host, port))
      payload = 0
      do_del = False
      if path.__contains__("fp/gm/1"):
        do_del = True
        contents = 5 # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_del   ", path, contents, payload)
        
      if path.__contains__("fp/g/1"):
        do_del = True
        contents = 5 # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_del   ", path, contents, payload)

      if do_del:
        response = nclient.delete(path, None, None, **ct)
        client_callback(response)
        #nclient.stop()
        #sys.exit(2)
        print ("=======")
        
        if do_exit:
          sys.exit(2)


def execute_post(mypath, ct_value):
      print ("---------------------------")
      print ("execute_post: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = ct_value
      ct['content_type'] = ct_value
      
      if mypath.startswith("coap://") == False:
        print(" not executing: ", mypath);
        return
      
      host, port, path = parse_uri(mypath)
      try:
        tmp = socket.gethostbyname(host)
        host = tmp
      except socket.gaierror:
        pass
      nclient = HelperClient(server=(host, port))
      nclientcheck = HelperClient(server=(host, port))
      payload = 0
      do_post = False
      if path == "fp/g":
        do_post = True
        # do_exit = True
        contents = [ {"id": 1, "href": "xxxx", "cflag": [1,2,3,4,5], "ga":[2222,3333]} ]
        payload = cbor.dumps(contents)
        ct['content_type'] = 60
        ct['accept'] = 60
        print ("---------------------------")
        print ("  execute_post   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
      if path == "fp/p":
        do_post = True
        # do_exit = True
        contents = [{"id": 7, "ia": "myiid.5", "path": "mypath-p", "ga":[2305, 2306, 2307, 2308]} ]
        payload = cbor.dumps(contents)
        ct['content_type'] = 60
        ct['accept'] = 60
        print ("---------------------------")
        print ("  execute_post   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
      if path == "fp/r":
        do_post = True
        # do_exit = True
        contents = [ {"id": 5, "ia": "myiid.5", "path": "mypath-r", "ga":[2222,3333]} ]
        payload = cbor.dumps(contents)
        ct['content_type'] = 60
        ct['accept'] = 60
        print ("---------------------------")
        print ("  execute_post   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
      if do_post:
        response = nclient.post(path, payload, None, None , None, **ct)
        client_callback(response)
        nclient.stop()
        #sys.exit(2)
        #print ("=======")
        #response_check = nclientcheck.get(path, None, None, **ct)
        #client_callback(response_check, payload)
        #nclientcheck.stop()
        #print ("=======")
        
        if do_exit:
          sys.exit(2)

def execute_put(mypath, ct_value):
      #print ("---------------------------")
      #print ("execute_put: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = ct_value
      ct['content_type'] = ct_value
      
      if mypath.startswith("coap://") == False:
        #print(" not executing: ", mypath);
        return
      
      host, port, path = parse_uri(mypath)
      try:
        tmp = socket.gethostbyname(host)
        host = tmp
      except socket.gaierror:
        pass
      nclient = HelperClient(server=(host, port))
      nclientcheck = HelperClient(server=(host, port))
      payload = 0
      do_put = False
      if path.__contains__("dev/ia"):
        do_put = True
        contents = 5 # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_put   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
      if path.__contains__("dev/iid"):
        do_put = True
        contents = "25345" # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_put   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
      if path.__contains__("dev/hostname"):
        do_put = True
        contents = "new host name" # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_put   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
        # do_exit = True
      if path.__contains__("dev/pm"):
        do_put = True
        contents = True # string
        payload = cbor.dumps(contents)
        print ("---------------------------")
        print ("  execute_put   ", path, contents, payload)
        contents_i = cbor.loads(payload)
        print ("  ", contents)
        print ("  ", contents_i)
        print ("---------------------------")
        do_exit = True
      if do_put:
        response = nclient.put(path, payload, None, None , None, **ct)
        client_callback(response)
        nclient.stop()
        #sys.exit(2)
        print ("=======")
        response_check = nclientcheck.get(path, None, None, **ct)
        client_callback(response_check, payload)
        nclientcheck.stop()
        print ("=======")
        
        if do_exit:
          sys.exit(2)
        


def main():  # pragma: no cover
    global client
    op = None
    path = None
    payload = None
    content_type = None
    #ct = {'content_type': defines.Content_types["application/link-format"]}
    ct = {}
    ct['accept'] = 40
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
        if response.content_type == defines.Content_types["application/link-format"]:
            #json_data = cbor.loads(response.payload)
            #json_string = json.dumps(json_data, indent=2, sort_keys=True)
            #print ("JSON ::")
            print (response.payload.decode())
            print ("\n\n")
            convertlinkformat2links(response.payload.decode())
            
            
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
        if ct['accept'] == str(defines.Content_types["application/cbor"]):
            json_data = json.loads(payload)
            cbor_data = cbor.dumps(json_data)
            payload = bytes(cbor_data)
        if ct['accept'] == str(defines.Content_types["application/vnd.ocf+cbor"]):
            json_data = json.loads(payload)
            cbor_data = cbor.loads(json_data)
            payload = cbor_data
            
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
        #response = client.discover( path, client_callback, None, **ct)
        response = client.discover( path, None, None, **ct)
        if response is not None:
            print(response.pretty_print())
            if response.content_type == defines.Content_types["application/cbor"]:
                json_data = cbor.loads(response.payload)
                json_string = json.dumps(json_data, indent=2, sort_keys=True)
                print (json_string)
            if response.content_type == defines.Content_types["application/vnd.ocf+cbor"]:
                json_data = cbor.loads(response.payload)
                json_string = json.dumps(json_data, indent=2, sort_keys=True)
                print (json_string)
            if response.content_type == defines.Content_types["application/link-format"]:
                #json_data = cbor.loads(response.payload)
                #json_string = json.dumps(json_data, indent=2, sort_keys=True)
                print (response.payload.decode())
                # do_get(response.payload.decode(), client)
                client_callback(response)
        
        counter = 2
        try:
           while counter > 0:
              time.sleep(1)
              counter = counter - 1
           #client.stop()
        except KeyboardInterrupt:
           print("Client Shutdown")
           #client.stop()
           
        execute_list()
        client.stop()
    else:
        print("Operation not recognized")
        usage()
        sys.exit(2)


if __name__ == '__main__':  # pragma: no cover
    main()
