.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _`Usage`:

Usage
=====


.. _`Ansible vault file`:

Ansible vault file
------------------

The `Ansible vault file`_ used by the **secureserveraccess** library is in YAML
format and defines the secrets for accessing each server.

The servers are identified with user-defined nicknames, and the data structure
of the secrets is completely user-defined.

Here are some example Ansible vault files that define server secrets using
different data structures.

This example defines the server secrets as host, username and password:

.. code-block:: yaml

    secrets:                              # Fixed key

      myserver1:                          # Nickname of the server
        host: "10.11.12.13"               # User-defined secrets
        username: myusername
        password: mypassword

Here is another example that defines the server secrets as URL and API key
(which is then more a service than a server):

.. code-block:: yaml

    secrets:

      myserver1:                          # Nickname of the server
        url: https://10.11.12.13/myservice
        api_key: mykey


The vault file can be encrypted or decrypted using the `ansible-vault command`_
that is part of `Ansible`_. Ansible can be installed for example as the
``ansible`` package from Pypi.

The vault file can be encrypted or in clear text when the
**secureserveraccess** library functions accessing it are called.
If it is encrypted, its vault password must be provided by the caller.
See :class:`secureserveraccess.VaultFile` for details.

Python programs for direct human use (e.g. command line utilities) can prompt
for the vault password and store it in the keyring facility of the local system
for repetitive use without further prompts.

Python programs that run in a CI system can get the vault password from the
CI system's facility to store secrets.

See :ref:`Securing the vault password` for details about these approaches.


.. _`Accessing the secrets in a program`:

Accessing the secrets in a program
----------------------------------

The following Python code demonstrates the use case of a command line utility
that prompts for the vault password if needed and stores that password in the
keyring facility of the local system for future use, using the
`keyring Python package`_:

.. code-block:: python

    import getpass
    import keyring
    from secureserveraccess import Vault, NotFound

    vault_file = 'vault.yml'        # Path name of Ansible vault file
    server_nick = 'myserver1'       # Nickname of server in Ansible vault file

    keyring_service = 'myprogram'   # Some unique service name within your keyring
    keyring_username = 'vault'

    password = keyring.get_password(keyring_service, keyring_username)
    if password is None:
        password = getpass.getpass("Password for Ansible vault file {fn}:".
                                   format(fn=vault_file))
        keyring.set_password(keyring_service, keyring_username, password)

    # Open the vault and access the entry for a server
    vault = Vault(vault_file, password)
    try:
        vault_server = vault.get_server(server_nick)
    except NotFound as exc:
        # Handle server nickname not found
        . . .

    session = MySession(  # A fictitious session class
      host=vault_server['host'],
      username=vault_server['username'],
      password=vault_server['password'])

    # Do something in the server session
    . . .

The use case where a Python test program using the `pytest Python package`_
needs access to servers is best handled by using the `Pytest fixture`_ provided
by the `pytest-ssa Python package`_.


.. _`Securing the vault password`:

Securing the vault password
---------------------------

TBD


.. _`Server definition file`:

Server definition file
----------------------

The *server definition file* is in YAML format and defines servers, server
groups and a default server or group. The servers and server groups are
identified using user-defined nicknames and the file stores some basic
information about them, without revealing any secrets.

The use of a server definition file is optional. For example, a program that
takes a server nickname as input and only needs to get to the server secrets
does not need a server definition file. However, if the program is designed to
run against the servers in a group, or to list the available servers and
groups, or to provide extra information about the servers, then the server
definition file would be used. At the end of the day, the choice of using
a server definition file is up to the Python program using this library.

Here is an example server definition file. The format of the file has some
predefined fixed data about the servers and groups, and additional user-defined
data for servers and groups.

Here is a complete working example of a server definition file that defines
two servers and one server group:

.. code-block:: yaml

    servers:

      myserver1:                          # Nickname of the server
        description: "my dev system 1"    # Short description of the server
        contact_name: "John Doe"          # Optional: Contact for the server
        access_via: "VPN to dev network"  # Optional: Any special network access needed
        user_defined:                     # Optional: user-defined additional information
          stuff: morestuff

      myserver2:                          # Nickname of the server
        description: "my dev system 2"    # Short description of the server
        contact_name: "John Doe"          # Optional: Contact for the server
        access_via: "Intranet"            # Optional: Any special network access needed
        user_defined:                     # Optional: user-defined additional information
          stuff: morestuff

    server_groups:

      mygroup1:                           # Nickname of the server group
        description: "my dev systems"     # Short description of server group
        members:                          # Group members (servers or groups)
          - myserver1
          - myserver2
        user_defined:                     # Optional: user-defined additional information
          stuff: morestuff

    default: mygroup1                     # Default server or group

In the example above, ``myserver1``, ``myserver2``, and ``mygroup1`` are
nicknames of the respective server or server group definitions. These nicknames
are used when servers or groups are put into a server group in that file, or
when they are specified as a default in that file, or when they are used
in functions of the **secureserveraccess** library.
See :class:`secureserveraccess.ServerDefinitionFile` for details.

These nicknames are case sensitive and their allowable character set are
alphenumeric characters and the underscore character.

The value of the ``servers`` top-level property is an object (=dictionary) that
has one property for each server that is defined. The property name is the
server nickname, and the property value is an object with the following
properties.

* ``description`` (string): Short description of the server (required).
* ``contact_name`` (string): Name of technical contact for the server (optional,
  defaults to `None`).
* ``access_via`` (string): Short reminder on the network/firewall/proxy/vpn
  used to access the server (optional, defaults to `None`).
* ``user_defined`` (object): User-defined details of the server (optional).

The value of the ``server_groups`` top-level property is an object that has one
property for each server group that is defined. The property name is the group
nickname, and the property value is an object with the following properties:

* ``description`` (string): Short description of the server group (required).
* ``members`` (list): List of server nicknames or other group nicknames that
  are the members of the group (required).

The value of the ``default`` top-level property is a string that is the
nickname of the default server or group.

Server groups may be nested. That is, server groups may be put into other server
groups at arbitrary nesting depth. There must not be any cycle (i.e. the
resulting graph of server groups must be a tree).

A particular server or server group may be put into more than one server group.


.. # Links:
.. _`Ansible`: https://www.ansible.com/
.. _`ansible-vault command`: https://docs.ansible.com/ansible/latest/cli/ansible-vault.html
.. _`keyring Python package`: https://pypi.org/project/keyring/
.. _`pytest Python package`: https://pypi.org/project/pytest/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
.. _`pytest-ssa Python package`: https://pypi.org/project/pytest-ssa/
