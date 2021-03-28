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
*****************************************

The **secure-server-access** Python package is a library for retrieving the
secrets needed for accessing servers or services from an encrypted
`Ansible vault file`_ in YAML format.

The servers are identified with user-defined nicknames and the data structure
of the secrets for each server is completely user-defined. The password for the
Ansible vault file must be provided by the caller of the **secure-server-access**
library. The documentation describes approaches for how the vault password can
be stored securely in CI systems and in keyring facilities.

An optional server definition file in YAML format is used to define some basic
information about the servers and to define groups of servers and a default
server or group. The servers and groups are identified using user-defined
nicknames. The Ansible vault file uses the same server nicknames to store the
secrets.

The end result is a convenient, flexible and secure way how your Python programs
can retrieve the secrets needed for accessing servers or services, while
protecting these secrets in a secure way. In addition, groups of servers can be
accessed for example to run automated tests against each server in the group.

.. toctree::
   :maxdepth: 2
   :numbered:

   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst

.. # Links:

.. _`Ansible vault file`: https://docs.ansible.com/ansible/latest/user_guide/vault.html
