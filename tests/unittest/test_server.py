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
Test the _server.py module.
"""

from __future__ import absolute_import, print_function
import pytest
from easy_server import Server

from ..utils.simplified_test_function import simplified_test_function


TESTCASES_SERVER_INIT = [

    # Testcases for Server.__init__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to Server().
    #   * init_kwargs: Dict of keyword arguments to Server().
    #   * exp_attrs: Dict with expected Server attributes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic parameter checking
    (
        "Order of positional parameters",
        dict(
            init_args=(
                'myserver',
                {
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                {
                    'host': 'myhost',
                },
            ),
            init_kwargs=dict(),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': 'my contact',
                'access_via': 'my vpn',
                'user_defined': {'stuff': 42},
                'secrets': {'host': 'myhost'},
            },
        ),
        None, None, True
    ),
    (
        "Names of keyword arguments",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': 'my contact',
                'access_via': 'my vpn',
                'user_defined': {'stuff': 42},
                'secrets': {'host': 'myhost'},
            },
        ),
        None, None, True
    ),

    # Omitted init parameters
    (
        "Omitted required parameter: description",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
            exp_attrs=None,
        ),
        KeyError, None, True
    ),
    (
        "Omitted optional parameter: contact_name",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': None,
                'access_via': 'my vpn',
                'user_defined': {'stuff': 42},
                'secrets': {'host': 'myhost'},
            },
        ),
        None, None, True
    ),
    (
        "Omitted optional parameter: access_via",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': 'my contact',
                'access_via': None,
                'user_defined': {'stuff': 42},
                'secrets': {'host': 'myhost'},
            },
        ),
        None, None, True
    ),
    (
        "Omitted optional parameter: user_defined",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': 'my contact',
                'access_via': 'my vpn',
                'user_defined': None,
                'secrets': {'host': 'myhost'},
            },
        ),
        None, None, True
    ),
    (
        "No secrets (None)",
        dict(
            init_args=(),
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict=None,
            ),
            exp_attrs={
                'nickname': 'myserver',
                'description': 'my description',
                'contact_name': 'my contact',
                'access_via': 'my vpn',
                'user_defined': {'stuff': 42},
                'secrets': None,
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SERVER_INIT)
@simplified_test_function
def test_Server_init(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test function for Server.__init__()
    """

    # The code to be tested
    act_obj = Server(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None, \
        "Expected exception not raised: {}". \
        format(testcase.exp_exc_types)

    for attr_name in exp_attrs:
        exp_attr_value = exp_attrs[attr_name]
        assert hasattr(act_obj, attr_name), \
            "Missing attribute {0!r} in returned Server object". \
            format(attr_name)
        act_attr_value = getattr(act_obj, attr_name)
        assert act_attr_value == exp_attr_value, \
            "Unexpected value for attribute {0!r}: Expected {1!r}, got {2!r}".\
            format(attr_name, exp_attr_value, act_attr_value)


TESTCASES_SERVER_REPR = [

    # Testcases for Server.__repr__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_kwargs: Dict of keyword arguments to Server().
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    (
        "All parameters set",
        dict(
            init_kwargs=dict(
                nickname='myserver',
                server_dict={
                    'description': 'my description',
                    'contact_name': 'my contact',
                    'access_via': 'my vpn',
                    'user_defined': {'stuff': 42},
                },
                secrets_dict={
                    'host': 'myhost',
                },
            ),
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SERVER_REPR)
@simplified_test_function
def test_Server_repr(testcase, init_kwargs):
    """
    Test function for Server.__repr__()
    """

    obj = Server(**init_kwargs)

    repr_str = repr(obj)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None, \
        "Expected exception not raised: {}". \
        format(testcase.exp_exc_types)

    assert "Server(" in repr_str
    assert "nickname=" in repr_str
    assert "description=" in repr_str
    assert "contact_name=" in repr_str
    assert "access_via=" in repr_str
    assert "user_defined=" in repr_str
    assert "secrets=" in repr_str
