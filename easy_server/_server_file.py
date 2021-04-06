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
Support for server files.
"""

from __future__ import absolute_import, print_function
import os
import yaml
import jsonschema

from ._server import Server
from ._vault_file import VaultFile

__all__ = ['ServerFile', 'ServerFileException',
           'ServerFileOpenError', 'ServerFileFormatError',
           'ServerFileUserDefinedFormatError',
           'ServerFileUserDefinedSchemaError',
           'ServerFileGroupUserDefinedFormatError',
           'ServerFileGroupUserDefinedSchemaError']


# JSON schema describing the structure of the server files
SERVER_FILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JSON schema for easy-server server files",
    "definitions": {},
    "type": "object",
    "required": [
        "servers",
    ],
    "additionalProperties": False,
    "properties": {
        "vault_file": {
            "type": "string",
            "description":
                "Path name of vault file. Relative path names are relative to "
                "the directory of the server file",
        },
        "servers": {
            "type": "object",
            "description": "The servers in the server file",
            "additionalProperties": False,
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Nickname of the server",
                    "required": [
                        "description",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Short description of the server",
                        },
                        "contact_name": {
                            "type": "string",
                            "description":
                                "Name of technical contact for the server",
                        },
                        "access_via": {
                            "type": "string",
                            "description":
                                "Short reminder on the "
                                "network/firewall/proxy/vpn used to access the "
                                "server",
                        },
                        "user_defined": {
                            "type": "object",
                            "description":
                                "User-defined properties of the server. "
                                "This object can have an arbitrary "
                                "user-defined structure",
                        },
                    },
                },
            },
        },
        "server_groups": {
            "type": "object",
            "description": "The server groups in the server file",
            "additionalProperties": False,
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Nickname of the server group",
                    "required": [
                        "description",
                        "members",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "description": {
                            "type": "string",
                            "description":
                                "Short description of the server group",
                        },
                        "members": {
                            "type": "array",
                            "description":
                                "List of members of the server group. "
                                "Those can be servers or other server groups.",
                            "items": {
                                "type": "string",
                                "description":
                                    "Nickname of server or server group in "
                                    "this file",
                            },
                        },
                        "user_defined": {
                            "type": "object",
                            "description":
                                "User-defined properties of the server group. "
                                "This object can have an arbitrary "
                                "user-defined structure",
                        },
                    },
                },
            },
        },
        "default": {
            "type": "string",
            "description": "Nickname of default server or server group",
        },
    },
}


class ServerFileException(Exception):
    """
    Abstract base exception for errors related to server files.

    Derived from :exc:`py:Exception`.
    """
    pass


class ServerFileOpenError(ServerFileException):
    """
    Exception indicating that a server file was not found or cannot
    be accessed due to a permission error.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFileFormatError(ServerFileException):
    """
    Exception indicating that an existing server file has some
    issue with the format of its file content.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFileUserDefinedFormatError(ServerFileException):
    """
    Exception indicating that the values of the user-defined portion of server
    items in a server file do not match the JSON schema defined for them.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFileUserDefinedSchemaError(ServerFileException):
    """
    Exception indicating that the JSON schema for validating the values of the
    user-defined portion of server items in a server file is not a valid JSON
    schema.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFileGroupUserDefinedFormatError(ServerFileException):
    """
    Exception indicating that the values of the user-defined portion of group
    items in a server file do not match the JSON schema defined for them.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFileGroupUserDefinedSchemaError(ServerFileException):
    """
    Exception indicating that the JSON schema for validating the values of the
    user-defined portion of group items in a server file is not a valid JSON
    schema.

    Derived from :exc:`ServerFileException`.
    """
    pass


