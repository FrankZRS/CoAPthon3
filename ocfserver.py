#############################
#
#    copyright 2020 Open Interconnect Consortium, Inc. All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification,
#    are permitted provided that the following conditions are met:
#    1.  Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright notice,
#        this list of conditions and the following disclaimer in the documentation and/or other materials provided
#        with the distribution.
#         
#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR
#    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#############################
# tool_version          : 20200103
# input_file            : ../device_output/out_codegeneration_merged.swagger.json
# version of input_file : 20190222
# title of input_file   : server_lite_14808

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from coapthon import defines
import getopt
import sys
import cbor
#import jsonschema
import json
import socket

ocf_piid="e61c3e6b-9c54-4b81-8ce5-f9039c1d04d9"
ocf_pi="e61c3e6b-9c54-4b81-8ce5-f9039c1d04d8"
ocf_di="e61c3e6b-9c54-4b81-8ce5-f9039c1d04d8"
global ocf_ip_address
ocf_ip_address=""
ocf_device_type="oic.d.light"
introspectionfile_json="../out_introspection_merged.swagger.json"
introspectionfile_cbor="../out_introspection_merged.swagger.json.cbor"

def bool2string(input):
    if input == True:
        return "true"
    return "false"



# class : "/activity"
class c_activityResource(Resource):
    def __init__(self, name="c_activityResource", coap_server=None):
        super(c_activityResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.payload = ""
        self.resource_type = "oic.r.activity"
        self.content_type = "application/vnd.ocf+cbor"
        interfaces_array = ['oic.if.a', 'oic.if.baseline']
        self.interface_type =  str(interfaces_array[0]) + "," + str(interfaces_array[1])
        self.m_activity = "mystring"  # string
        self.m_ccal_day = 0.0  # number
        self.m_ccal_day_precision = 0.0  # number
        self.m_ccal_day_range = "unknown"  # something else
        self.m_ccal_day_step = 0.0  # number
        self.m_ccal_reset = 0.0  # number
        self.m_ccal_reset_precision = 0.0  # number
        self.m_ccal_reset_range = "unknown"  # something else
        self.m_ccal_reset_step = 0.0  # number
        self.m_steps_day = 0  # integer
        self.m_steps_day_range = "unknown"  # something else
        self.m_steps_day_step = 0  # integer
        self.m_steps_reset = 0  # integer
        self.m_steps_reset_range = "unknown"  # something else
        self.m_steps_reset_step = 0  # integer 
    def create_return_json(self):
        return_json = "{"
        
        return_json = return_json + '"activity" : "' + str(self.m_activity) + '"' + ','
        
        return_json = return_json + '"ccal_day" : ' + str(self.m_ccal_day) + ','
        
        return_json = return_json + '"ccal_day_precision" : ' + str(self.m_ccal_day_precision) + ','
        
        return_json = return_json + '"ccal_day_range" : ' + str(self.m_ccal_day_range) + ','
        
        return_json = return_json + '"ccal_day_step" : ' + str(self.m_ccal_day_step) + ','
        
        return_json = return_json + '"ccal_reset" : ' + str(self.m_ccal_reset) + ','
        
        return_json = return_json + '"ccal_reset_precision" : ' + str(self.m_ccal_reset_precision) + ','
        
        return_json = return_json + '"ccal_reset_range" : ' + str(self.m_ccal_reset_range) + ','
        
        return_json = return_json + '"ccal_reset_step" : ' + str(self.m_ccal_reset_step) + ','
        
        return_json = return_json + '"steps_day" : ' + str(self.m_steps_day) + ','
        
        return_json = return_json + '"steps_day_range" : ' + str(self.m_steps_day_range) + ','
        
        return_json = return_json + '"steps_day_step" : ' + str(self.m_steps_day_step) + ','
        
        return_json = return_json + '"steps_reset" : ' + str(self.m_steps_reset) + ','
        
        return_json = return_json + '"steps_reset_range" : ' + str(self.m_steps_reset_range) + ','
        
        return_json = return_json + '"steps_reset_step" : ' + str(self.m_steps_reset_step) 
        return_json = return_json + " }"
        return return_json

    def render_GET_advanced(self, request, response):
        print ("GET /activity :", request.accept)
        return_json = self.create_return_json()
        print ("  ",return_json)
        json_data = json.loads(return_json)
        self.payload = str(return_json)
        print ("/activity : get query: ", request.uri_query)
        print ("/activity : get returning: ", return_json)
        response.code = defines.Codes.CONTENT.number
        response.content_type = request.accept
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            response.payload = bytes(cbor.dumps(json_data))
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            response.payload = bytes(cbor.dumps(json_data))
            response.ocf_content_format_version = int(2048)
        return self, response

# class : "/binaryswitch2"
class c_binaryswitch2Resource(Resource):
    def __init__(self, name="c_binaryswitch2Resource", coap_server=None):
        super(c_binaryswitch2Resource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.payload = ""
        self.resource_type = "oic.r.switch.binary"
        self.content_type = "application/vnd.ocf+cbor"
        interfaces_array = ['oic.if.a', 'oic.if.baseline']
        self.interface_type =  str(interfaces_array[0]) + "," + str(interfaces_array[1])
        self.m_value = True   # boolean 
    def create_return_json(self):
        return_json = "{"
        
        return_json = return_json + '"value" : ' + bool2string(self.m_value) 
        return_json = return_json + " }"
        return return_json

    def render_GET_advanced(self, request, response):
        print ("GET /binaryswitch2 :", request.accept)
        return_json = self.create_return_json()
        print ("  ",return_json)
        json_data = json.loads(return_json)
        self.payload = str(return_json)
        print ("/binaryswitch2 : get query: ", request.uri_query)
        print ("/binaryswitch2 : get returning: ", return_json)
        response.code = defines.Codes.CONTENT.number
        response.content_type = request.accept
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            response.payload = bytes(cbor.dumps(json_data))
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            response.payload = bytes(cbor.dumps(json_data))
            response.ocf_content_format_version = int(2048)
        return self, response 
    def render_POST(self, request):
        print ("POST /binaryswitch2:", request.accept)
        if len(request.payload) > 0:
            if request.accept == defines.Content_types["application/json"]:
                print ("  JSON")
                json_data = json.loads(request.payload)
                #json_string = json.dumps(json_data, indent=2, sort_keys=True)
                print ("  assigning self.m_value :", json_data["value"])
                self.m_value = json_data["value"]               
                self.edit_resource(request)
                self.payload = (defines.Content_types["application/json"], self.create_return_json())
                return self
            if request.accept == defines.Content_types["application/cbor"]:
                print ("  CBOR")
                json_data = cbor.loads(request.payload)
                print (json_data)
                print ("  assigning self.m_value :", json_data["value"])
                self.m_value = json_data["value"]               
                self.edit_resource(request)
                ret_json_string = self.create_return_json()
                json_data = json.loads(ret_json_string)
                self.payload = (defines.Content_types["application/json"], bytes(cbor.dumps(json_data)))
                return self
            if request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
                print ("  OCF-CBOR")
                json_data = cbor.loads(request.payload)
                print ("  assigning self.m_value :", json_data["value"])
                self.m_value = json_data["value"]               
                self.edit_resource(request)
                ret_json_string = self.create_return_json()
                json_data = json.loads(ret_json_string)
                self.payload = (defines.Content_types["application/vnd.ocf+cbor"], bytes(cbor.dumps(json_data)))
                return self
        return None 

#
# the oic.wk.res implementation
#
class OICRESResource(Resource):
    def __init__(self, name="OICRESResource", coap_server=None):
        super(OICRESResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = "oic.wk.res oic.d.light"
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.ll oic.if.baseline"

    def render_GET_advanced(self, request, response):
        print ("OICRES: get :", request.accept )
        
        all_queries = request.uri_query
        print ("OICRES: queries:",all_queries)
        return_json = ""
        
        if all_queries == "if=oic.if.baseline":
            return_json = return_json + '[{ "rt": ["oic.wk.res"], '
            return_json = return_json + '"if": ["oic.if.ll", "oic.if.baseline"],'
            return_json = return_json + '"links":'
        ## oic.if.ll 
        return_json = return_json + '[ { "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/res", "rel": "self",'
        return_json = return_json + '"rt": ["oic.wk.res"], "if": ["oic.if.ll", "oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/d",'
        return_json = return_json + ' "rt": ["oic.wk.d"], "if": ["oic.if.r", "oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'

        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/p",'
        return_json = return_json + ' "rt": ["oic.wk.p"], "if": ["oic.if.r", "oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        
        ## introspection
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/introspection",'
        return_json = return_json + ' "rt": ["oic.wk.introspection"], "if": ["oic.if.r", "oic.if.baseline"], "p": {"bm": 1},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        
        # security
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/sec/doxm",'
        return_json = return_json + ' "rt": ["oic.r.doxm"], "if": ["oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"}, {"ep": "coaps://'+ocf_ip_address+'"} ] }'

        # /oic/sec/pstat
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/sec/pstat",'
        return_json = return_json + ' "rt": ["oic.r.pstat"], "if": ["oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        # /oic/sec/cred
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/sec/cred",'
        return_json = return_json + ' "rt": ["oic.r.cred"], "if": ["oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        # /oic/sec/csr
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/oic/sec/csr",'
        return_json = return_json + ' "rt": ["oic.r.csr"], "if": ["oic.if.baseline"], "p": {"bm": 3},'
        return_json = return_json + ' "eps": [ {"ep": "coap://'+ocf_ip_address+'"},{"ep": "coaps://'+ocf_ip_address+'"} ] }'
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/activity",'
        return_json = return_json + ' "rt": ["oic.r.activity"],"if":' + '["oic.if.a", "oic.if.baseline"],'
        return_json = return_json + ' "p": {"bm": 3}, "eps": [ {"ep": "coap://'+ocf_ip_address+'"}, {"ep": "coaps://'+ocf_ip_address+'"}]}'
        return_json = return_json + ',{ "anchor": "ocf://'+ocf_piid+ '", "href": "/binaryswitch2",'
        return_json = return_json + ' "rt": ["oic.r.switch.binary"],"if":' + '["oic.if.a", "oic.if.baseline"],'
        return_json = return_json + ' "p": {"bm": 3}, "eps": [ {"ep": "coap://'+ocf_ip_address+'"}, {"ep": "coaps://'+ocf_ip_address+'"}]}' 
        return_json = return_json + " ]"
        
        if all_queries == "if=oic.if.baseline":
            return_json = return_json + '}]'
        
        json_data = json.loads(return_json)
        self.payload = str(return_json)
        print ("   return :")
        print (return_json)
        response.code = defines.Codes.CONTENT.number
        response.content_type = request.accept 
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            response.payload =  bytes(cbor.dumps(json_data))
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            response.payload = bytes(cbor.dumps(json_data))
            response.ocf_content_format_version = int(2048)
        
        return self, response
        
#
# the /oic path implementation
# needs to be there, otherwise the childeren are not hosted
# code returns not implemented.       
class OICResource(Resource):
    def __init__(self, name="OICResource", coap_server=None):
        super(OICResource, self).__init__(name, coap_server, visible=False,
                                             observable=False, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = ""
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.r" #, "oic.if.baseline"

    def render_GET_advanced(self, request, response):
        print ("OICResource: get :", request.accept )
        response.code = defines.Codes.NOT_FOUND.number
        return self, response

#
# the /oic/sec path implementation
# needs to be there, otherwise the childeren are not hosted
# code returns not implemented.       
class OICSECResource(Resource):
    def __init__(self, name="OICSECResource", coap_server=None):
        super(OICSECResource, self).__init__(name, coap_server, visible=False,
                                             observable=False, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = ""
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.r" #, "oic.if.baseline"

    def render_GET_advanced(self, request, response):
        print ("OICSECResource: get :", request.accept )
        response.code = defines.Codes.NOT_FOUND.number
        return self, response

        
#
# the oic.wk.d implementation
#        
class OICDResource(Resource):
    def __init__(self, name="OICDResource", coap_server=None):
        global ocf_device_type
        super(OICDResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = "oic.wk.d oic.d.light"
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.r oic.if.baseline" #, "oic.if.baseline"

    def render_GET_advanced(self, request, response):
        global ocf_device_type
        print ("OICDRES: get :", request.accept )
        
        return_json = ""
        all_queries = request.uri_query
        print ("OICD: queries:", all_queries)
        
        return_json = return_json +  '{ "n": "server_lite_14808",'
        if all_queries == "if=oic.if.baseline":
            return_json = return_json + '"rt": ["oic.wk.d","oic.d.light"],'
            return_json = return_json + '"if": ["oic.if.r", "oic.if.baseline"],'
        return_json = return_json + '"icv": "ocf.2.0.2", '
        return_json = return_json + '"dmv": "ocf.res.1.0.0, ocf.sh.1.0.0",'
        return_json = return_json + '"piid": "'+ocf_piid+'",'
        return_json = return_json + '"di": "'+ocf_di+'"' 
        return_json = return_json + " }"
        
        json_data = json.loads(return_json)
        #self.payload = str(return_json)
        response.content_type = request.accept 
        response.code = defines.Codes.CONTENT.number
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
            response.ocf_content_format_version = int(2048)
            
        return self, response
        
                
#
# the oic.wk.p implementation
#        
class OICPResource(Resource):
    def __init__(self, name="OICPResource", coap_server=None):
        super(OICPResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = "oic.wk.p"
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.r" #, "oic.if.baseline"

    def render_GET_advanced(self, request, response):
        print ("OICP: get :", request.accept )

        all_queries = request.uri_query 
        print ("OICP: queries:", all_queries)
        
        return_json = '{ '
        if all_queries == "if=oic.if.baseline":
            return_json = return_json + '"rt": ["oic.wk.p"],'
            return_json = return_json + '"if": ["oic.if.r", "oic.if.baseline"],'
        return_json = return_json + '"mnmn": "OCF",'
        return_json = return_json + '"pi": "'+ocf_pi+'"' 
        return_json = return_json + " }"
        
        json_data = json.loads(return_json)
        self.payload = str(return_json)
        response.content_type = request.accept 
        response.code = defines.Codes.CONTENT.number
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
            response.ocf_content_format_version = int(2048)
        return self, response
     
#
# the oic.wk.introspection implementation
#        
class introspectionResource(Resource):
    def __init__(self, name="introspectionResource", coap_server=None):
        super(introspectionResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=False)
        self.value = { "rt": ["oic.wk.introspection"], 
                       "if": ["oic.if.r", "oic.if.baseline"], 
                       "urlInfo": [ { "content-type": "application/json", "protocol": "coap", "url": "/ifile"},
                       { "content-type": "application/cbor", "protocol": "coap", "url": "/ifile"}] }
        self.payload = str(self.value)
        self.resource_type = "oic.wk.introspection"
        self.content_type = "application/vnd.ocf+cbor"
        self.interface_type = "oic.if.r"

    def render_GET_advanced(self, request, response):
        print (" /introspection get ")
        json_data = self.value
        self.payload = str(self.value)
        response.content_type = request.accept 
        response.code = defines.Codes.CONTENT.number
        if request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            return_json = json.dumps(json_data, indent=2, sort_keys=True)
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
            response.ocf_content_format_version = int(2048)
        return self, response

#
# the oic.wk.introspection file read implementation
# 
class introspectionFileResource(Resource):
    def __init__(self, name="introspectionFileResource", coap_server=None):
        super(introspectionFileResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=False)
        self.payload = " illegal "
        self.resource_type = "oic.wk.introspection"
        self.content_type = "application/vnd.ocf+cbor"
        self.interface_type = "oic.if.r"

    def render_GET(self, request):
        print (" introspection file get ", request.accept)
        if request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            data = " empty "
            print ("  reading file:",introspectionfile_json)
            with open(introspectionfile_json, 'rb') as f:
                data = f.read()
            self.payload = (defines.Content_types["application/json"], data)
        elif request.accept == defines.Content_types["application/cbor"]:
            cbordata = " empty "
            print ("  reading file:",introspectionfile_cbor)
            with open(introspectionfile_cbor, 'rb') as f:
                cbordata = f.read()
            self.payload = (defines.Content_types["application/cbor"], bytes(cbordata))
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            cbordata = " empty "
            print ("  reading file:",introspectionfile_cbor)
            with open(introspectionfile_cbor, 'rb') as f:
                cbordata = f.read()
            self.payload = (defines.Content_types["application/vnd.ocf+cbor"], bytes(cbordata))
        return self
     
                
#
# the oic.r.doxm implementation
#        
class OICDOXMResource(Resource):
    def __init__(self, name="OICDOXMResource", coap_server=None):
        super(OICDOXMResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=True)
        self.value = 0
        self.payload = str(self.value)
        self.resource_type = "oic.r.doxm"
        self.content_type = "application/vnd.ocf+cbor"  #application/cbor
        self.interface_type = "oic.if.rw" #, "oic.if.baseline"

    def render_GET_advanced(self, request, response):
        print ("OICDOXMResource: get :", request.accept )
        return_json = '{ "rt": ["oic.r.doxm"],'
        return_json = return_json + '"if": [ "oic.if.baseline"],'
        return_json = return_json + '"oxms": [0,1,2],'
        return_json = return_json + '"oxmsel": 0,'
        return_json = return_json + '"sct": 9,'
        return_json = return_json + '"owned": false,' 
        return_json = return_json + '"deviceuuid": "'+ocf_pi+'",' 
        return_json = return_json + '"devowneruuid": "'+ocf_pi+'",' 
        return_json = return_json + '"rowneruuid": "'+ocf_pi+'"' 
        return_json = return_json + " }"
        
        json_data = json.loads(return_json)
        self.payload = str(return_json)
        response.content_type = request.accept 
        response.code = defines.Codes.CONTENT.number
        if request.accept == defines.Content_types["text/plain"]:
            print ("  content type text/plain")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/json"]:
            print ("  content type application/json")
            response.payload = return_json
        elif request.accept == defines.Content_types["application/cbor"]:
            print ("  content type application/cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
        elif request.accept == defines.Content_types["application/vnd.ocf+cbor"]:
            print ("  content type application/vnd.ocf+cbor")
            cbordata = cbor.dumps(json_data)
            print ("cbor :",cbordata)
            response.payload = bytes(cbordata)
            response.ocf_content_format_version = int(2048)
        return self, response
     
     
class wellknownResource(Resource):
    def __init__(self, name="wellknownResource", coap_server=None):
        super(wellknownResource, self).__init__(name, coap_server, visible=True,
                                             observable=True, allow_children=False)
        self.value = '</oic/res>;ct=60;rt="oic.wk.res";if="oic.if.r";et="oic.d.light"; base="coap://'+ocf_ip_address+'";rel="hosts"'

        self.payload = str(self.value)
        self.resource_type = "oic.wk.res"
        self.content_type = "application/link-format"
        self.interface_type = "oic.if.r"

    def render_GET(self, request):
        self.payload = str(self.value)
        return self

class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=True):
        global ocf_ip_address
        CoAP.__init__(self, (host, port), multicast)
        print(" CoAP Server init:")
        
        print("  adding resource: '/oic/'")
        self.add_resource('/oic/', OICResource())
        print("  adding resource: '/oic/res/'")
        self.add_resource('/oic/res/', OICRESResource())
        print("  adding resource: '/oic/d'")
        self.add_resource('/oic/d/', OICDResource())
        print("  adding resource: '/oic/p'")
        self.add_resource('/oic/p/', OICPResource())
        
        print("  adding resource: '/ifile' (introspection file)")
        self.add_resource('/ifile', introspectionFileResource())
        print("  adding resource: '/introspection' (introspection resource)")
        self.add_resource('/introspection', introspectionResource())
        
        print("  adding resource: '/oic/sec'")
        self.add_resource('/oic/sec', OICSECResource())
        
        print("  adding resource: '/oic/sec/doxm'")
        self.add_resource('/oic/sec/doxm', OICDOXMResource())
        

        self.add_resource('/activity/', c_activityResource())
        print("  adding resource: '/activity/'")

        self.add_resource('/binaryswitch2/', c_binaryswitch2Resource())
        print("  adding resource: '/binaryswitch2/'")
 
        #print("  start on " + host + ":" + str(port))
        #ocf_ip_address = "["+ str(host) + "]:" + str(port)
        
        # CTT can't handle zone ID
        # e.g. remove %13 from {"ep":"coaps://[fe80::b536:6766:9ed9:15a4%13]:55555"}
        my_host = host.replace("%13","")
        ocf_ip_address = "["+ str(my_host) + "]:" + str(port)
        
        self.ocf_ip_address = ocf_ip_address
        print("  start on (ip): coap://"+ocf_ip_address)
        #print(" python3 coapclient.py -o GET -p "coap://[fe80::b536:6766:9ed9:15a4%13]:55555/oic/d?if=oic.if.baseline -c 10000
        print ("dump:")
        print(self.root.dump())

def usage():  # pragma: no cover
    print("ocfserver.py -i <ip address> -p <port> -m")
    
def main(argv):  # pragma: no cover
    ip = "127.0.0.1" # local ipv4
    ip = "::1"       # local ipv6
    host_name = socket.gethostname() 
    #ip = socket.gethostbyname(host_name) # local ipv4
    data = socket.getaddrinfo(host_name, None, socket.AF_INET6)
    ip = "fd79:8ae:665:1:7ca9:e760:bb4b:f3ea"
    port = 32000
    multicast = True
    
    try:
        opts, args = getopt.getopt(argv, "hi:p:m", ["ip=", "port=", "multicast"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-m", "--multicast"):
            multicast = True

    print("------------------------------------")
    print("Used input file : \"../device_output/out_codegeneration_merged.swagger.json\"")
    print("OCF Server name : \"server_lite_14808\"")
    print("OCF Device Type : \"oic.d.light\"")
    print("OCF piid        : ", ocf_piid)
    print("OCF pi          : ", ocf_pi)
    print("------------------------------------\n")

    server = CoAPServer(ip, port, multicast)
    print("Waiting on incoming connections.. " )
    try:
        server.listen(5)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
