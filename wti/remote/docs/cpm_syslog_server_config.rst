.. _cpm_syslog_server_config_module:


cpm_syslog_server_config -- Set network SYSLOG Server parameters in WTI OOB and PDU devices
===========================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set network SYSLOG Server parameters in WTI OOB and PDU devices






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


  interface (True, list, None)
    The ethernet port for the SYSLOG we are defining.


  protocol (False, int, 0)
    The protocol that the SYSLOG entry should be applied. 0 = ipv4, 1 = ipv6.


  enable (False, int, None)
    Activates SYSLOG listening for the specified interface and protocol.


  port (False, int, None)
    Defines the port number used by the SYSLOG Server (1 - 65535).


  transport (False, int, None)
    Defines the transfer protocol type used by the SYSLOG Server. 0=UDP, 1=TCP;


  secure (False, int, None)
    Defines if a secure connection is used by the SYSLOG Server (TCP Transport required).


  clear (False, int, None)
    Removes all the IP block entries for the protocol being defined before setting the newly defined entries.


  index (False, list, None)
    Index of the IP block being modified.


  address (False, list, None)
    Sets the IP Address to block message logging.





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Sets the device SYSLOG Server Parameters
    - name: Set the an SYSLOG Server Parameter for a WTI device
      cpm_iptables_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        interface: "eth0"
        protocol: 0
        port: 514
        transport: 0
        secure: 0
        clear: 1

    # Sets the device SYSLOG Server Parameters
    - name: Set the SYSLOG Server Parameters a WTI device
      cpm_iptables_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        interface: "eth0"
        protocol: 0
        port: 514
        transport: 0
        secure: 0
        clear: 1
        index:
          - 1
          - 2
        block:
          - "192.168.50.4"
          - "72.76.4.56"



Return Values
-------------

data (always, complex, )
  The output JSON returned from the commands sent


  syslogserver (always, dict, {'syslogserver': {'eth0': [{'ietf-ipv4': {'block': [{'address': '', 'index': '1'}, {'address': '', 'index': '2'}, {'address': '', 'index': '3'}, {'address': '', 'index': '4'}], 'enable': 0, 'port': '514', 'secure': '0', 'transport': '0'}, 'ietf-ipv6': {'block': [{'address': '', 'index': '1'}, {'address': '', 'index': '2'}, {'address': '', 'index': '3'}, {'address': '', 'index': '4'}], 'enable': 0, 'port': '514', 'secure': '0', 'transport': '0'}}]}})
    Current k/v pairs of interface info for the WTI device after module execution.






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

