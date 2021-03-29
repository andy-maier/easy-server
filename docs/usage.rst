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


.. _`Supported environments`:

Supported environments
----------------------

The **secure-server-access** package is supported in these environments:

* Operating Systems: Linux, macOS / OS-X, native Windows, Linux subsystem in
  Windows, UNIX-like environments in Windows.

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

The following command installs the **secure-server-access** package and its
prerequisite packages into the active Python environment:

.. code-block:: bash

    $ pip install secure-server-access


.. _`Server definition file`:

Server definition file
----------------------

The *server definition file* is the open part of the server definitions
that are used. It is in YAML format and defines servers, server
groups and a default server or group. The servers and server groups are
identified using user-defined nicknames and the file stores some basic
information about them.

The secrets for accessing the servers are not defined in this file but
in the :ref:`vault file`. The match between items in these two files is done
by means of the user-defined nicknames of the servers.

Here is an example server definition file. The format of the file has some
predefined fixed data about the servers and groups, and additional user-defined
data for servers and groups.

Here is a complete working example of a server definition file that defines
two servers and one server group:

.. code-block:: yaml

    servers:                              # Fixed top-level key

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

    server_groups:                        # Fixed top-level key

      mygroup1:                           # Nickname of the server group
        description: "my dev systems"     # Short description of server group
        members:                          # Group members (servers or groups)
          - myserver1
          - myserver2
        user_defined:                     # Optional: user-defined additional information
          stuff: morestuff

    default: mygroup1                     # Fixed top-level key: default server or group

In the example above, ``myserver1``, ``myserver2``, and ``mygroup1`` are
nicknames of the respective server or server group definitions. These nicknames
are used when servers or groups are put into a server group in that file, or
when they are specified as a default in that file, or when they are used
in functions of the **secure-server-access** library.
See :class:`secure_server_access.ServerDefinitionFile` for details.

These nicknames are case sensitive and their allowable character set are
alphenumeric characters and the underscore character, i.e. ``A-Z``, ``a-z``,
``0-9``, and ``_``.

The value of the ``servers`` top-level property is an object (=dictionary) that
has one property for each server that is defined. The property name is the
server nickname, and the property value is an object with the following
properties:

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


.. _`Vault file`:

Vault file
----------

The vault file is the protected part of the server definitions that are used.
It is in YAML format and defines the secrets for each server. The servers are
identified using the user-defined nicknames from the server definition file.

Here is a complete working example of a server definition file that defines
the secrets for the two servers from the example server definition file
shown in the previous section:

.. code-block:: yaml

    secrets:                                # Fixed top-level key

      myserver1:                            # Nickname of the server
        # User-defined properties:
        host: "10.11.12.13"
        username: myuser1
        password: mypass1

      myserver2:                            # Nickname of the server
        # User-defined properties:
        host: "9.10.11.12"
        username: myuser2
        password: mypass2

The vault file must have one top-level property named ``secrets``. Below
that are properties that represent the servers (or services).

The server items are identified by nicknames (``myserver1`` and ``myserver2``
in the example above) and can have an arbitrary user-defined set of properties
(``host``, ``username`` and ``password`` in the example above). The properties
may be of arbitrary types, i.e. you can build substructures as you see fit.

Here is another example that defines the server secrets as URL and API key
(which is then more a service than a server):

.. code-block:: yaml

    secrets:                                # Fixed key

      myserver1:                            # Nickname of the server
        # User-defined properties:
        url: https://10.11.12.13/myservice
        api_key: mykey1

      myserver2:                            # Nickname of the server
        # User-defined properties:
        url: https://9.10.11.12/myservice
        api_key: mykey2

Because the server definition file has user-defined properties for each
server entry, and the structure of the server entries in the vault file
is user-defined, there is a choice of which information is put into which
file. For example, the host property from the previous examples could have
been moved into the server definition file as a user-defined property,
since usually it is not really a secret.

The vault file can be encrypted or decrypted using the ``easy-vault`` command
that is part of the
`easy-vault package <https://easy-vault.readthedocs.io/en/latest/>`_

The vault file can be in the encrypted state or in clear text when the
**secure-server-access** library functions are accessing it. It is recommended
to always have it in the encrypted state and to decrypt it only for the period
of time while it is edited.


.. _`Example usage`:

Example usage
-------------

This section describes how a program would use the example server definition
file and vault file from the previous sections to get to all the information
that is needed to access the server.

.. code-block:: python

    from secure_server_access import VaultFile, VaultFileException, \
        ServerDefinitionFile, ServerDefinitionFileException

    # Some parameters that typically would be inout to the program:
    vault_file = 'examples/vault.yml'        # Path name of vault file
    srvdef_file = 'examples/srvdef.yml'      # Path name of server definition file
    nickname = 'mygroup1'                    # Nickname of server or group

    try:
        sdf = ServerDefinitionFile(srvdef_file)
    except ServerDefinitionFileException as exc:
        print("Error: {}".format(exc))
        return 1

    sd_list = sdf.list_servers(nickname)

    try:
        vault = VaultFile(vault_file)
    except VaultFileException as exc:
        print("Error: {}".format(exc))
        return 1

    for sd in sd_list:
        nick = sd.nickname
        secrets = vault.get_secrets(nick)

        host=secrets['host'],
        username=secrets['username']
        password=secrets['password']

        print("Server {n}: host={h}, username={u}, password=********".
              format(n=nick, h=host, u=username))

        # A fictitious session class
        session = MySession(host, username, password)
        . . .

The use case where a Python test program using the `pytest Python package`_
needs access to servers is best handled by using the `Pytest fixture`_ provided
by the `pytest-ssa Python package`_.


.. _`Securing the vault password`:

Securing the vault password
---------------------------

TBD


.. # Links:
.. _`Ansible`: https://www.ansible.com/
.. _`ansible-vault command`: https://docs.ansible.com/ansible/latest/cli/ansible-vault.html
.. _`keyring Python package`: https://pypi.org/project/keyring/
.. _`pytest Python package`: https://pypi.org/project/pytest/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
.. _`pytest-ssa Python package`: https://pypi.org/project/pytest-ssa/
