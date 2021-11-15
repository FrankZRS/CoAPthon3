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

client = None
paths = {}
paths_extend = {}

my_base = ""


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


def get_base_from_link(payload):
    print("get_base_from_link\n")
    global paths
    global paths_extend
    lines = payload.splitlines()
    
    # add the 
    if len(paths) == 0:
        my_base = get_base(get_url(lines[0]))
        return my_base
        


# no json tags as strings
def do_sequence_dev(my_base):

    print("===================")
    print("Get SN :");
    execute_get("coap://"+my_base+"/dev/sn", 60)

    print("===================")
    print("Get HWT :");
    execute_get("coap://"+my_base+"/dev/hwt", 60)
    
    print("===================")
    print("Get HWV :");
    execute_get("coap://"+my_base+"/dev/hwv", 60)

    print("===================")
    print("Get FWV :");
    execute_get("coap://"+my_base+"/dev/fwv", 60)

    print("===================")
    print("Get Model :");
    execute_get("coap://"+my_base+"/dev/model", 60)

    print("===================")
    content = True
    print("set PM :", content);
    execute_put("coap://"+my_base+"/dev/pm", 60, 60, content)
    execute_get("coap://"+my_base+"/dev/pm", 60)
    content = False
    print("set PM :", content);
    execute_put("coap://"+my_base+"/dev/pm", 60, 60, content)
    execute_get("coap://"+my_base+"/dev/pm", 60)
    
    print("===================")
    content = 44
    print("set IA :", content);
    execute_put("coap://"+my_base+"/dev/ia", 60, 60, content)
    execute_get("coap://"+my_base+"/dev/ia", 60)
    
    print("===================")
    content = "my host name"
    print("set hostname :", content);
    execute_put("coap://"+my_base+"/dev/hostname", 60, 60, content)
    execute_get("coap://"+my_base+"/dev/hostname", 60)
    
    
    print("===================")
    content = " iid xxx"
    print("set iid :", content);
    execute_put("coap://"+my_base+"/dev/iid", 60, 60, content)
    execute_get("coap://"+my_base+"/dev/iid", 60)