class ServerFile(object):
    """
    A server file that specifies the openly accessible portion of the servers
    and optionally references a vault file that specifies the secret portion
    of the servers.

    An object of this class is tied to a single server file.

    The server file is loaded when this object is initialized. If
    the server file specifies a vault file, the vault file is also
    loaded at that point.

    Optionally, the user-defined portions of the server and group items in
    the server file, and the server items in the vault file can be validated
    against user-provided JSON schema.

    For a description of the file formats, see sections
    :ref:`Server files` and :ref:`Vault files`.
    """

    def __init__(
            self, filepath, password=None, use_keyring=True, use_prompting=True,
            verbose=False, user_defined_schema=None,
            group_user_defined_schema=None, vault_server_schema=None):
        """
        Parameters:

          filepath (:term:`unicode string`):
            Path name of the server file. Relative path names are
            relative to the current directory.

          password (:term:`unicode string`):
            Password for the vault file. `None` indicates that no password has
            been provided.

          use_keyring (bool):
            Enable the use of the keyring service for retrieving and storing the
            password of the vault file.

          use_prompting (bool):
            Enable the use of password prompting for getting the password of
            the vault file.

          verbose (bool):
            Print additional messages. Note that the password prompt (if needed)
            is displayed regardless of verbose mode.

          user_defined_schema (:term:`JSON schema`):
            JSON schema for validating the values of the user-defined portion
            of server items when loading the server file.
            `None` means no schema validation takes place for these items.

          group_user_defined_schema (:term:`JSON schema`):
            JSON schema for validating the values of the user-defined portion
            of group items when loading the server file.
            `None` means no schema validation takes place for these items.

          vault_server_schema (:term:`JSON schema`):
            JSON schema for validating the values of the server items when
            loading the vault file.
            `None` means no schema validation takes place for these items.

        Raises:
          ServerFileOpenError: Error opening server file
          ServerFileFormatError: Invalid server file format
          ServerFileUserDefinedFormatError: Invalid format of user-defined
            portion of server items in the server file
          ServerFileUserDefinedSchemaError: Invalid JSON schema for validating
            user-defined portion of server items in the server file
          ServerFileGroupUserDefinedFormatError: Invalid format of user-defined
            portion of group items in the server file
          ServerFileGroupUserDefinedSchemaError: Invalid JSON schema for
            validating user-defined portion of group items in the server file
          VaultFileOpenError: Error with opening the vault file
          VaultFileDecryptError: Error with decrypting the vault file
          VaultFileFormatError: Invalid vault file format
          VaultFileServerFormatError: Invalid format of server items in the
            vault file
          VaultFileServerSchemaError: Invalid JSON schema for validating server
            items in the vault file
        """
        self._filepath = os.path.abspath(filepath)
        self._user_defined_schema = user_defined_schema
        self._group_user_defined_schema = group_user_defined_schema
        self._vault_server_schema = vault_server_schema

        self._data = _load_server_file(
            filepath, user_defined_schema, group_user_defined_schema)

        self._vault_file = self._data['vault_file']
        if self._vault_file:
            if not os.path.isabs(self._vault_file):
                self._vault_file = os.path.join(
                    os.path.dirname(self._filepath), self._vault_file)
            self._vault = VaultFile(
                self._vault_file, password=password, use_keyring=use_keyring,
                use_prompting=use_prompting, verbose=verbose,
                server_schema=vault_server_schema)
        else:
            self._vault = None

        # The following attributes are for faster access
        self._servers = self._data['servers']
        self._server_groups = self._data['server_groups']
        self._default = self._data['default']

    @property
    def filepath(self):
        """
        :term:`unicode string`: Absolute path name of the server file.
        """
        return self._filepath

    @property
    def vault_file(self):
        """
        :term:`unicode string`: Absolute path name of the vault file specified
        in the server file, or `None` if no vault file was specified.

        Vault files specified with a relative path name are relative to the
        directory of the server file.
        """
        return self._vault_file

    @property
    def user_defined_schema(self):
        """
        :term:`JSON schema`: JSON schema for validating the values of the
        user-defined portion of server items in the server file, or `None`.
        """
        return self._user_defined_schema

    @property
    def group_user_defined_schema(self):
        """
        :term:`JSON schema`: JSON schema for validating the values of the
        user-defined portion of group items in the server file, or `None`.
        """
        return self._group_user_defined_schema

    @property
    def vault_server_schema(self):
        """
        :term:`JSON schema`: JSON schema for validating the values of the
        server items in the vault file, or `None`.
        """
        return self._vault_server_schema

    def is_vault_file_encrypted(self):
        """
        Test whether the vault file is in the encrypted state.

        If the server file does not specify a vault file, `None` is returned.

        Returns:
          bool: Boolean indicating whether the vault file is in the encrypted
          state, or `None` if no vault file was specified.
        """
        if self._vault is None:
            return None
        return self._vault.is_encrypted()

    def get_server(self, nickname):
        """
        Get server for a given server nickname.

        Parameters:
          nickname (:term:`unicode string`): Server nickname.

        Returns:
          :class:`~easy_server.Server`:
             Server with the specified nickname.

        Raises:
          :exc:`py:KeyError`: Nickname not found
        """
        try:
            server_dict = self._servers[nickname]
        except KeyError:
            new_exc = KeyError(
                "Server with nickname {!r} not found in server "
                "file {!r}".
                format(nickname, self._filepath))
            new_exc.__cause__ = None
            raise new_exc  # KeyError
        if self._vault:
            try:
                secrets_dict = self._vault.get_secrets(nickname)
            except KeyError:
                secrets_dict = None
        else:
            secrets_dict = None
        return Server(nickname, server_dict, secrets_dict)

    def list_servers(self, nickname):
        """
        List the servers for a given server or server group nickname.

        Parameters:
          nickname (:term:`unicode string`): Server or server group nickname.

        Returns:
          list of :class:`~easy_server.Server`:
          List of servers.

        Raises:
          :exc:`py:KeyError`: Nickname not found
        """
        if nickname in self._servers:
            return [self.get_server(nickname)]

        if nickname in self._server_groups:
            sd_list = list()  # of Server objects
            sd_nick_list = list()  # of server nicknames
            sg_item = self._server_groups[nickname]
            for member_nick in sg_item['members']:
                member_sds = self.list_servers(member_nick)
                for sd in member_sds:
                    if sd.nickname not in sd_nick_list:
                        sd_nick_list.append(sd.nickname)
                        sd_list.append(sd)
            return sd_list

        raise KeyError(
            "Server or server group with nickname {!r} not found in server "
            "definition file {!r}".
            format(nickname, self._filepath))

    def list_default_servers(self):
        """
        List the servers for the default server or group.

        An omitted 'default' element in the server file results in
        an empty list.

        Returns:
          list of :class:`~easy_server.Server`:
          List of servers.
        """
        if self._default is None:
            return []
        return self.list_servers(self._default)

    def list_all_servers(self):
        """
        List all servers.

        Returns:
          list of :class:`~easy_server.Server`:
          List of servers.
        """
        return [self.get_server(nickname) for nickname in self._servers]


