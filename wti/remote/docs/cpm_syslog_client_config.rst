.. _cpm_syslog_client_config_module:


cpm_syslog_client_config -- Set network SYSLOG Client parameters in WTI OOB and PDU devices
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set network SYSLOG Client parameters in WTI OOB and PDU devices






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


  protocol (False, int, None)
    The protocol that the SYSLOG entry should be applied. 0 = ipv4, 1 = ipv6.


  clear (False, int, None)
    Removes all the IP block entries for the protocol being defined before setting the newly defined entries.


  index (False, list, None)
    Index of the IP block being modified.


  address (False, list, None)
    Sets the IP Address of the SYSLOG server to contact.


  port (False, list, None)
    Defines the port number used by the SYSLOG Client (1 - 65535).


  transport (False, list, None)
    Defines the transfer protocol type used by the SYSLOG Client. 0=UDP, 1=TCP;


  secure (False, list, None)
    Defines if a secure connection is used by the SYSLOG Client (TCP Transport required).





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Sets the device SYSLOG Client Parameters
    - name: Set the an SYSLOG Client Parameter for a WTI device
      cpm_iptables_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        protocol: 0
        index:
            - 1
        address:
            - "11.22.33.44"
        port:
            - 555
        transport:
            - 1
        secure:
            - 0

    # Sets the device SYSLOG Client Parameters
    - name: Set the SYSLOG Client Parameters a WTI device
      cpm_iptables_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        protocol: 0
        index:
            - 1
            - 2
        address:
            - "11.22.33.44"
            - "55.66.77.88"
        port:
            - 555
            - 557
        transport:
            - 1
            - 0
        secure:
            - 0
            - 1



Return Values
-------------

data (always, complex, )
  The output JSON returned from the commands sent


  syslogclient (always, dict, {'syslogclient': {'ietf-ipv4': {'clients': [{'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '1'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '2'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '3'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '4'}]}, 'ietf-ipv6': {'clients': [{'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '1'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '2'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '3'}, {'address': '', 'port': '514', 'transport': '0', 'secure': '0', 'index': '4'}]}}})
    Current k/v pairs of interface info for the WTI device after module execution.






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

