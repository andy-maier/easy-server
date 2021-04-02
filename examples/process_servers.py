#!/usr/bin/env python
"""
Example script that processes the servers of a server or group nickname.
"""

import sys
import os
from pprint import pprint
import easy_server


def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("Usage: {} SERVERFILE [NICKNAME]".format(sys.argv[0]))
        sys.exit(2)

    server_file = sys.argv[1]
    if len(sys.argv) > 2:
        nickname = sys.argv[2]
    else:
        nickname = None

    try:
        esf_obj = easy_server.ServerFile(server_file)
    except easy_server.ServerFileException as exc:
        print("Error: {}".format(exc))
        return 1

    if nickname:
        es_list = esf_obj.list_servers(nickname)
    else:
        es_list = esf_obj.list_default_servers()

    for es in es_list:
        nickname = es.nickname
        host = es.secrets['host'],
        username = es.secrets['username']
        password = es.secrets['password']

        print("Server {n}: host={h}, username={u}, password=********".
              format(n=nickname, h=host, u=username))

    return 0


if __name__ == '__main__':
    sys.exit(main())
