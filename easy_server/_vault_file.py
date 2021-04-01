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
Support for vault files.
"""

from __future__ import absolute_import, print_function
from copy import deepcopy
import jsonschema
import easy_vault


__all__ = ['VaultFile', 'VaultFileException', 'VaultFileOpenError',
           'VaultFileDecryptError', 'VaultFileFormatError']


# JSON schema describing the structure of the vault files
VAULT_FILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JSON schema for easy-server vault files",
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


class VaultFileException(Exception):
    """
    Abstract base exception for errors related to vault files.

    Derived from :exc:`py:Exception`.
    """
    pass


class VaultFileOpenError(VaultFileException):
    """
    Exception indicating that a vault file was not found or cannot be accessed
    for reading due to a permission error.

    Derived from :exc:`VaultFileException`.
    """
    pass


class VaultFileDecryptError(VaultFileException):
    """
    Exception indicating that an encrypted vault file could not be decrypted.

    Derived from :exc:`VaultFileException`.
    """
    pass


class VaultFileFormatError(VaultFileException):
    """
    Exception indicating that an existing vault file has some issue with the
    format of its file content.

    Derived from :exc:`VaultFileException`.
    """
    pass


class VaultFile(object):
    """
    A vault file that specifies the sensitive portion of servers,
    i.e. the secrets for accessing the servers.

    An object of this class is tied to a single vault file.

    For a description of the file format, see section :ref:`Vault files`.

    The vault file may be in the encrypted or decrypted state. When data from
    the vault file is read, the vault file remains unchanged, and the data is
    is decrypted in memory if the file was in the encrypted state.

    Vault file encryption, vault file decryption, and reading data from an
    encrypted vault file requires a password specific to the vault file.
    The password can be specified as an init argument to this class, or if not
    provided will be retrieved the keyring service, or if not found there, will
    be interactively prompted for. The use of the keyring service (for
    retrieving and storing) and the use of password prompting can be
    individually disabled.

    Typical use in client programs would be to use the keyring and to specify
    no password (the default). Typical use in test programs running in a CI/CD
    system would be to specify a password (from the CI/CD system's secrets)
    and not to use the keyring.
    """

    def __init__(
            self, filepath, password=None, use_keyring=True, use_prompting=True,
            verbose=False):
        """
        Parameters:

          filepath (:term:`unicode string`):
            Path name of the vault file.

          password (:term:`unicode string`):
            Password for the vault file. `None` indicates that no password has
            been provided.

          use_keyring (bool):
            Enable the use of the keyring service for retrieving and storing the
            password.

          use_prompting (bool):
            Enable the use of password prompting for getting the password.

          verbose (bool):
            Print additional messages. Note that the password prompt (if needed)
            is displayed regardless of verbose mode.

        Raises:
          VaultFileOpenError: Error with opening the vault file
          VaultFileDecryptError: Error with decrypting the vault file
          VaultFileFormatError: Invalid vault file format
        """
        self._filepath = filepath
        self._vault_obj = _load_vault_file(
            filepath, password, use_keyring, use_prompting, verbose)

        # The following attributes are for faster access
        self._secrets = self._vault_obj['secrets']

    @property
    def filepath(self):
        """
        :term:`unicode string`: Path name of the vault file.
        """
        return self._filepath

    @property
    def nicknames(self):
        """
        list of string: Server nicknames in the vault file.
        """
        return list(self._secrets.keys())

    def get_secrets(self, nickname):
        """
        Get the secrets item from the vault file for a given server nickname.

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
          dict: Copy of the secrets item for that server from the vault file.

        Raises:
          KeyError: Nickname not found in the vault file.
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


def _load_vault_file(filepath, password, use_keyring, use_prompting, verbose):
    """
    Load the vault file and return its complete content.

    The format of the vault file is validated against a JSON schema.

    Parameters:

      filepath (:term:`unicode string`):
        Path name of vault file.

      password (:term:`unicode string`):
        Password for the vault file. `None` indicates that no password has
        been provided.

      use_keyring (bool):
        Enable the use of the keyring service for retrieving and storing the
        password.

      use_prompting (bool):
        Enable the use of password prompting for getting the password.

      verbose (bool):
        Print additional messages. Note that the password prompt (if needed)
        is displayed regardless of verbose mode.

    Returns:
      dict: Python dict representing the vault file content.

    Raises:
      VaultFileOpenError: Error with opening the vault file
      VaultFileDecryptError: Error with decrypting the vault file
      VaultFileFormatError: Invalid vault file format
    """

    if password is None and easy_vault.EasyVault(filepath).is_encrypted():
        password = easy_vault.get_password(
            filepath, use_keyring=use_keyring, use_prompting=use_prompting,
            verbose=verbose)

    vault = easy_vault.EasyVault(filepath, password)
    try:
        vault_obj = vault.get_yaml()
    except easy_vault.EasyVaultFileError as exc:
        new_exc = VaultFileOpenError(str(exc))
        new_exc.__cause__ = None
        raise new_exc  # VaultFileOpenError
    except easy_vault.EasyVaultDecryptError as exc:
        new_exc = VaultFileDecryptError(str(exc))
        new_exc.__cause__ = None
        raise new_exc  # VaultFileDecryptError
    except easy_vault.EasyVaultYamlError as exc:
        new_exc = VaultFileFormatError(str(exc))
        new_exc.__cause__ = None
        raise new_exc  # VaultFileFormatError

    if password is not None:
        easy_vault.set_password(
            filepath, password, use_keyring=use_keyring, verbose=verbose)

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
