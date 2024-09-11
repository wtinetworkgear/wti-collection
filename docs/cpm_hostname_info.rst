.. _cpm_hostname_info_module:


cpm_hostname_info -- Get Hostname (Site ID), Location, Asset Tag parameters in WTI OOB and PDU devices
======================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get Hostname (Site ID), Location, Asset Tag parameters from WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to send the module.


  cpm_username (True, str, None)
    This is the Username of the WTI device to send the module.


  cpm_password (True, str, None)
    This is the Password of the WTI device to send the module.


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

    
    - name: Get the Hostname parameters for a WTI device
      cpm_hostname_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false

    - name: Get the Hostname parameters for a WTI device
      cpm_hostname_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: false
        validate_certs: false



Return Values
-------------

data (always, complex, )
  The output JSON returned from the commands sent


  timestamp (success, str, 2021-08-17T21:33:50+00:00)
    Current timestamp of the WTI device after module execution.


  siteid (success, str, myhostname)
    Current Site ID of the WTI device.


  location (success, str, Irvine)
    Current Location of the WTI device.


  hostname (success, str, myhostname)
    Current Hostname of the WTI device.


  domain (success, str, myhostname)
    Current Domain of the WTI device.


  assettag (success, str, irvine92395)
    Current Asset Tag of the WTI device.






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

