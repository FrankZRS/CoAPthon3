# notes


## discovery

### ietf well-known/core discovery

using [FF05::FD] (site local)

python coapclient.py -o DISCOVER -p coap://[FF05::FD]:5683/.well-known/core?rt=oic.wk.res -c 40

using [FF02::FD] (link local)

python coapclient.py -o DISCOVER -p coap://[FF02::FD]:5683/.well-known/core?rt=oic.wk.res -c 40


using ALL OCF (site local): 

python coapclient.py -o DISCOVER -p coap://[FF05::158]:5683/.well-known/core?rt=oic.wk.res -c 40



### ocf discovery

using [FF05::158] (site local)

python coapclient.py -o DISCOVER -p coap://[FF05::158]:5683/oic/res -c 10000

