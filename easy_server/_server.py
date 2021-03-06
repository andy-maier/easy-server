# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A single server including secrets.
"""

from __future__ import absolute_import, print_function

__all__ = ['Server']


class Server(object):
    """
    A data object that represents a single server item from a server file, and
    optionally the corresponding secrets item from a vault file.

    Objects of this class are not created by the user, but are returned by
    methods of the :class:`~easy_server.ServerFile` class.

    Example for a server item in a server file:

    .. code-block:: yaml

        myserver1:                              # nickname of the server
          description: "my dev system 1"
          contact_name: "John Doe"
          access_via: "VPN to dev network"
          user_defined:                         # user-defined part
            stuff: morestuff

    Example for a corresponding secrets item in a vault file:

    .. code-block:: yaml

        myserver1:                              # nickname of the server
          host: "10.11.12.13"
          username: myuser1
          password: mypass1
    """

    def __init__(self, nickname, server_dict, secrets_dict=None):
        """
        Parameters:

          nickname (:term:`unicode string`):
            Nickname of the server.

          server_dict (dict):
            Dictionary with the properties of the server item from the server
            file, wherein optional properties omitted in the server file have
            been set to their default values.

          secrets_dict (dict):
            Dictionary with the properties of the secrets item from the vault
            file, or `None` if no vault file is specified in the server file
            or if the vault file does not contain a corresponding item.
        """
        self._nickname = nickname
        self._description = server_dict['description']
        self._contact_name = server_dict.get('contact_name', None)
        self._access_via = server_dict.get('access_via', None)
        self._user_defined = server_dict.get('user_defined', None)
        self._secrets = secrets_dict

    def __repr__(self):
        secrets = "{...}" if self._secrets else "None"
        return "Server(" \
            "nickname={s._nickname!r}, " \
            "description={s._description!r}, " \
            "contact_name={s._contact_name!r}, " \
            "access_via={s._access_via!r}, " \
            "user_defined={s._user_defined!r}, " \
            "secrets={secrets})". \
            format(s=self, secrets=secrets)

    @property
    def nickname(self):
        """
        :term:`unicode string`: Nickname of the server.
        """
        return self._nickname

    @property
    def description(self):
        """
        :term:`unicode string`: Short description of the server.

        This is the value of the ``description`` property of the server item
        in the server file.
        """
        return self._description

    @property
    def contact_name(self):
        """
        :term:`unicode string`: Name of technical contact for the server.

        This is the value of the ``contact_name`` property of the server item
        in the server file. It is optional and defaults to `None`.
        """
        return self._contact_name

    @property
    def access_via(self):
        """
        :term:`unicode string`: Short reminder on the network/firewall/proxy/vpn
        used to access the server.

        This is the value of the ``access_via`` property of the server item
        in the server file. It is optional and defaults to `None`.
        """
        return self._access_via

    @property
    def user_defined(self):
        """
        dict: Additional user-defined properties for the server.

        This is the value of the ``user_defined`` property of the server item
        in the server file. This value can have an arbitrary user-defined
        structure. It is optional and defaults to `None`.
        """
        return self._user_defined

    @property
    def secrets(self):
        """
        dict: Secrets defined in the vault file for the server, or `None` if
        no vault file is specified in the server file or if the vault file does
        not contain a corresponding item.
        """
        return self._secrets
