secure-server-access - Secure Server Access
===========================================

.. image:: https://badge.fury.io/py/secure-server-access.svg
    :target: https://pypi.python.org/pypi/secure-server-access/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/secure-server-access/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/secure-server-access/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/secure-server-access/badge/?version=latest
    :target: https://readthedocs.org/projects/secure-server-access/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/secure-server-access/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/secure-server-access?branch=master
    :alt: Test coverage (master)


Overview
--------

The **secure-server-access** package is a library for retrieving the information
needed for accessing servers (or service), such as IP address, logon credentials,
or informal information such as contact name or which network to use.

The information for accessing the servers is divided into an open part that is
defined in a *server definition file*, and a protected part containing the
secrets for the actual access that is defined in a *vault file*. The vault file
can be encrypted and decrypted using the ``easy-vault`` command provided by the
`easy-vault <https://easy-vault.readthedocs.io/en/latest/>`_ package.

The server definition file defines nicknames for the servers and allows grouping
them into groups that also have nicknames.

The **secure-server-access** package is not used by end users, but by programs
that integrate with it, such as test programs or command line clients that
access servers or services. The users of these programs can then access
servers or services by means of the server and group nicknames that are defined.

The secrets needed to access the servers remain in the vault file which remains
encrypted in teh file system while the server is accessed.

This provides a convenient, flexible and secure way how your Python programs
can retrieve the secrets needed for accessing servers or services, while
protecting these secrets in a secure way.


.. _`Documentation and change log`:

Documentation and change log
----------------------------

* `Documentation`_
* `Change log`_


License
-------

The **secure-server-access** project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/secure-server-access/master/LICENSE>`_.


.. # Links:

.. _`Documentation`: https://secure-server-access.readthedocs.io/en/latest/
.. _`Change log`: https://secure-server-access.readthedocs.io/en/latest/changes.html
