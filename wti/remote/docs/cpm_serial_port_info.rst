.. _cpm_serial_port_info_module:


cpm_serial_port_info -- Get Serial port parameters in WTI OOB and PDU devices
=============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get Serial port parameters from WTI OOB and PDU devices






Parameters
----------

  cpm_url (True, str, None)
    This is the URL of the WTI device to send the module.


  cpm_username (True, str, None)
    This is the Username of the WTI device to send the module.


  cpm_password (True, str, None)
    This is the Password of the WTI device to send the module.


  use_https (False, bool, False)
    Designates to use an https connection or http connection.


  validate_certs (False, bool, False)
    If false, SSL certificates will not be validated. This should only be used

    on personally controlled sites using self-signed certificates.


  use_proxy (False, bool, False)
    Flag to control if the lookup will observe HTTP proxy environment variables when present.


  port (False, list, ['*'])
    This is the serial port number that is getting retrieved. It can include a single port

    number, multiple port numbers separated by commas, a list of port numbers, or an '*' character for all ports.





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.)




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get the Serial Port Parameters for port 2 of a WTI device
      cpm_serial_port_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: 2

    - name: Get the Serial Port Parameters for ports 2 and 4 of a WTI device
      cpm_serial_port_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: 2,4

    - name: Get the Serial Port Parameters for all ports of a WTI device
      cpm_serial_port_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: "*"



Return Values
-------------

data (always, complex, )
  The output JSON returned from the commands sent


  serialports (success, list, [{'baud': 4, 'break': 1, 'cmd': 1, 'connstatus': 'Free', 'echo': 1, 'handshake': 2, 'logoff': '^X', 'mode': 1, 'parity': 3, 'port': 2, 'portname': 'switch', 'seq': 2, 'stopbits': 1, 'tout': 0}, {'baud': 3, 'break': 1, 'cmd': 1, 'connstatus': 'Free', 'echo': 1, 'handshake': 2, 'logoff': '^X', 'mode': 1, 'parity': 1, 'port': 4, 'portname': 'router', 'seq': 2, 'stopbits': 1, 'tout': 1}])
    List of data for each serial port






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

