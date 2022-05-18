.. _cpm_config_backup_module:


cpm_config_backup -- Get parameters from WTI OOB and PDU devices
================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get parameters from WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to get the parameters from.


  cpm_username (True, str, None)
    This is the Username of the WTI device to get the parameters from.


  cpm_password (True, str, None)
    This is the Password of the WTI device to get the parameters from.


  cpm_path (False, str, /tmp/)
    This is the directory path to store the WTI device configuration file.


  use_https (False, bool, True)
    Designates to use an https connection or http connection.


  validate_certs (False, bool, True)
    If false, SSL certificates will not be validated. This should only be used

    on personally controlled sites using self-signed certificates.


  use_proxy (False, bool, False)
    Flag to control if the lookup will observe HTTP proxy environment variables when present.





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.)




Examples
--------

.. code-block:: yaml+jinja

    
    -   name: Get the Parameters for a WTI device
        cpm_config_backup:
            cpm_url: "nonexist.wti.com"
            cpm_username: "super"
            cpm_password: "super"
            use_https: true
            validate_certs: false



Return Values
-------------

data (always, complex, )
  The XML configuration of the WTI device queried


  status (success, list, [{'code': 0, 'savedfilename': '/tmp/wti-192-10-10-239-2020-02-13T16-05-57.xml', 'text': 'ok'}])
    List of status returns from backup operation






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

