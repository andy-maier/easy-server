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


easy-server - Secure server access that is easy to use
******************************************************

The **easy-server** package is a Python library for securely defining
sensitive information for accessing servers (or services), such as logon
credentials or API keys.

The information for accessing the servers is divided into a general portion
that is defined in an openly accessible *server file*, and a sensitive portion
that is defined in an encrypted *vault file*.

The vault file defines the secrets needed to access the servers, such as
logon credentials or API keys. The vault file must be an "easy-vault" file and
thus can be encrypted and decrypted using the ``easy-vault`` command provided
by the `easy-vault <https://easy-vault.readthedocs.io/en/latest/>`_ package.
The "easy-vault" files remain encrypted in the file system while their content
is used to access the servers.

The server file defines general information about the servers, such as a short
description, contact name, or a reminder which network to use for accessing
them.

The link between the server file and the vault file are user-defined
nicknames for the servers. These nicknames can also used by users as a
convenient way to identify servers in commands.

The server files support the definition of server groups that
also have a nickname.

Typical use cases for the **easy-server** package are test programs
running end-to-end tests against real servers, or command line clients that
access servers or services.

This provides a convenient, flexible and secure way how Python programs can
retrieve the secrets needed for accessing servers or services, while protecting
these secrets in a secure way.

.. toctree::
   :maxdepth: 2
   :numbered:

   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst
