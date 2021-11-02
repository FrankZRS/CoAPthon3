#!/bin/bash
set -x #echo on

#  CBOR = 60
# JSON = 50
# LF = 40


# rt filtering
python3 knx-test.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=urn:knx:dpa.* -c 40

# rt filtering
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=urn:knx:dpa.* -c 40
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=urn:knx:dpa.353* -c 40
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=urn:knx:dpa.352* -c 40

# ia filtering
# next one should not return... so don't run this one in the script
# python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:ia.0 -c 50

python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:ia.5 -c 50

# interface filtering
# urn:knx:pm
# if=urn:knx:ia.<Individual Address>
# { “<Individual Address>” }
# GET coap://<ip unicast>/.well-known/core?if=urn:knx:if.o
# programming mode
#GET coap://[FF03::FD]/.well-known/core?ep=urn:knx:*&if=urn:knx:if.pm
# <>; ep="urn:knx:sn.12345678"
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.* -c 40
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.s -c 40
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.a -c 40

# programming mode filtering.
# works only when the device is in programming mode. returns line with serial number
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.pm -c 40

## data point (rt) filtering
python3 knxcoapclient.py -o DISCOVER -p "coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.a&rt=urn:knx:dpa.353*" -c 40
python3 knxcoapclient.py -o DISCOVER -p "coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if.s&rt=urn:knx:dpa.352*" -c 40

# ep filtering
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?ep=urn:knx:sn.* -c 40
python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?ep=urn:knx:sn.012346 -c 40



#python3 knxcoapclient.py -o GET -p coap://[fe80::6513:3050:71a7:5b98]:62414/a?if=if.a -c 50
#coaps://[fe80::6513:3050:71a7:5b98]:49272

# ource: ('fe80::6513:3050:71a7:5b98', 62940)
#python3 knxcoapclient.py -o GET -p coap://[fe80::6513:3050:71a7:5b98]:64099/b -c 50
#python3 knxcoapclient.py -o GET -p coap://[fe80::6513:3050:71a7:5b98]:64099/.well-known/knx -c 40
#python3 knxcoapclient.py -o GET -p coap://[fe80::6513:3050:71a7:5b98]:62920/dev -c 40

