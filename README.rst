easy-server - Secure server access that is easy to use
======================================================

.. image:: https://badge.fury.io/py/easy-server.svg
    :target: https://pypi.python.org/pypi/easy-server/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/easy-server/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/easy-server/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/easy-server/badge/?version=latest
    :target: https://readthedocs.org/projects/easy-server/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/easy-server/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/easy-server?branch=master
    :alt: Test coverage (master)


Overview
--------

The **easy-server** package is a Python library for securely defining
sensitive information for accessing servers (or services), such as logon
credentials or API keys.

The information for accessing the servers is divided into a general portion
that is defined in an openly accessible *server file*, and
a sensitive portion that is defined in an encrypted *vault file*.

The vault file defines the secrets needed to access the servers, such as
logon credentials or API keys. The vault file must be an "easy-vault" file and
thus can be encrypted and decrypted using the ``easy-vault`` command provided
by the `easy-vault <https://easy-vault.readthedocs.io/en/latest/>`_ package.
The "easy-vault" files remain encrypted in the file system while their content
is used to access the servers.

The server file defines general information about the servers, such
as a short description, contact name, or a reminder which network to use for
accessing them.

The link between the server file and the vault file are user-defined
nicknames for the servers. These nicknames can also used by users as a
convenient way to identify servers in commands.

The server files support the definition of server groups that
also have a nickname.

Typical use cases for the **easy-server** package are test programs
running end-to-end tests against real servers, or command line clients that
access servers or services.

This provides a convenient, flexible and secure way how Python programs can
retrieve the secrets needed for accessing servers or services, while protecting
these secrets in a secure way.


.. _`Documentation and change log`:

Documentation and change log
----------------------------

* `Documentation`_
* `Change log`_


License
-------

The **easy-server** project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/easy-server/master/LICENSE>`_.


.. # Links:

.. _`Documentation`: https://easy-server.readthedocs.io/en/latest/
.. _`Change log`: https://easy-server.readthedocs.io/en/latest/changes.html