# id ==> 0
# href ==> 11
# ga ==> 7
# cflag ==> 8
def do_sequence_fp_g_int(my_base):

    #  url, content, accept, contents
    content = [ {0: 1, 11: "xxxx1", 8: [1,2,3,4,5], 7:[2222,3333]} ] 
    execute_post("coap://"+my_base+"/fp/g", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/g/1", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)
    content = [ {0: 2, 11: "xxxxyyy2", 8: [1,4,5], 7:[44,55,33]}, {0: 3, 1: "xxxxyyy3", 8: [1,4,5], 7:[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/g", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/g/2", 60)
    execute_get("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)
    
    execute_del("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)

def do_sequence_fp_g(my_base):

    #  url, content, accept, contents
    content = [ {"id": 1, "href": "xxxx1", "cflag": [1,2,3,4,5], "ga":[2222,3333]} ] 
    execute_post("coap://"+my_base+"/fp/g", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/g/1", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)
    content = [ {"id": 2, "href": "xxxxyyy2", "cflag": [1,4,5], "ga":[44,55,33]}, {"id": 3, "href": "xxxxyyy3", "cflag": [1,4,5], "ga":[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/g", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/g/2", 60)
    execute_get("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)
    
    execute_del("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g/3", 60)
    execute_get("coap://"+my_base+"/fp/g", 40)
    
        
# id ==> 0
# ia ==> 12
# path ==> 112
# url ==> 10
# ga ==> 7
def do_sequence_fp_p_int(my_base):

    #  url, content, accept, contents
    content = [ {0: 1, 12: "Ia.IA1", 112: "path1", 7:[2222,3333]} ] 
    execute_post("coap://"+my_base+"/fp/p", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/p/1", 60)
    # 40 == application-link format
    execute_get("coap://"+my_base+"/fp/p", 40)
    content = [ {0: 2, 12: "xxxxyyyia2", 112: "path2", 7:[44,55,33]}, 
                {0: 3, 12: "xxxxyyyia3", 112: "path3", 7:[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/p", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/p/2", 60)
    execute_get("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p", 40)
    
    execute_del("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p", 40)

def do_sequence_fp_p(my_base):

    #  url, content, accept, contents
    content = [ {"id": 1, "ia": "Ia.IA1", "path": "path1", "ga":[2222,3333]} ] 
    execute_post("coap://"+my_base+"/fp/p", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/p/1", 60)
    # 40 == application-link format
    execute_get("coap://"+my_base+"/fp/p", 40)
    content = [ {"id": 2, "ia": "xxxxyyyia2", "path": "path2","ga":[44,55,33]}, {"id": 3, "ia": "xxxxyyyia3", "path": "path3","ga":[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/p", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/p/2", 60)
    execute_get("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p", 40)
    
    execute_del("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p/3", 60)
    execute_get("coap://"+my_base+"/fp/p", 40)



# id ==> 0
# ia ==> 12
# path ==> 112
# url ==> 10
# ga ==> 7
def do_sequence_fp_r_int(my_base):

    #  url, content, accept, contents
    content = [ { 0: 1, 12: "r-Ia.IA1", 112: "r-path1", 7:[2222,3333]}  ] 
    execute_post("coap://"+my_base+"/fp/r", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/r/1", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)
    content = [ { 0: 2, 12: "r-Ia.IA2", 10: "url2", 112: "r-path2", 7:[44,55,33]}, 
                {0: 3, 12: "r-Ia.IA3", 112: "r-path3", 7:[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/r", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/r/2", 60)
    execute_get("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)
    
    execute_del("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)

def do_sequence_fp_r(my_base):

    #  url, content, accept, contents
    content = [ {"id": 1, "ia": "r-Ia.IA1", "path": "r-path1", "ga":[2222,3333]}  ] 
    execute_post("coap://"+my_base+"/fp/r", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/r/1", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)
    content = [ {"id": 2, "ia": "r-Ia.IA2", "path": "r-path2", "ga":[44,55,33]}, {"id": 3, "ia": "r-Ia.IA3", "path": "r-path3", "ga":[44,55,33]} ] 
    execute_post("coap://"+my_base+"/fp/r", 60, 60, content)
    execute_get("coap://"+my_base+"/fp/r/2", 60)
    execute_get("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)
    
    execute_del("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r/3", 60)
    execute_get("coap://"+my_base+"/fp/r", 40)


# cmd ==> 2
def do_sequence_lsm_int(my_base):

    #  url, content, accept, contents

    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {2 : "startLoading"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {2 : "loadComplete"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {2 : "unload"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)

def do_sequence_lsm(my_base):

    #  url, content, accept, contents

    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {"cmd": "startLoading"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {"cmd": "loadComplete"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)
    
    content = {"cmd": "unload"}
    execute_post("coap://"+my_base+"/a/lsm", 60, 60, content)
    execute_get("coap://"+my_base+"/a/lsm", 60)


# ./knx resource
# sia ==> 4
# ga ==> 7
# st 6 
def do_sequence_knx_knx_int(my_base):

    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.knx", 60)
    content = {"value": { 4 : 5, 7: 7777 , 6 : "rp"}}
    execute_post("coap://"+my_base+"/.knx", 60, 60, content)
    execute_get("coap://"+my_base+"/.knx", 60)

# ./knx resource
def do_sequence_knx_knx(my_base):

    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.knx", 60)
    content = {"value": { "sia" : 5, "ga": 7, "st": "rp"}}
    execute_post("coap://"+my_base+"/.knx", 60, 60, content)
    execute_get("coap://"+my_base+"/.knx", 60)


def do_sequence_knx_spake(my_base):

    #  url, content, accept, contents
    
    # sequence:
    # - parameter exchange: 15 (rnd)- return value
    # - credential exchange: 10 - return value
    # - pase verification exchange: 14  - no return value
    
    content = { 15: b"a-15-sdfsdred"}
    execute_post("coap://"+my_base+"/.well-known/knx/spake", 60, 60, content)
    
    # pa
    content = { 10: b"s10dfsdfsfs" }
    execute_post("coap://"+my_base+"/.well-known/knx/spake", 60, 60, content)
    
    # ca
    content = { 14: b"a15sdfsdred"}
    execute_post("coap://"+my_base+"/.well-known/knx/spake", 60, 60, content)
    # expecting return 
    

def do_sequence_knx_idevid(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.well-known/knx/idevid", 282)
    
def do_sequence_knx_ldevid(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.well-known/knx/ldevid", 282)


def do_sequence_knx_osn(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.well-known/knx/osn", 60)


def do_sequence_knx_crc(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.well-known/knx/crc", 60)
    
    
def do_sequence_oscore(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/f/oscore", 40)
    
    execute_get("coap://"+my_base+"/p/oscore/replwdo", 60)
    content = 105 
    execute_put("coap://"+my_base+"/p/oscore/replwdo", 60, 60, content)
    execute_get("coap://"+my_base+"/p/oscore/replwdo", 60)
    
    execute_get("coap://"+my_base+"/p/oscore/osndelay", 60)
    content =  1050
    execute_put("coap://"+my_base+"/p/oscore/osndelay", 60, 60, content)
    execute_get("coap://"+my_base+"/p/oscore/osndelay", 60)


def do_sequence_core_knx(my_base):
    #  url, content, accept, contents
    execute_get("coap://"+my_base+"/.well-known/knx", 60)
    content = { 1 : 5, 2: "reset"}
    execute_post("coap://"+my_base+"/.well-known/knx", 60, 60, content)
    
    
def do_sequence_a_sen(my_base):
    #  url, content, accept, contents
    content = {2: "reset"}
    execute_post("coap://"+my_base+"/a/sen", 60, 60, content)
    

def do_sequence(my_base):
    
    do_sequence_a_sen(my_base)
    return
    do_sequence_dev(my_base)
    
    #return
    do_sequence_fp_g_int(my_base)
    #do_sequence_fp_g(my_base)
    
    do_sequence_fp_p_int(my_base)
    #do_sequence_fp_p(my_base)
    
    do_sequence_fp_r_int(my_base)
    #do_sequence_fp_r(my_base)
    
    do_sequence_lsm_int(my_base)
    #do_sequence_lsm(my_base)
    do_sequence_lsm_int(my_base)
    # .knx
    do_sequence_knx_knx_int(my_base)
    #do_sequence_knx_knx(my_base)
    
    do_sequence_knx_spake(my_base)
    do_sequence_knx_idevid(my_base)
    do_sequence_knx_ldevid(my_base)
    do_sequence_knx_crc(my_base)
    do_sequence_knx_osn(my_base)
    
    do_sequence_oscore(my_base)
    do_sequence_core_knx(my_base)
    
        

def client_callback_discovery(response, checkdata=None):
    print(" --- Discovery Callback ---")
    global my_base
    if response is not None:
        print ("response code:",response.code)
        print ("response type:",response.content_type)
        if response.code > 100:
            print("+++returned error+++")
            return
        if response.content_type == defines.Content_types["application/link-format"]:
            print (response.payload.decode())
            my_base = get_base_from_link(response.payload.decode())
            do_sequence(my_base)

def code2string(code):
   if code == 68:
      return "(Changed)"
   if code == 69:
      return "(Content)"
   if code == 132:
      return "(Not Found)"
   if code == 133:
      return "(METHOD_NOT_ALLOWED)"
   if code == 160:
      return "(INTERNAL_SERVER_ERROR)"
   
   return ""


def client_callback(response, checkdata=None):
    print(" --- Callback ---")
    if response is not None:
        print ("response code:",response.code, code2string(response.code))
        print ("response type:",response.content_type)
        if response.code > 100:
            print("+++returned error+++")
            return
        #print(response.pretty_print())
        if response.content_type == defines.Content_types["text/plain"]:
            if response.payload is not None:
              print (type(response.payload), len(response.payload))
              print ("=========")
              print (response.payload)
              print ("=========")
            else: 
                print ("payload: none")
        elif response.content_type == defines.Content_types["application/cbor"]:
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
        else:
            if response.payload is not None:
              print ("type, len", type(response.payload), len(response.payload))
              print (response.payload)
            #else:
            #    print ("    not handled: ", response)
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
      print ("---------------------------")
      print ("execute_del: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = ct_value
      ct['content_type'] = ct_value
      
      if mypath.startswith("coap://") == False:
        print(" not executing: ", mypath);
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

      response = nclient.delete(path, None, None, **ct)
      client_callback(response)
        #nclient.stop()
        #sys.exit(2)
      print ("=======")



def execute_put(mypath, ct_value, accept, content):
      print ("---------------------------")
      print ("execute_put: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = accept
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

      if accept == 60:
        payload = cbor.dumps(content)
      else:
        payload = content
      print ("payload: ", payload)
      response = nclient.put(path, payload, None, None , None, **ct)
      client_callback(response)
      nclient.stop()
      
      
def execute_post(mypath, ct_value, accept, content):
      print ("---------------------------")
      print ("execute_post: ", ct_value, mypath)
      do_exit = False
      ct = {}
      ct['accept'] = accept
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

      if accept == 60:
        payload = cbor.dumps(content)
      else:
        payload = content
      response = nclient.post(path, payload, None, None , None, **ct)
      client_callback(response)
      nclient.stop()


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
                client_callback_discovery(response)
        
        counter = 2
        try:
           while counter > 0:
              time.sleep(1)
              counter = counter - 1
           #client.stop()
        except KeyboardInterrupt:
           print("Client Shutdown")
           #client.stop()
           
        #execute_list()
        client.stop()
    else:
        print("Operation not recognized")
        usage()
        sys.exit(2)


if __name__ == '__main__':  # pragma: no cover
    main()
