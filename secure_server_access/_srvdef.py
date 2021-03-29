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
Encapsulation of a single server definition.
"""

from __future__ import absolute_import, print_function

__all__ = ['ServerDefinition']


class ServerDefinition(object):
    """
    Represents a single server definition from a server definition file.

    Example for a server definition item in a server definition file:

    .. code-block:: yaml

        myserver1:                              # nickname of the server
          description: "my dev system 1"
          contact_name: "John Doe"
          access_via: "VPN to dev network"
          user_defined:                         # user-defined part
            stuff: morestuff
    """

    def __init__(self, nickname, server_dict):
        self._nickname = nickname
        self._description = server_dict['description']
        self._contact_name = server_dict.get('contact_name', None)
        self._access_via = server_dict.get('access_via', None)
        self._user_defined = server_dict.get('user_defined', None)

    def __repr__(self):
        return "ServerDefinition(" \
            "nickname={s._nickname!r}, " \
            "description={s._description!r}, " \
            "contact_name={s._contact_name!r}, " \
            "access_via={s._access_via!r}, " \
            "user_defined={s._user_defined!r})". \
            format(s=self)

    @property
    def nickname(self):
        """
        :term:`unicode string`: Nickname of the server.

        This is the key of the server object in the server definition file.
        """
        return self._nickname

    @property
    def description(self):
        """
        :term:`unicode string`: Short description of the server.

        This is the value of the ``description`` property of the server object
        in the server definition file.
        """
        return self._description

    @property
    def contact_name(self):
        """
        :term:`unicode string`: Name of technical contact for the server.

        This is the value of the ``contact_name`` property of the server object
        in the server definition file.
        """
        return self._contact_name

    @property
    def access_via(self):
        """
        :term:`unicode string`: Short reminder on the network/firewall/proxy/vpn
        used to access the server.

        This is the value of the ``access_via`` property of the server object
        in the server definition file.
        """
        return self._access_via

    @property
    def user_defined(self):
        """
        dict: Details of the server, such as IP address.

        This is the value of the ``user_defined`` property of the server object
        in the server definition file. This value can have an arbitrary
        user-defined structure.
        """
        return self._user_defined
