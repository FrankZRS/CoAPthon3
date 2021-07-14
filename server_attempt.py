#!/usr/bin/env python

from ocfserver import *

def main(argv):
    ip = "fd79:8ae:665:1:7ca9:e760:bb4b:f3ea"
    port = 12345
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

if __name__ == "__main__":
    main(sys.argv[1:])