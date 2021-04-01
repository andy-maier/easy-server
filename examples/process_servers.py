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

    if len(sys.argv) < 4:
        print("Usage: {} VAULTFILE SRVDEFFILE NICKNAME".format(sys.argv[0]))
        sys.exit(2)

    vault_file = sys.argv[1]
    server_file = sys.argv[2]
    nickname = sys.argv[3]

    try:
        sdf = easy_server.ServerFile(server_file)
    except easy_server.ServerFileException as exc:
        print("Error: {}".format(exc))
        return 1

    try:
        vault = easy_server.VaultFile(vault_file)
    except easy_server.VaultFileException as exc:
        print("Error: {}".format(exc))
        return 1

    sd_list = sdf.list_servers(nickname)

    for sd in sd_list:
        nick = sd.nickname
        secrets = vault.get_secrets(nick)

        host=secrets['host'],
        username=secrets['username']
        password=secrets['password']

        print("Server {n}: host={h}, username={u}, password=********".
              format(n=nick, h=host, u=username))

    return 0


if __name__ == '__main__':
    sys.exit(main())
