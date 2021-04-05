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


.. _`Change log`:

Change log
==========


Version 0.7.0.dev1
------------------

Released: not yet

**Incompatible changes:**

* The 'VaultFile' class now raises 'VaultFileOpenError' for vault file
  not found. Previously, it raised 'easy_vault.EasyVaultFileError'
  (related to issue #10)

**Deprecations:**

**Bug fixes:**

* Added missing exception transformation to 'VaultFileOpenError' for vault file
  not found in 'VaultFile' class. (related to issue #10)

**Enhancements:**

* Docs: Updated usage example and example scripts to use integrated vault.
  (issue #26)

* In 'VaultFile' class, the input 'filepath' is now made absolute.
  (related to issue #10)

* Added a method 'VaultFile.is_encrypted()' to return whether the
  vault file, is encrypted.

* Added a method 'ServerFile.is_vault_file_encrypted()' to return whether the
  vault file of the server file (if any) is encrypted.

* Improved text coverage of 'VaultFile' class. (issue #10)

* Increased minimum version of easy-vault package to 0.7.0. (issue #40)

**Cleanup:**

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/andy-maier/easy-server/issues


Version 0.6.0
-------------

Released: 2021-04-02

**Incompatible changes:**

* The new optional 'use_prompting' parameter of the 'VaultFile' and
  'ServerDefinitionFile' classes was not added at the end of the parameter list.
  This is incompatible for users who called the function with positional
  arguments. (related to issue #22)

* Renamed the following classes for simplicity:
  'ServerDefinitionFile' to 'ServerFile',
  'ServerDefinition' to 'Server',
  'ServerDefinition...' exceptions to 'Server...'

**Enhancements:**

* Integrated vault access into server definition file. The server definition
  files can now optionally specify the path name of a vault file. If specified,
  the vault file is loaded as well and the secrets for a server defined in
  the vault file are available in the ServerDefinition object as a new `secrets`
  property. (issue #20)

* In the 'VaultFile' and 'ServerDefinitionFile' classes, added a new parameter
  'use_prompting' that allows disabling the interactive prompting for passwords.
  Also, changed the logic for requiring passwords such that they are only
  required when the vault file is being encrypted, decrypted or accessed in the
  encrypted state. (issue #22)


Version 0.5.0
-------------

Released: 2021-03-29

Initial release.
