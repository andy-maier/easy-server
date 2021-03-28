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
Test the _srvdeffile.py module.
"""

from __future__ import absolute_import, print_function
import os
import pytest
from testfixtures import TempDirectory
import six
from secure_server_access import ServerDefinitionFile, \
    ServerDefinitionFileFormatError, ServerDefinitionFileOpenError
# White box testing: We test an internal function
from secure_server_access._srvdeffile import _load_server_definition_file

from ..utils.simplified_test_function import simplified_test_function


TEST_SDF_FILEPATH = 'examples/ssa.yml'

TESTCASES_SDF_INIT = [

    # Testcases for ServerDefinitionFile.__init__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to ServerDefinitionFile().
    #   * init_kwargs: Dict of keyword arguments to ServerDefinitionFile().
    #   * exp_attrs: Dict with expected ServerDefinitionFile attributes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "Order of positional parameters",
        dict(
            init_args=(
                TEST_SDF_FILEPATH,
            ),
            init_kwargs=dict(),
            exp_attrs={
                'filepath': TEST_SDF_FILEPATH,
            },
        ),
        None, None, True
    ),
    (
        "Names of keyword arguments",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath=TEST_SDF_FILEPATH,
            ),
            exp_attrs={
                'filepath': TEST_SDF_FILEPATH,
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
        (ServerDefinitionFileOpenError, "Cannot open server definition file"),
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SDF_INIT)
@simplified_test_function
def test_SDF_init(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test function for ServerDefinitionFile.__init__()
    """

    # The code to be tested
    act_obj = ServerDefinitionFile(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None, \
        "Expected exception not raised: {}". \
        format(testcase.exp_exc_types)

    for attr_name in exp_attrs:
        exp_attr_value = exp_attrs[attr_name]
        assert hasattr(act_obj, attr_name), \
            "Missing attribute {0!r} in returned ServerDefinitionFile object". \
            format(attr_name)
        act_attr_value = getattr(act_obj, attr_name)
        assert act_attr_value == exp_attr_value, \
            "Unexpected value for attribute {0!r}: Expected {1!r}, got {2!r}".\
            format(attr_name, exp_attr_value, act_attr_value)


TESTCASES_SDF_LOAD = [

    # Testcases for ServerDefinitionFile._load_server_definition_file()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * exp_data: Expected result of _load_server_definition_file()
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic validation
    (
        "Empty file: Missing required elements",
        dict(
            sdf_yaml="",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on top-level element.* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid YAML syntax: Mixing list and dict",
        dict(
            sdf_yaml="servers:\n"
                     "  - foo\n"
                     "  bar:\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError, "Invalid YAML syntax"),
        None, True
    ),
    (
        "Invalid top-level type list",
        dict(
            sdf_yaml="- servers: {}\n"
                     "- server_groups: {}\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on top-level element: .* is not of type 'object'"),
        None, True
    ),
    (
        "Missing required 'servers' element",
        dict(
            sdf_yaml="server_groups: {}\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on top-level element: 'servers' is a required "
         "property"),
        None, True
    ),
    (
        "Invalid type for 'servers' element: list",
        dict(
            sdf_yaml="servers:\n"
                     "  - foo\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'servers': .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'servers' element: string",
        dict(
            sdf_yaml="servers: bla\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'servers': .* is not of type 'object'"),
        None, True
    ),
    (
        "Invalid type for 'server_groups' element: list",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: []\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Invalid type for 'server_groups' element: string",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: bla\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Invalid type of server group",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1: invalid\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1': .* is not of type "
         "'object'"),
        None, True
    ),
    (
        "Missing required element 'description' in server group",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    members: []\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1': 'description' is "
         "a required property"),
        None, True
    ),
    (
        "Invalid type for element 'description' in server group: list",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: []\n"
                     "    members: []\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1.description': "
         ".* is not of type 'string'"),
        None, True
    ),
    (
        "Missing required element 'members' in server group",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: desc1\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1': 'members' is "
         "a required property"),
        None, True
    ),
    (
        "Invalid type for element 'members' in server group: string",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: desc1\n"
                     "    members: invalid\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1.members': "
         ".* is not of type 'array'"),
        None, True
    ),
    (
        "Invalid type for server group member: dict",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: desc1\n"
                     "    members:\n"
                     "      - {}\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'server_groups.grp1.members.0': "
         ".* is not of type 'string'"),
        None, True
    ),
    (
        "Invalid default null",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: {}\n"
                     "default: null\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Validation failed on element 'default': "
         "None is not of type 'string'"),
        None, True
    ),

    # More semantic errors
    (
        "Server group member nickname not found",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: desc1\n"
                     "    members:\n"
                     "      - srv1\n",
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Nickname 'srv1' in server group 'grp1' not found"),
        None, True
    ),
    (
        "Default nickname not found",
        dict(
            sdf_yaml="servers:\n"
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
            exp_data=None,
        ),
        (ServerDefinitionFileFormatError,
         "Default nickname 'srv' not found"),
        None, True
    ),

    # Valid simple server definition files
    (
        "Valid file with no servers and server_group+default omitted",
        dict(
            sdf_yaml="servers: {}\n",
            exp_data={
                'servers': {},
                'server_groups': {},
                'default': None,
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one server that is default",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "default: srv1\n",
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
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one server and one server group that is default",
        dict(
            sdf_yaml="servers:\n"
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
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SDF_LOAD)
@simplified_test_function
def test_SDF_load(testcase, sdf_yaml, exp_data):
    """
    Test function for ServerDefinitionFile._load_server_definition_file()
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        # The code to be tested
        act_data = _load_server_definition_file(filepath)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert act_data == exp_data


TESTCASES_SDF_GET_SERVER = [

    # Testcases for ServerDefinitionFile.get_server()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * nick: nickname input parameter for get_server().
    #   * exp_attrs: Dict with expected attributes of ServerDefinition result
    #     of get_server(). Keys: attribute names; values: attribute values.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers; non-existing nickname",
        dict(
            sdf_yaml="servers: {}\n",
            nick='srv',
            exp_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server; non-existing nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n",
            nick='srv',
            exp_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; non-existing nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='srv',
            exp_attrs=None,
        ),
        (KeyError, "Server with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; existing server nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='srv1',
            exp_attrs=dict(
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
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='grp1',
            exp_attrs=None,
        ),
        (KeyError, "Server with nickname 'grp1' not found"),
        None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SDF_GET_SERVER)
@simplified_test_function
def test_SDF_get_server(testcase, sdf_yaml, nick, exp_attrs):
    """
    Test function for ServerDefinitionFile.get_server()
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        sdf = ServerDefinitionFile(filepath)

        # The code to be tested
        act_srv = sdf.get_server(nick)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        for name in exp_attrs:
            assert getattr(act_srv, name) == exp_attrs[name]


TESTCASES_SDF_LIST_SERVERS = [

    # Testcases for ServerDefinitionFile.list_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * nick: nickname input parameter for list_servers().
    #   * exp_srvs_attrs: List of dicts with expected attributes of
    #     ServerDefinition objects in the result of list_servers().
    #     Keys: attr names; values: attr values.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers; non-existing nickname",
        dict(
            sdf_yaml="servers: {}\n",
            nick='srv',
            exp_srvs_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server; non-existing nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n",
            nick='srv',
            exp_srvs_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; non-existing nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='srv',
            exp_srvs_attrs=None,
        ),
        (KeyError, "Server or server group with nickname 'srv' not found"),
        None, True
    ),
    (
        "One server group with one server; existing server nickname",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='srv1',
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            nick='grp1',
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            nick='grp1',
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            nick='grp2',
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            nick='grp2',
            exp_srvs_attrs=[
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
    TESTCASES_SDF_LIST_SERVERS)
@simplified_test_function
def test_SDF_list_servers(testcase, sdf_yaml, nick, exp_srvs_attrs):
    """
    Test function for ServerDefinitionFile.list_servers()
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        sdf = ServerDefinitionFile(filepath)

        # The code to be tested
        act_sds = sdf.list_servers(nick)

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_srvs_attrs) == len(act_sds)

        sorted_exp_srvs_attrs = sorted(
            exp_srvs_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_attrs in enumerate(sorted_exp_srvs_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_attrs:
                assert getattr(act_sd, name) == exp_attrs[name]


TESTCASES_SDF_LIST_DEFAULT_SERVERS = [

    # Testcases for ServerDefinitionFile.list_default_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * exp_srvs_attrs: List of dicts with expected attributes of
    #     ServerDefinition objects in the result of list_servers().
    #     Keys: attr names; values: attr values.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers, no default",
        dict(
            sdf_yaml="servers: {}\n",
            exp_srvs_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server; no default",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n",
            exp_srvs_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server; with default",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "default: srv1\n",
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            exp_srvs_attrs=[
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
    TESTCASES_SDF_LIST_DEFAULT_SERVERS)
@simplified_test_function
def test_SDF_list_default_servers(testcase, sdf_yaml, exp_srvs_attrs):
    """
    Test function for ServerDefinitionFile.list_default_servers()
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        sdf = ServerDefinitionFile(filepath)

        # The code to be tested
        act_sds = sdf.list_default_servers()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_srvs_attrs) == len(act_sds)

        sorted_exp_srvs_attrs = sorted(
            exp_srvs_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_attrs in enumerate(sorted_exp_srvs_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_attrs:
                assert getattr(act_sd, name) == exp_attrs[name]


TESTCASES_SDF_LIST_ALL_SERVERS = [

    # Testcases for ServerDefinitionFile.list_all_servers()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * exp_srvs_attrs: List of dicts with expected attributes of
    #     ServerDefinition objects in the result of list_servers().
    #     Keys: attr names; values: attr values.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "No servers",
        dict(
            sdf_yaml="servers: {}\n",
            exp_srvs_attrs=[],
        ),
        None, None, True
    ),
    (
        "One server",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n",
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    user_defined:\n"
                     "      stuff: 42\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    description: group1\n"
                     "    members:\n"
                     "      - srv1\n",
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            exp_srvs_attrs=[
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
            sdf_yaml="servers:\n"
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
            exp_srvs_attrs=[
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
    TESTCASES_SDF_LIST_ALL_SERVERS)
@simplified_test_function
def test_SDF_list_all_servers(testcase, sdf_yaml, exp_srvs_attrs):
    """
    Test function for ServerDefinitionFile.list_all_servers()
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        sdf = ServerDefinitionFile(filepath)

        # The code to be tested
        act_sds = sdf.list_all_servers()

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None, \
            "Expected exception not raised: {}". \
            format(testcase.exp_exc_types)

        assert len(exp_srvs_attrs) == len(act_sds)

        sorted_exp_srvs_attrs = sorted(
            exp_srvs_attrs, key=lambda x: x['nickname'])
        sorted_act_sds = sorted(act_sds, key=lambda x: x.nickname)
        for i, exp_attrs in enumerate(sorted_exp_srvs_attrs):
            act_sd = sorted_act_sds[i]
            for name in exp_attrs:
                assert getattr(act_sd, name) == exp_attrs[name]
