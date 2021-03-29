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
Encapsulation of vault files.
"""

from __future__ import absolute_import, print_function
from copy import deepcopy
import jsonschema
import easy_vault

from ._exceptions import VaultFileFormatError

__all__ = ['VaultFile']


# JSON schema describing the structure of the vault files
VAULT_FILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JSON schema for vault files used by the "
             "secure-server-access package",
    "definitions": {},
    "type": "object",
    "required": [
        "secrets",
    ],
    "additionalProperties": False,
    "properties": {
        "secrets": {
            "type": "object",
            "description": "The secrets of the servers",
            "additionalProperties": False,
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Nickname of the server",
                    "additionalProperties": True,
                },
            },
        },
    },
}


class VaultFile(object):
    """
    Encapsulates a vault file used by the secure-server-access package.

    For a description of the file format, see :ref:`Format of vault files`.

    The vault file may be in clear text form (i.e. unencrypted) or
    encrypted. The file remains unchanged in all cases, and only the data read
    from it is decrypted upon use if it was encrypted.
    """

    def __init__(self, filepath, password=None):
        """
        Parameters:

          filepath (:term:`unicode string`):
            Path name of vault file.

          password (:term:`unicode string`):
            Password for decrypting the vault file. If not provided, the vault
            file must be in clear text form (i.e. unencrypted).

        Raises:
          VaultFileOpenError: Error opening vault file
          VaultFileDecryptError: Error decrypting an encrypted vault file
          VaultFileFormatError: Invalid vault file content
        """
        self._filepath = filepath
        self._vault_obj = _load_vault_file(filepath, password)

        # The following attributes are for faster access
        self._secrets = self._vault_obj['secrets']

    @property
    def filepath(self):
        """
        :term:`unicode string`: File path of the vault file.
        """
        return self._filepath

    @property
    def nicknames(self):
        """
        list of string: Server nicknames in the vault.
        """
        return list(self._secrets.keys())

    def get_secrets(self, nickname):
        """
        Get the secrets for a given server nickname.

        Example:

          Using the following vault file:

          .. code-block:: yaml

              secrets:                              # Fixed key
                myserver1:                          # Nickname of the server
                  host: "10.11.12.13"               # User-defined secrets
                  username: myusername
                  password: mypassword

          The return value for ``nickname='myserver1'`` will be:

          .. code-block:: python

              dict(
                  'host': '10.11.12.13',
                  'username': 'myusername,
                  'password': 'mypassword',
              )

        Parameters:
          nickname (:term:`unicode string`): Server nickname.

        Returns:
          dict: Copy of the secrets for that server from the vault.

        Raises:
          :exc:`py:KeyError`: Nickname not found in the vault.
        """
        try:
            secrets_dict = self._secrets[nickname]
        except KeyError:
            new_exc = KeyError(
                "Server with nickname {n} not found in vault file {fn}".
                format(n=nickname, fn=self._filepath))
            new_exc.__cause__ = None
            raise new_exc  # KeyError
        return deepcopy(secrets_dict)


def _load_vault_file(filepath, password=None):
    """
    Load the vault file and return its complete content.

    The format of the vault file is validated against a JSON schema.

    Parameters:

      filepath (:term:`unicode string`):
        Path name of vault file.

      password (:term:`unicode string`):
        Password for decrypting the vault file. If `None`, the vault file must
        be in clear text form (i.e. unencrypted).

    Returns:
      dict: Python dict representing the vault file content.

    Raises:
      EasyVaultException: Error with opening or decrypting vault file
      VaultFileFormatError: Invalid vault file content
    """

    password = easy_vault.get_password(filepath)
    vault = easy_vault.EasyVault(filepath, password)
    try:
        vault_obj = vault.get_yaml()
    except easy_vault.EasyVaultException as exc:
        raise exc  # For now. TODO: Encapsulate exceptions
    easy_vault.set_password(filepath, password)

    # Validate the data object using JSON schema
    try:
        jsonschema.validate(vault_obj, VAULT_FILE_SCHEMA)
        # Raises jsonschema.exceptions.SchemaError if JSON schema is invalid
    except jsonschema.exceptions.ValidationError as exc:
        if exc.absolute_path:
            elem_str = "element '{}'". \
                format('.'.join(str(e) for e in exc.absolute_path))
        else:
            elem_str = 'top-level element'
        new_exc = VaultFileFormatError(
            "Invalid format in vault file {fn}: Validation failed on {elem}: "
            "{msg}".
            format(fn=filepath, elem=elem_str, msg=exc.message))
        new_exc.__cause__ = None
        raise new_exc  # VaultFileFormatError

    return vault_obj
