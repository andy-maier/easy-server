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
server_file_utils - Utilities for server file testing.
"""

from __future__ import absolute_import

import os
import contextlib
import six
import testfixtures
import easy_vault


@contextlib.contextmanager
def easy_server_file(
        server_filename, server_yaml, vault_filename=None, vault_yaml=None,
        vault_password=None):
    """
    Context manager that creates an easy-server server file and optionally
    a corresponding vault file from their YAML content, which is optionally
    encrypted with a password.
    """
    with testfixtures.TempDirectory() as tmp_dir:

        # Create the server file
        server_filepath = os.path.join(tmp_dir.path, server_filename)
        if isinstance(server_yaml, six.text_type):
            server_yaml = server_yaml.encode('utf-8')
        tmp_dir.write(server_filename, server_yaml)

        # Create the vault file, if specified
        if vault_yaml:
            vault_filepath = os.path.join(tmp_dir.path, vault_filename)
            if isinstance(vault_yaml, six.text_type):
                vault_yaml = vault_yaml.encode('utf-8')
            tmp_dir.write(vault_filename, vault_yaml)

            # Encrypt the vault file, if specified
            if vault_password:
                vault = easy_vault.EasyVault(vault_filepath, vault_password)
                vault.encrypt()
        else:
            vault_filepath = None

        yield server_filepath
