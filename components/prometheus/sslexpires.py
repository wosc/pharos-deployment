#!/usr/bin/env python

import socket
import ssl
import sys

host = sys.argv[1]
SSL = ssl.create_default_context()
try:
    with socket.create_connection((host, 443)) as tcp_socket:
        with SSL.wrap_socket(tcp_socket, server_hostname=host) as ssl_socket:
            cert = ssl_socket.getpeercert()
            print(str(ssl.cert_time_to_seconds(cert['notAfter'])))
except Exception:
    print('0')
