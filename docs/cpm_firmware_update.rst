.. _cpm_firmware_update_module:


cpm_firmware_update -- Update firmware in WTI OOB and PDU devices
============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Update firmware in WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to send the module.


  cpm_username (True, str, None)
    This is the Username of the WTI device to send the module.


  cpm_password (True, str, None)
    This is the Password of the WTI device to send the module.


  cpm_path (False, str, /tmp/)
    This is the directory path to store the WTI device configuration file.


  cpm_file (False, str, None)
    If a file is defined, this file will be used to update the WTI device.


  use_force (False, bool, False)
    If set to True, the upgrade will happen even if the device doesnt need it.


  use_https (False, bool, True)
    Designates to use an https connection or http connection.


  validate_certs (False, bool, True)
    If false, SSL certificates will not be validated. This should only be used - on personally controlled sites using self-signed certificates.


  use_proxy (False, bool, False)
    Flag to control if the lookup will observe HTTP proxy environment variables when present.


  family (False, int, 1)
    Force the download to both either Console (1) or Power (0)


  removefileonexit (False, int, 1)
    After an upgrade, remove the upgrade OS image





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Upgrade the firmware of a WTI device
    - name: Upgrade the firmware of a WTI device
      cpm_firmware_update:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false


    # Upgrade the firmware of a WTI device and keep the download OS image after exit
    - name: Upgrade the firmware of a WTI device and keep the download OS image after exit
      cpm_firmware_update:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        removefileonexit: "0"



Return Values
-------------

data (always, complex, )
  The output XML configuration of the WTI device being updated


  filelength (success, int, [{'filelength': 329439}])
    Length of the file uploaded in bytes


  status (success, list, [{'code': 0}, {'text': 'ok'}, {'unittimestamp': '2020-02-14T00:18:57+00:00'}])
    List of status returns from backup operation






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

