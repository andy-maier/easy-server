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
Test the _vault_file.py module.
"""

from __future__ import absolute_import, print_function
import os
import pytest
from testfixtures import TempDirectory
import six
import easy_vault
from easy_server import VaultFile, VaultFileFormatError, VaultFileOpenError
# White box testing: We test an internal function
from easy_server._vault_file import _load_vault_file

from ..utils.simplified_test_function import simplified_test_function


TEST_VAULTFILE_FILEPATH = 'tests/testfiles/vault.yml'
TEST_VAULTFILE_FILEPATH_ABS = os.path.abspath(TEST_VAULTFILE_FILEPATH)

TESTCASES_VAULTFILE_INIT = [

    # Testcases for VaultFile.__init__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to VaultFile().
    #   * init_kwargs: Dict of keyword arguments to VaultFile().
    #   * exp_attrs: Dict with expected VaultFile attributes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Order of positional parameters",
        dict(
            init_args=(
                TEST_VAULTFILE_FILEPATH,
                'mypassword',
                False,
                False,
                False,
            ),
            init_kwargs=dict(),
            exp_attrs={
                'filepath': TEST_VAULTFILE_FILEPATH_ABS,
            },
        ),
        None, None, True
    ),
    (
        "Names of keyword arguments",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath=TEST_VAULTFILE_FILEPATH,
                password='mypassword',
                use_keyring=False,
                use_prompting=False,
                verbose=False,
            ),
            exp_attrs={
                'filepath': TEST_VAULTFILE_FILEPATH_ABS,
            },
        ),
        None, None, True
    ),
    (
        "Omitted required parameter: filepath",
        dict(
            init_args=(),
            init_kwargs=dict(),
            exp_attrs=None,
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
            exp_attrs=None,
        ),
        (VaultFileOpenError, "Cannot open vault file"),
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VAULTFILE_INIT)
@simplified_test_function
def test_VaultFile_init(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test function for VaultFile.__init__()
    """

    # The code to be tested
    act_obj = VaultFile(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None, \
        "Expected exception not raised: {}". \
        format(testcase.exp_exc_types)

    for attr_name in exp_attrs:
        exp_attr_value = exp_attrs[attr_name]
        assert hasattr(act_obj, attr_name), \
            "Missing attribute {0!r} in returned VaultFile object". \
            format(attr_name)
        act_attr_value = getattr(act_obj, attr_name)
        assert act_attr_value == exp_attr_value, \
            "Unexpected value for attribute {0!r}: Expected {1!r}, got {2!r}".\
            format(attr_name, exp_attr_value, act_attr_value)


TESTCASES_VAULTFILE_LOAD = [

    # Testcases for VaultFile._load_vault_file()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * vault_yaml: Content of vault file.
    #   * password: Password for encryption (and flag to be encrypted)
    #   * exp_data: Expected result of _load_vault_file()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic validation
    (
        "Empty file: Missing required elements",
        dict(
            vault_yaml="",
            password=None,
            exp_data=None,
        ),
        (VaultFileFormatError,
         "Validation failed on top-level element.* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid YAML syntax: Mixing list and dict",
        dict(
            vault_yaml="servers:\n"
                       "  - foo\n"
                       "  bar:\n",
            password=None,
            exp_data=None,
        ),
        (VaultFileFormatError, "Invalid YAML syntax"),
        None, True
    ),
    (
        "Invalid top-level type list",
        dict(
            vault_yaml="- secrets: {}\n",
            password=None,
            exp_data=None,
        ),
        (VaultFileFormatError,
         "Validation failed on top-level element: .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'secrets' element: list",
        dict(
            vault_yaml="secrets:\n"
                       "  - foo\n",
            password=None,
            exp_data=None,
        ),
        (VaultFileFormatError,
         "Validation failed on element 'secrets': .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'secrets' element: string",
        dict(
            vault_yaml="secrets: bla\n",
            password=None,
            exp_data=None,
        ),
        (VaultFileFormatError,
         "Validation failed on element 'secrets': .* is not of type 'object'"),
        None, True
    ),

    # Valid simple server files
    (
        "Valid file with no secrets, decrypted",
        dict(
            vault_yaml="secrets: {}\n",
            password=None,
            exp_data={
                'secrets': {},
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one secret, decrypted",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            password=None,
            exp_data={
                'secrets': {
                    'srv1': {
                        'foo': 'bar',
                    },
                },
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one secret, encrypted",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            password='abc',
            exp_data={
                'secrets': {
                    'srv1': {
                        'foo': 'bar',
                    },
                },
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VAULTFILE_LOAD)
@simplified_test_function
def test_VaultFile_load(testcase, vault_yaml, password, exp_data):
    """
    Test function for VaultFile._load_vault_file()
    """

    with TempDirectory() as tmp_dir:

        # Create the vault file
        filename = 'tmp_vault.yml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(vault_yaml, six.text_type):
            vault_yaml = vault_yaml.encode('utf-8')
        tmp_dir.write(filename, vault_yaml)

        if password:
            vault = easy_vault.EasyVault(filepath, password)
            vault.encrypt()
            del vault

        # The code to be tested
        act_data = _load_vault_file(
            filepath, password, use_keyring=False, use_prompting=False,
            verbose=False)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert act_data == exp_data


TESTCASES_VAULTFILE_GET_SECRETS = [

    # Testcases for VaultFile.get_secrets()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * vault_yaml: Content of vault file.
    #   * nick: nickname input parameter for get_secrets().
    #   * exp_secrets: Dict with expected result of get_secrets().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No secrets; non-existing nickname",
        dict(
            vault_yaml="secrets: {}\n",
            nick='srv',
            exp_secrets=None,
        ),
        (KeyError, "Server with nickname .?srv.? not found"),
        None, True
    ),
    (
        "One secret; non-existing nickname",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            nick='srv',
            exp_secrets=None,
        ),
        (KeyError, "Server with nickname .?srv.? not found"),
        None, True
    ),
    (
        "One secret; existing nickname",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            nick='srv1',
            exp_secrets={
                'foo': 'bar',
            },
        ),
        None,
        None, True
    ),
    (
        "Two secrets; existing nickname",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n"
                       "  srv2:\n"
                       "    bar: foo\n",
            nick='srv1',
            exp_secrets={
                'foo': 'bar',
            },
        ),
        None,
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VAULTFILE_GET_SECRETS)
@simplified_test_function
def test_VaultFile_get_secrets(testcase, vault_yaml, nick, exp_secrets):
    """
    Test function for VaultFile.get_secrets()
    """

    with TempDirectory() as tmp_dir:

        # Create the server file
        filename = 'tmp_vault.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(vault_yaml, six.text_type):
            vault_yaml = vault_yaml.encode('utf-8')
        tmp_dir.write(filename, vault_yaml)

        vf = VaultFile(filepath)

        # The code to be tested
        act_secrets = vf.get_secrets(nick)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        for name in exp_secrets:
            assert act_secrets[name] == exp_secrets[name]


TESTCASES_VAULTFILE_NICKNAMES = [

    # Testcases for VaultFile.nicknames

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * vault_yaml: Content of vault file.
    #   * exp_nicknames: Dict with expected result of nicknames.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No secrets",
        dict(
            vault_yaml="secrets: {}\n",
            exp_nicknames=[],
        ),
        None,
        None, True
    ),
    (
        "One secret",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n",
            exp_nicknames=['srv1'],
        ),
        None,
        None, True
    ),
    (
        "Two secretw",
        dict(
            vault_yaml="secrets:\n"
                       "  srv1:\n"
                       "    foo: bar\n"
                       "  srv2:\n"
                       "    bar: foo\n",
            exp_nicknames=['srv1', 'srv2'],
        ),
        None,
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_VAULTFILE_NICKNAMES)
@simplified_test_function
def test_VaultFile_nicknames(testcase, vault_yaml, exp_nicknames):
    """
    Test function for VaultFile.nicknames
    """

    with TempDirectory() as tmp_dir:

        # Create the server file
        filename = 'tmp_vault.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(vault_yaml, six.text_type):
            vault_yaml = vault_yaml.encode('utf-8')
        tmp_dir.write(filename, vault_yaml)

        vf = VaultFile(filepath)

        # The code to be tested
        act_nicknames = vf.nicknames

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert set(act_nicknames) == set(exp_nicknames)
