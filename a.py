import socket
import struct

hop_limit = 11
msg = b"test"
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

s.sendmsg([msg],
    [(socket.IPPROTO_IPV6, socket.IPV6_HOPLIMIT, struct.pack("i",hop_limit))],
    0, ('::1',1234))