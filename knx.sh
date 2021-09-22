#!/bin/bash
set -x #echo on

python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=urn:knx:dpa:* -c 40

python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?if=urn:knx:if:* -c 40

python3 knxcoapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?ep=urn:knx:sn:* -c 40

