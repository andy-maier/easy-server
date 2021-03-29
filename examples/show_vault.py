#!/usr/bin/env python
"""
Example script that shows the content of a vault file.
"""

import sys
import os
from pprint import pprint
import easy_vault

from secure_server_access import VaultFile, VaultFileException


def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("Usage: {} VAULTFILE".format(sys.argv[0]))
        sys.exit(2)

    vault_file = sys.argv[1]

    try:
        vault = VaultFile(vault_file)
    except VaultFileException as exc:
        print("Error: {}".format(exc))
        return 1

    for nick in vault.nicknames:
        print("Secrets for nickname {}:".format(nick))
        pprint(vault.get_secrets(nick))

    return 0


if __name__ == '__main__':
    sys.exit(main())
