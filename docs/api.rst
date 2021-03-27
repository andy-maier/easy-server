.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _`API Reference`:

API Reference
=============

This section describes the API of the **secureserveraccess** package.


.. _`VaultFile class`:

VaultFile class
---------------

.. autoclass:: secureserveraccess.VaultFile
    :members:
    :autosummary:
    :autosummary-inherited-members:
    :special-members: __str__


.. _`ServerDefinitionFile class`:

ServerDefinitionFile class
--------------------------

.. autoclass:: secureserveraccess.ServerDefinitionFile
    :members:
    :autosummary:
    :autosummary-inherited-members:
    :special-members: __str__


.. _`ServerDefinition class`:

ServerDefinition class
----------------------

.. autoclass:: secureserveraccess.ServerDefinition
    :members:
    :autosummary:
    :autosummary-inherited-members:
    :special-members: __str__


.. _`Exception classes`:

Exception classes
-----------------

.. autoclass:: secureserveraccess.VaultFileException
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.VaultFileOpenError
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.VaultFileDecryptError
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.VaultFileFormatError
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.ServerDefinitionFileException
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.ServerDefinitionFileOpenError
    :members:
    :special-members: __str__

.. autoclass:: secureserveraccess.ServerDefinitionFileFormatError
    :members:
    :special-members: __str__


.. _`Package version`:

Package version
---------------

The package version can be accessed by programs using the
``secureserveraccess.__version__`` variable [#]_:

.. autodata:: secureserveraccess._version.__version__

This documentation may have been built from a development level of the
package. You can recognize a development version of this package by the
presence of a ".devD" suffix in the version string. Development versions are
pre-versions of the next assumed version that is not yet released. For example,
version 0.1.2.dev25 is development pre-version #25 of the next version to be
released after 0.1.1. Version 1.1.2 is an `assumed` next version, because the
`actually released` next version might be 0.2.0 or even 1.0.0.

.. [#] For tooling reasons, that variable is shown as
   ``secureserveraccess._version.__version__`` in this documentation, but
   it should be accessed as ``secureserveraccess.__version__``.
