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

The **easy-server** package is supported in these environments:

* Operating Systems: Linux, macOS / OS-X, native Windows, Linux subsystem in
  Windows, UNIX-like environments in Windows.

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

The following command installs the **easy-server** package and its
prerequisite packages into the active Python environment:

.. code-block:: bash

    $ pip install easy-server


.. _`Server files`:

Server files
-----------------------

A *server file* contains the openly accessible portion of the servers and
optionally references a :ref:`vault file <vault files>` that specifies the
secret portion of the servers.

The server file must be in YAML syntax and must follow the rules
described in this section.

The server file defines servers, server groups and a default server or group.
The servers and server groups are identified using user-defined nicknames and
the server file stores some basic information about them.

The vault file is optional and its path name is specified with a property in
the server file. Corresponding server items in these two files have the same
nicknames. See :ref:`Vault files` for details.

Here is an example server file that defines two servers and one server group,
and additional user-defined properties named 'stuff':

.. code-block:: yaml

    vault_file: vault.yml                 # Relative to directory of this file

    servers:                              # Fixed top-level key

      myserver1:                          # Nickname of the server
        description: "my dev system 1"    # Short description of the server
        contact_name: "John Doe"          # Optional: Contact for the server
        access_via: "VPN to dev network"  # Optional: Any special network access needed
        user_defined:                     # Optional: User-defined additional information
          # User-defined properties:
          stuff: morestuff

      myserver2:                          # Nickname of the server
        description: "my dev system 2"    # Short description of the server
        contact_name: "John Doe"          # Optional: Contact for the server
        access_via: "Intranet"            # Optional: Any special network access needed
        user_defined:                     # Optional: User-defined additional information
          # User-defined properties:
          stuff: morestuff

    server_groups:                        # Fixed top-level key

      mygroup1:                           # Nickname of the server group
        description: "my dev systems"     # Short description of server group
        members:                          # Group members (servers or groups)
          - myserver1
          - myserver2
        user_defined:                     # Optional: User-defined additional information
          # User-defined properties:
          stuff: morestuff

    default: mygroup1                     # Fixed top-level key: default server or group

In the example above, ``myserver1``, ``myserver2``, and ``mygroup1`` are
nicknames of the respective server or server groups. These nicknames are used
when servers or groups are put into a server group in that file, or when they
are specified as a default in that file, or when they are used in functions of
the **easy-server** package. See :class:`easy_server.ServerFile` for details.

These nicknames are case sensitive and their allowable character set are
alphenumeric characters and the underscore character, i.e. ``A-Z``, ``a-z``,
``0-9``, and ``_``.

The value of the optional ``vault_file`` top-level property is the path name
of the vault file that belongs to this server file. Relative path names are
relative to the directory of the server file.

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
  Can be schema-validated via the ``user_defined_schema`` init parameter of
  :class:`easy_server.ServerFile`.

The value of the ``server_groups`` top-level property is an object that has one
property for each server group that is defined. The property name is the group
nickname, and the property value is an object with the following properties:

* ``description`` (string): Short description of the server group (required).
* ``members`` (list): List of server nicknames or other group nicknames that
  are the members of the group (required).
* ``user_defined`` (object): User-defined details of the group (optional).
  Can be schema-validated via the ``group_user_defined_schema`` init parameter
  of :class:`easy_server.ServerFile`.

The value of the ``default`` top-level property is a string that is the
nickname of the default server or group.

Server groups may be nested. That is, server groups may be put into other server
groups at arbitrary nesting depth. There must not be any cycle (i.e. the
resulting graph of server groups must be a tree).

A particular server or server group may be put into more than one server group.


.. _`Vault files`:

Vault files
-----------

A *vault file* contains the sensitive portion of the servers, such as passwords
or API keys.

The vault file must be an "easy-vault" file and can be encrypted and decrypted
using the ``easy-vault`` command provided by the
`easy-vault <https://easy-vault.readthedocs.io/en/latest/>`_ package.

The "easy-vault" files must be in YAML syntax and must follow the rules
described in this section.

Here is a complete working example of a vault file that defines host, username
and password for the servers from the example server file shown in the previous
section:

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

The values of the server items can be schema-validated via the
``vault_server_schema`` init parameter of :class:`easy_server.ServerFile`,
or the ``server_schema`` init parameter of :class:`easy_server.VaultFile`.

Here is another example that defines URL and API key for the servers (or rather
for the services, in this case):

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

Because the server file has user-defined properties for each
server entry, and the structure of the server entries in the vault file
is user-defined, there is a choice of which information is put into which
file. For example, the host property from the previous examples could have
been moved into the server file as a user-defined property,
since usually it is not really a secret.

