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


secure-server-access - Secure Server Access
*******************************************

The **secure-server-access** package is a library for retrieving the information
needed for accessing servers (or service), such as IP address, logon credentials,
or informal information such as contact name or which network to use.

The information for accessing the servers is divided into an open part that is
defined in a *server definition file*, and a protected part containing the
secrets for the actual access that is defined in a *vault file*. The vault file
can be encrypted and decrypted using the ``easy-vault`` command provided by the
`easy-vault <https://easy-vault.readthedocs.io/en/latest/>`_ package.

The server definition file defines nicknames for the servers and allows grouping
them into groups that also have nicknames.

The **secure-server-access** package is not used by end users, but by programs
that integrate with it, such as test programs or command line clients that
access servers or services. The users of these programs can then access
servers or services by means of the server and group nicknames that are defined.

The secrets needed to access the servers remain in the vault file which remains
encrypted in teh file system while the server is accessed.

This provides a convenient, flexible and secure way how your Python programs
can retrieve the secrets needed for accessing servers or services, while
protecting these secrets in a secure way.

.. toctree::
   :maxdepth: 2
   :numbered:

   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst
