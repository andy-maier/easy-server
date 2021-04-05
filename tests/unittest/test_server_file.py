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
Test the _server_file.py module.
"""

from __future__ import absolute_import, print_function
import os
import pytest
from easy_server import ServerFile, ServerFileFormatError, ServerFileOpenError
# White box testing: We test an internal function
from easy_server._server_file import _load_server_file

from ..utils.simplified_test_function import simplified_test_function
from ..utils.server_file_utils import easy_server_file


TEST_SERVERFILE_FILEPATH = 'tests/testfiles/server.yml'
TEST_SERVERFILE_FILEPATH_ABS = os.path.abspath(TEST_SERVERFILE_FILEPATH)
TEST_VAULTFILE_FILEPATH = 'tests/testfiles/vault.yml'
TEST_VAULTFILE_FILEPATH_ABS = os.path.abspath(TEST_VAULTFILE_FILEPATH)

# Standard server and vault files that are dynamically created for testing:
TEST_SERVER_FILENAME = 'server.yml'
TEST_VAULT_FILENAME = 'vault.yml'
TEST_VAULT_PASSWORD = 'vault'

TESTCASES_SF_INIT = [

    # Testcases for ServerFile.__init__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to ServerFile().
    #   * init_kwargs: Dict of keyword arguments to ServerFile().
    #   * exp_serverfile_attrs: Dict with expected ServerFile attributes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Order of positional parameters",
        dict(
            init_args=(
                TEST_SERVERFILE_FILEPATH,
            ),
            init_kwargs=dict(),
            exp_serverfile_attrs={
                'filepath': TEST_SERVERFILE_FILEPATH_ABS,
            },
        ),
        None, None, True
    ),
    (
        "Names of keyword arguments",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath=TEST_SERVERFILE_FILEPATH,
            ),
            exp_serverfile_attrs={
                'filepath': TEST_SERVERFILE_FILEPATH_ABS,
            },
        ),
        None, None, True
    ),
    (
        "Omitted required parameter: filepath",
        dict(
            init_args=(),
            init_kwargs=dict(),
            exp_serverfile_attrs=None,
        ),
        TypeError, None, True
    ),
    (
        "File not found",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath='invalid_file',
            ),
            exp_serverfile_attrs=None,
        ),
        (ServerFileOpenError, "Cannot open server file"),
        None, True
    ),
    (
        "Server file that references vault file",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath=TEST_SERVERFILE_FILEPATH,
            ),
            exp_serverfile_attrs={
                'filepath': TEST_SERVERFILE_FILEPATH_ABS,
                'vault_file': TEST_VAULTFILE_FILEPATH_ABS,
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_INIT)
@simplified_test_function
def test_ServerFile_init(
        testcase, init_args, init_kwargs, exp_serverfile_attrs):
    """
    Test function for ServerFile.__init__()
    """

    # The code to be tested
    act_obj = ServerFile(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None, \
        "Expected exception not raised: {}". \
        format(testcase.exp_exc_types)

    for attr_name in exp_serverfile_attrs:
        exp_attr_value = exp_serverfile_attrs[attr_name]
        assert hasattr(act_obj, attr_name), \
            "Missing attribute {0!r} in returned ServerFile object". \
            format(attr_name)
        act_attr_value = getattr(act_obj, attr_name)
        assert act_attr_value == exp_attr_value, \
            "Unexpected value for attribute {0!r}: Expected {1!r}, got {2!r}".\
            format(attr_name, exp_attr_value, act_attr_value)


TESTCASES_SF_LOAD = [

    # Testcases for ServerFile._load_server_file()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * exp_data: Expected result of _load_server_file()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic validation
    (
        "Empty file: Missing required elements",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on top-level element.* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid YAML syntax: Mixing list and dict",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  - foo\n"
                        "  bar:\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError, "Invalid YAML syntax"),
        None, True
    ),
    (
        "Invalid top-level type list",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="- servers: {}\n"
                        "- server_groups: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on top-level element: .* is not of type 'object'"),
        None, True
    ),
    (
        "Missing required 'servers' element",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="server_groups: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on top-level element: 'servers' is a required "
         "property"),
        None, True
    ),
    (
        "Invalid type for 'servers' element: list",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  - foo\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'servers': .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'servers' element: string",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: bla\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'servers': .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'server_groups' element: list",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups: []\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Invalid type for 'server_groups' element: string",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups: bla\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Invalid type of server group",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1: invalid\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Missing required element 'description' in server group",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    members: []\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1': 'description' is "
         "a required property"),
        None, True
    ),
    (
        "Invalid type for element 'description' in server group: list",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: []\n"
                        "    members: []\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1.description': "
         ".* is not of type 'string'"),
        None, True
    ),
    (
        "Missing required element 'members' in server group",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: desc1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1': 'members' is "
         "a required property"),
        None, True
    ),
    (
        "Invalid type for element 'members' in server group: string",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: desc1\n"
                        "    members: invalid\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1.members': "
         ".* is not of type 'array'"),
        None, True
    ),
    (
        "Invalid type for server group member: dict",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: desc1\n"
                        "    members:\n"
                        "      - {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'server_groups.grp1.members.0': "
         ".* is not of type 'string'"),
        None, True
    ),
    (
        "Invalid default null",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups: {}\n"
                        "default: null\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Validation failed on element 'default': "
         "None is not of type 'string'"),
        None, True
    ),

    # More semantic errors
    (
        "Server group member nickname not found",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: desc1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Nickname 'srv1' in server group 'grp1' not found"),
        None, True
    ),
    (
        "Default nickname not found",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: desc1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "default: srv\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data=None,
        ),
        (ServerFileFormatError,
         "Default nickname 'srv' not found"),
        None, True
    ),

    # Valid simple server files
    (
        "Valid file with no servers and server_group+default omitted",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data={
                'servers': {},
                'server_groups': {},
                'default': None,
                'vault_file': None,
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one server that is default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "default: srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data={
                'servers': {
                    'srv1': {
                        'description': 'server1',
                        'user_defined': {
                            'stuff': 42,
                        },
                    },
                },
                'server_groups': {},
                'default': 'srv1',
                'vault_file': None,
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one server and one server group that is default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "default: grp1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_data={
                'servers': {
                    'srv1': {
                        'description': 'server1',
                        'user_defined': {
                            'stuff': 42,
                        },
                    },
                },
                'server_groups': {
                    'grp1': {
                        'description': 'group1',
                        'members': ['srv1'],
                    },
                },
                'default': 'grp1',
                'vault_file': None,
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_LOAD)
@simplified_test_function
def test_ServerFile_load(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, exp_data):
    """
    Test function for ServerFile._load_server_file()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        # The code to be tested
        act_data = _load_server_file(server_filepath)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert act_data == exp_data


TESTCASES_SF_IS_VAULT_FILE_ENCRYPTED = [

    # Testcases for ServerFile.is_vault_file_encrypted()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * exp_result: Expected return valoue of is_vault_file_encrypted().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No vault file",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_encrypted=None,
        ),
        None, None, True
    ),
    (
        "Decrypted vault file, no password",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="vault_file: {vfn}\n"
                        "servers:\n"
                        "  srv1:\n"
                        "    description: server1\n". \
                        format(vfn=TEST_VAULT_FILENAME),
            vault_filename=TEST_VAULT_FILENAME,
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            vault_password=None,
            exp_encrypted=False,
        ),
        None, None, True
    ),
    (
        "Encrypted vault file, with correct password",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="vault_file: {vfn}\n"
                        "servers:\n"
                        "  srv1:\n"
                        "    description: server1\n". \
                        format(vfn=TEST_VAULT_FILENAME),
            vault_filename=TEST_VAULT_FILENAME,
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            vault_password=TEST_VAULT_PASSWORD,
            exp_encrypted=True,
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_IS_VAULT_FILE_ENCRYPTED)
@simplified_test_function
def test_SF_is_vault_file_encrypted(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, exp_encrypted):
    """
    Test function for ServerFile.is_vault_file_encrypted()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        esf = ServerFile(server_filepath, vault_password, use_keyring=False,
                         use_prompting=False)

        # The code to be tested
        act_encrypted = esf.is_vault_file_encrypted()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert act_encrypted == exp_encrypted


TESTCASES_SF_GET_SERVER = [

    # Testcases for ServerFile.get_server()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * nick: nickname input parameter for get_server().
    #   * exp_server_attrs: Dict with expected attributes of Server result
    #     of get_server().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_server_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_server_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_server_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; existing server nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv1',
            exp_server_attrs=dict(
                nickname='srv1',
                description='server1',
                contact_name=None,
                access_via=None,
                user_defined={'stuff': 42},
            ),
        ),
        None, None, True
    ),
    (
        "One server group with one server; existing group nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='grp1',
            exp_server_attrs=None,
        ),
        (KeyError, "Server with nickname 'grp1' not found"),
        None, True
    ),
    (
        "One server with vault file, server exists in vault file",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="vault_file: {vfn}\n"
                        "servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n".format(vfn=TEST_VAULT_FILENAME),
            vault_filename=TEST_VAULT_FILENAME,
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            vault_password=None,
            nick='srv1',
            exp_server_attrs=dict(
                nickname='srv1',
                description='server1',
                contact_name=None,
                access_via=None,
                user_defined={'stuff': 42},
                secrets={'foo': 'bar'}),
        ),
        None, None, True
    ),
    (
        "One server with vault file, server does not exist in vault file",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="vault_file: {vfn}\n"
                        "servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n".format(vfn=TEST_VAULT_FILENAME),
            vault_filename=TEST_VAULT_FILENAME,
            vault_yaml="secrets:\n"
                       "  srv2:\n"
                       "    foo: bar\n",
            vault_password=None,
            nick='srv1',
            exp_server_attrs=dict(
                nickname='srv1',
                description='server1',
                contact_name=None,
                access_via=None,
                user_defined={'stuff': 42},
                secrets=None),
        ),
        None, None, True
    ),
    (
        "One server with encrypted vault file",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="vault_file: {vfn}\n"
                        "servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n".format(vfn=TEST_VAULT_FILENAME),
            vault_filename=TEST_VAULT_FILENAME,
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            vault_password=TEST_VAULT_PASSWORD,
            nick='srv1',
            exp_server_attrs=dict(
                nickname='srv1',
                description='server1',
                contact_name=None,
                access_via=None,
                user_defined={'stuff': 42},
                secrets={'foo': 'bar'}),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_GET_SERVER)
@simplified_test_function
def test_ServerFile_get_server(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, nick, exp_server_attrs):
    """
    Test function for ServerFile.get_server()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        esf = ServerFile(server_filepath, vault_password, use_keyring=False,
                         use_prompting=False)

        # The code to be tested
        act_srv = esf.get_server(nick)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        for name in exp_server_attrs:
            assert getattr(act_srv, name) == exp_server_attrs[name]