The vault file can be encrypted or decrypted using the ``easy-vault`` command
that is part of the
`easy-vault package <https://easy-vault.readthedocs.io/en/latest/>`_

The vault file can be in the encrypted state or in clear text when the
**easy-server** library functions are accessing it. It is recommended
to always have it in the encrypted state and to decrypt it only for the period
of time while it is edited.


.. _`Example usage`:

Example usage
-------------

The following code snippet shows how a server file and a vault file
is used to get to all the information that is needed to access a server
or in this example, the servers in a server group:

.. code-block:: python

    import easy_server

    # Some parameters that typically would be input to the program:
    vault_file = 'examples/vault.yml'        # Path name of vault file
    server_file = 'examples/server.yml'      # Path name of server file
    nickname = 'mygroup1'                    # Nickname of server or group

    try:
        esf = easy_server.ServerFile(server_file)
    except (easy_server.ServerFileException, easy_server.VaultFileException) as exc:
        print("Error: {}".format(exc))
        return 1

    es_list = esf.list_servers(nickname)  # Works for server and group nicknames

    for es in es_list:
        nick = es.nickname

        # The structure of the secrets in the vault file is user-defined.
        # Here, we use the first example vault file.

        host = es.secrets['host'],
        username = es.secrets['username']
        password = es.secrets['password']

        print("Server {n}: host={h}, username={u}, password=********".
              format(n=nick, h=host, u=username))

        # A fictitious session class
        session = MySession(host, username, password)
        . . .


.. _`Example usage with schema validation`:

Example usage with schema validation
------------------------------------

The following code snippet is an extension of the previous example that shows
how the user-defined items in a server file and the server items in a vault
file are validated with JSON schema.

Note that JSON schema validates the structure of complex objects and its use
does not require that the input data that is being validated is in JSON syntax.
In fact, in our case the input data is in YAML syntax, and what is validated is
the complex object representing the YAML file after it has been parsed.

For details about how to define a JSON schema, see
https://json-schema.org/understanding-json-schema/.
Note that the JSON schemas used in this project are represented using a Python
``dict`` object that represents the JSON schema (i.e. as if it had been loaded
from a JSON schema file using ``json.load()``). Due to the syntax similarities
between JSON and literal dict specifications in Python, the JSON schema examples in
that document can be specified directly in Python.

The server file used in this example is again the one shown earlier. In the
JSON schema, its user-defined property 'stuff' is defined as string-typed and
optional, and no additional properties are allowed. In this example, the
user-defined portions of the server items and group items are defined to be the
same.

The vault file used in this example is the one with the 'host', 'username' and
'password' properties shown earlier. In the JSON schema, these properties are
all defined as string-typed and required, and no additional properties are
allowed.

.. code-block:: python

    import easy_server

    # Some parameters that typically would be input to the program:
    vault_file = 'examples/vault.yml'        # Path name of vault file
    server_file = 'examples/server.yml'      # Path name of server file
    nickname = 'mygroup1'                    # Nickname of server or group

    # JSON schema applied to the value of the user_defined element of each
    # server item in the server file:
    user_defined_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "stuff": { "type": "string" },
        },
        "required": [
            # 'stuff' is optional
        ],
        "additionalProperties": False,
    }

    # JSON schema applied to the value of the user_defined element of each
    # group item in the server file. In this example, the same schema as for
    # the server items is used.
    group_user_defined_schema = user_defined_schema

    # JSON schema applied to the value of each server item in the vault file:
    vault_server_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "host": { "type": "string" },
            "username": { "type": "string" },
            "password": { "type": "string" },
        },
        "required": [
            "host",
            "username",
            "password",
        ],
        "additionalProperties": False,
    }

    try:
        esf = easy_server.ServerFile(
            server_file,
            user_defined_schema=user_defined_schema,
            group_user_defined_schema=group_user_defined_schema,
            vault_server_schema=vault_server_schema)
    except (easy_server.ServerFileException, easy_server.VaultFileException) as exc:
        print("Error: {}".format(exc))
        return 1

    es_list = esf.list_servers(nickname)  # Works for server and group nicknames

    for es in es_list:
        nick = es.nickname

        # The structure of the secrets in the vault file is user-defined.
        # Here, we use the first example vault file.

        host = es.secrets['host'],
        username = es.secrets['username']
        password = es.secrets['password']

        print("Server {n}: host={h}, username={u}, password=********".
              format(n=nick, h=host, u=username))

        # A fictitious session class
        session = MySession(host, username, password)
        . . .
