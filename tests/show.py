#!/usr/bin/env python
"""
Test script that shows the content of a vault file.
"""

import sys
import getpass
import keyring
from secureserveraccess import VaultFile, VaultFileException


def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("Usage: {} vaultfile [password]".format(sys.argv[0]))
        sys.exit(2)

    vault_file = sys.argv[1]
    try:
        password = sys.argv[2]
    except IndexError:
        password = None

    keyring_service = 'secureserveraccess.show'    # unique within keyring
    keyring_username = 'vault'

    if password is None:
        password = keyring.get_password(keyring_service, keyring_username)
        if password is None:
            password = getpass.getpass("Password for Ansible vault file {fn}:".
                                       format(fn=vault_file))
            print("Setting password for vault file in keyring")
            keyring.set_password(keyring_service, keyring_username, password)
        else:
            print("Using password for vault file from keyring")
    else:
        print("Setting password for vault file in keyring")
        keyring.set_password(keyring_service, keyring_username, password)

    try:
        vault = VaultFile(vault_file, password)
    except VaultFileException as exc:
        print("Error: {}".format(exc))
        return 1

    print("vault.nicknames (type {}): {}".
          format(type(vault.nicknames), vault.nicknames))

    for nick in vault.nicknames:
        print("Secrets for nickname {}:".format(nick))
        print(vault.get_secrets(nick))

    return 0


if __name__ == '__main__':
    sys.exit(main())