def _load_server_file(
        filepath, user_defined_schema=None, group_user_defined_schema=None):
    """
    Load the server file, validate its format and default some
    optional elements.

    Returns:
      dict: Python dict representing the file content.

    Raises:
      ServerFileOpenError: Error opening server file
      ServerFileFormatError: Invalid server file content
      ServerFileUserDefinedFormatError: Invalid format of user-defined
        portion of server items in the server file
      ServerFileUserDefinedSchemaError: Invalid JSON schema for validating
        user-defined portion of server items in the server file
      ServerFileGroupUserDefinedFormatError: Invalid format of user-defined
        portion of group items in the server file
      ServerFileGroupUserDefinedSchemaError: Invalid JSON schema for
        validating user-defined portion of group items in the server file
    """

    # Load the server file (YAML)
    try:
        with open(filepath, 'r') as fp:
            data = yaml.safe_load(fp)
    except (OSError, IOError) as exc:
        new_exc = ServerFileOpenError(
            "Cannot open server file: {fn}: {exc}".
            format(fn=filepath, exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # ServerFileOpenError
    except yaml.YAMLError as exc:
        new_exc = ServerFileFormatError(
            "Invalid YAML syntax in server file {fn}: {exc}".
            format(fn=filepath, exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # ServerFileFormatError

    # Schema validation of server file content
    try:
        jsonschema.validate(data, SERVER_FILE_SCHEMA)
        # Raises jsonschema.exceptions.SchemaError if JSON schema is invalid
    except jsonschema.exceptions.ValidationError as exc:
        if exc.absolute_path:
            elem_str = "element '{}'". \
                format('.'.join(str(e) for e in exc.absolute_path))
        else:
            elem_str = 'top-level element'

        new_exc = ServerFileFormatError(
            "Invalid format in server file {fn}: Validation "
            "failed on {elem}: {exc}".
            format(fn=filepath, elem=elem_str, exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # ServerFileFormatError

    # Establish defaults for optional top-level elements

    if 'server_groups' not in data:
        data['server_groups'] = {}

    if 'default' not in data:
        data['default'] = None

    if 'vault_file' not in data:
        data['vault_file'] = None

    # Schema validation of user-defined portion of server items
    if user_defined_schema:
        for server_nick, server_item in data['servers'].items():
            user_defined = server_item.get('user_defined', None)
            if user_defined is None:
                new_exc = ServerFileUserDefinedFormatError(
                    "Missing user_defined element for server {srv} "
                    "in server file {fn}".
                    format(srv=server_nick, fn=filepath))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileUserDefinedFormatError
            try:
                jsonschema.validate(user_defined, user_defined_schema)
            except jsonschema.exceptions.SchemaError as exc:
                new_exc = ServerFileUserDefinedSchemaError(
                    "Invalid JSON schema for validating user-defined portion "
                    "of server items in server file: {exc}".
                    format(exc=exc))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileUserDefinedSchemaError
            except jsonschema.exceptions.ValidationError as exc:
                if exc.absolute_path:
                    elem_str = "element '{}'". \
                        format('.'.join(str(e) for e in exc.absolute_path))
                else:
                    elem_str = "top-level of user-defined item"
                new_exc = ServerFileUserDefinedFormatError(
                    "Invalid format in user-defined portion of item for "
                    "server {srv} in server file {fn}: "
                    "Validation failed on {elem}: {exc}".
                    format(srv=server_nick, fn=filepath, elem=elem_str,
                           exc=exc))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileUserDefinedFormatError

    # Schema validation of user-defined portion of group items
    if group_user_defined_schema:
        for group_nick, group_item in data['server_groups'].items():
            user_defined = group_item.get('user_defined', None)
            if user_defined is None:
                new_exc = ServerFileGroupUserDefinedFormatError(
                    "Missing user_defined element for group {grp} "
                    "in server file {fn}".
                    format(grp=group_nick, fn=filepath))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileGroupUserDefinedFormatError
            try:
                jsonschema.validate(user_defined, group_user_defined_schema)
            except jsonschema.exceptions.SchemaError as exc:
                new_exc = ServerFileGroupUserDefinedSchemaError(
                    "Invalid JSON schema for validating user-defined portion "
                    "of group items in server file: {exc}".
                    format(exc=exc))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileGroupUserDefinedSchemaError
            except jsonschema.exceptions.ValidationError as exc:
                if exc.absolute_path:
                    elem_str = "element '{}'". \
                        format('.'.join(str(e) for e in exc.absolute_path))
                else:
                    elem_str = "top-level of user-defined item"
                new_exc = ServerFileGroupUserDefinedFormatError(
                    "Invalid format in user-defined portion of item for "
                    "group {grp} in server file {fn}: "
                    "Validation failed on {elem}: {exc}".
                    format(grp=group_nick, fn=filepath, elem=elem_str,
                           exc=exc))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileGroupUserDefinedFormatError

    # Check dependencies in the file

    server_nicks = list(data['servers'].keys())
    group_nicks = list(data['server_groups'].keys())
    all_nicks = server_nicks + group_nicks
    default_nick = data['default']

    if default_nick and default_nick not in all_nicks:
        new_exc = ServerFileFormatError(
            "Default nickname '{n}' not found in servers or groups in "
            "server file {fn}".
            format(n=default_nick, fn=filepath))
        new_exc.__cause__ = None
        raise new_exc  # ServerFileFormatError

    for group_nick in group_nicks:
        sg_item = data['server_groups'][group_nick]
        for member_nick in sg_item['members']:
            if member_nick not in all_nicks:
                new_exc = ServerFileFormatError(
                    "Nickname '{n}' in server group '{g}' not found in "
                    "servers or groups in server file {fn}".
                    format(n=member_nick, g=group_nick, fn=filepath))
                new_exc.__cause__ = None
                raise new_exc  # ServerFileFormatError

    return data