TESTCASES_SF_LIST_SERVERS = [

    # Testcases for ServerFile.list_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * nick: nickname input parameter for list_servers().
    #   * exp_servers_attrs: List of dicts with expected attributes of
    #     Server objects in the result of list_servers().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_servers_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_servers_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; non-existing nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv',
            exp_servers_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; existing server nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='srv1',
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with one server; existing group nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='grp1',
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with two servers; existing group nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='grp1',
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "Nested server groups 2 levels deep; existing group nickname",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "  grp2:\n"
                        "    description: group2\n"
                        "    members:\n"
                        "      - grp1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='grp2',
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "Nested server groups 2 levels deep; existing group nickname and "
        "multiple group memberships",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "  grp2:\n"
                        "    description: group2\n"
                        "    members:\n"
                        "      - grp1\n"
                        "      - srv1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            nick='grp2',
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_LIST_SERVERS)
@simplified_test_function
def test_ServerFile_list_servers(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, nick, exp_servers_attrs):
    """
    Test function for ServerFile.list_servers()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        esf = ServerFile(server_filepath, vault_password, use_keyring=False,
                         use_prompting=False)

        # The code to be tested
        act_sds = esf.list_servers(nick)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_servers_attrs) == len(act_sds)

        sorted_exp_servers_attrs = sorted(
            exp_servers_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_server_attrs in enumerate(sorted_exp_servers_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_server_attrs:
                assert getattr(act_sd, name) == exp_server_attrs[name]


TESTCASES_SF_LIST_DEFAULT_SERVERS = [

    # Testcases for ServerFile.list_default_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * exp_servers_attrs: List of dicts with expected attributes of
    #     Server objects in the result of list_default_servers().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers, no default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server; no default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server; with default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "default: srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with one server; server is default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "default: srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with one server; group is default",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "default: grp1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_LIST_DEFAULT_SERVERS)
@simplified_test_function
def test_ServerFile_list_default_servers(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, exp_servers_attrs):
    """
    Test function for ServerFile.list_default_servers()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        esf = ServerFile(server_filepath, vault_password, use_keyring=False,
                         use_prompting=False)

        # The code to be tested
        act_sds = esf.list_default_servers()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_servers_attrs) == len(act_sds)

        sorted_exp_servers_attrs = sorted(
            exp_servers_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_server_attrs in enumerate(sorted_exp_servers_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_server_attrs:
                assert getattr(act_sd, name) == exp_server_attrs[name]


TESTCASES_SF_LIST_ALL_SERVERS = [

    # Testcases for ServerFile.list_all_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * server_filename: Filename of server file to be created.
    #   * server_yaml: Content of server file.
    #   * vault_filename: Filename of vault file to be created, or None.
    #   * vault_yaml: Content of vault file, or None.
    #   * vault_password: Password for encryption of vault file, or None.
    #   * exp_servers_attrs: List of dicts with expected attributes of
    #     Server objects in the result of list_all_servers().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers: {}\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with one server",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "One server group with two servers",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "Nested server groups 2 levels deep with two servers total",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "  grp2:\n"
                        "    description: group2\n"
                        "    members:\n"
                        "      - grp1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
    (
        "Nested server groups 2 levels deep with two servers total and "
        "multiple group memberships",
        dict(
            server_filename=TEST_SERVER_FILENAME,
            server_yaml="servers:\n"
                        "  srv1:\n"
                        "    description: server1\n"
                        "    user_defined:\n"
                        "      stuff: 42\n"
                        "  srv2:\n"
                        "    description: server2\n"
                        "    user_defined:\n"
                        "      stuff: 43\n"
                        "server_groups:\n"
                        "  grp1:\n"
                        "    description: group1\n"
                        "    members:\n"
                        "      - srv1\n"
                        "  grp2:\n"
                        "    description: group2\n"
                        "    members:\n"
                        "      - grp1\n"
                        "      - srv1\n"
                        "      - srv2\n",
            vault_filename=None,
            vault_yaml=None,
            vault_password=None,
            exp_servers_attrs=[
                dict(
                    nickname='srv1',
                    description='server1',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 42},
                ),
                dict(
                    nickname='srv2',
                    description='server2',
                    contact_name=None,
                    access_via=None,
                    user_defined={'stuff': 43},
                ),
            ],
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SF_LIST_ALL_SERVERS)
@simplified_test_function
def test_ServerFile_list_all_servers(
        testcase, server_filename, server_yaml, vault_filename, vault_yaml,
        vault_password, exp_servers_attrs):
    """
    Test function for ServerFile.list_all_servers()
    """

    with easy_server_file(
            server_filename, server_yaml, vault_filename, vault_yaml,
            vault_password) as server_filepath:

        esf = ServerFile(server_filepath, vault_password, use_keyring=False,
                         use_prompting=False)

        # The code to be tested
        act_sds = esf.list_all_servers()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_servers_attrs) == len(act_sds)

        sorted_exp_servers_attrs = sorted(
            exp_servers_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_server_attrs in enumerate(sorted_exp_servers_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_server_attrs:
                assert getattr(act_sd, name) == exp_server_attrs[name]
