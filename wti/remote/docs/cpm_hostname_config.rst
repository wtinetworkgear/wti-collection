
cpm_hostname_config -- Set Hostname (Site ID), Location, Asset Tag parameters in WTI OOB and PDU devices.
=========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set Hostname (Site ID), Location, Asset Tag parameters parameters in WTI OOB and PDU devices






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


  hostname (False, str, None)
    This is the Hostname (Site-ID) tag to be set for the WTI OOB and PDU device.


  location (False, str, None)
    This is the Location tag to be set for the WTI OOB and PDU device.


  assettag (False, str, None)
    This is the Asset Tag to be set for the WTI OOB and PDU device.





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Set Hostname, Location and Site-ID variables of a WTI device
    - name: Set known fixed hostname variables of a WTI device
      cpm_time_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        hostname: "myhostname"
        location: "Irvine"
        assettag: "irvine92395"

    # Set the Hostname variable of a WTI device
    - name: Set the Hostname of a WTI device
      cpm_time_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        hostname: "myhostname"



Return Values
-------------

  data (always, complex, )
    The output JSON returned from the commands sent

    timestamp (success, str, 2021-08-17T21:33:50+00:00)
      Current timestamp of the WTI device after module execution.

    hostname (success, str, myhostname)
      Current Hostname (Site-ID) of the WTI device after module execution.

    location (success, int, Irvine)
      Current Location of the WTI device after module execution.

    assettag (success, int, irvine92395)
      Current Asset Tag of the WTI device after module execution.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

