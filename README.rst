secureserveraccess - Secure Server Access
=========================================

.. image:: https://badge.fury.io/py/secureserveraccess.svg
    :target: https://pypi.python.org/pypi/secureserveraccess/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/secureserveraccess/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/secureserveraccess/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/secureserveraccess/badge/?version=latest
    :target: https://readthedocs.org/projects/secureserveraccess/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/secureserveraccess/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/secureserveraccess?branch=master
    :alt: Test coverage (master)


Overview
--------

The **secureserveraccess** Python package is a library for retrieving the
secrets needed for accessing servers or services from an encrypted
`Ansible vault file`_ in YAML format.

The servers are identified with user-defined nicknames and the data structure
of the secrets for each server is completely user-defined. The password for the
Ansible vault file must be provided by the caller of the **secureserveraccess**
library. The documentation describes approaches for how the vault password can
be stored securely in CI systems and in keyring facilities.

An optional server definition file in YAML format is used to define some basic
information about the servers and to define groups of servers and a default
server or group. The servers and groups are identified using user-defined
nicknames. The Ansible vault file uses the same server nicknames to store the
secrets.

The end result is a convenient, flexible and secure way how your Python programs
can retrieve the secrets needed for accessing servers or services, while
protecting these secrets in a secure way. In addition, groups of servers can be
accessed for example to run automated tests against each server in the group.


.. _`Supported environments`:

Supported environments
----------------------

The **secureserveraccess** package is supported in these environments:

* Operating Systems: Linux, Windows (native, and with UNIX-like environments),
  macOS/OS-X

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

The following command installs the **secureserveraccess** package and its
prerequisite packages into the active Python environment:

.. code-block:: bash

    $ pip install secureserveraccess


.. _`Documentation and change log`:

Documentation and change log
----------------------------

* `Documentation`_
* `Change log`_


License
-------

The **secureserveraccess** project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/secureserveraccess/master/LICENSE>`_.


.. # Links:

.. _`Ansible vault file`: https://docs.ansible.com/ansible/latest/user_guide/vault.html
.. _`Documentation`: https://secureserveraccess.readthedocs.io/en/latest/
.. _`Change log`: https://secureserveraccess.readthedocs.io/en/latest/changes.html
