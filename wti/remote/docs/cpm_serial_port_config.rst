.. _cpm_serial_port_config_module:


cpm_serial_port_config -- Set Serial port parameters in WTI OOB and PDU devices
===============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Set Serial port parameters in WTI OOB and PDU devices






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


  port (True, int, None)
    This is the port number that is getting the action performed on.


  portname (False, str, None)
    This is the Name of the Port that is displayed.


  baud (False, int, None)
    This is the baud rate to assign to the port.

    0=300, 1=1200, 2=2400, 3=4800, 4=9600, 5=19200, 6=38400, 7=57600, 8=115200, 9=230400, 10=460800


  handshake (False, int, None)
    This is the handshake to assign to the port, 0=None, 1=XON/XOFF, 2=RTS/CTS, 3=Both.


  stopbits (False, int, None)
    This is the stop bits to assign to the port, 1=1 Stop Bit, 2=2 Stop Bit.


  parity (False, int, None)
    This is the parity to assign to the port, 0=7-None, 1=7-Even, 2=7-Odd, 3=8-None, 4=8-Even, 5=8-Odd.


  mode (False, int, None)
    This is the port mode to assign to the port, 0=Any-to-Any. 1=Passive, 2=Buffer, 3=Modem, 4=ModemPPP.


  cmd (False, int, None)
    This is the Admin Mode to assign to the port, 0=Deny, 1=Permit.


  seq (False, int, None)
    This is the type of Sequence Disconnect to assign to the port, 1=Three Characters (before and after), 2=One Character Only, 3=Off


  tout (False, int, None)
    This is the Port Activity Timeout to assign to the port, 0=Off, 1=5 Min, 2=15 Min, 3=30 Min, 4=90 Min, 5=1 Min.


  echo (False, bool, None)
    -This is the command echo parameter to assign to the port, 0=Off, 1=On


  break_allow (False, bool, None)
    This is if the break character is allowed to be passed through the port, 0=Off, 1=On


  logoff (False, str, None)
    This is the logout character to assign to the port

    If preceded by a ^ character, the sequence will be a control character. Used if seq is set to 0 or 1





Notes
-----

.. note::
   - Use ``groups/cpm`` in ``module_defaults`` to set common options used between CPM modules.




Examples
--------

.. code-block:: yaml+jinja

    
    # Set Serial Port Parameters
    - name: Set the Port Parameters for port 2 of a WTI device
      cpm_serial_port_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: "2"
        portname: "RouterLabel"
        baud: "7"
        handshake: "1"
        stopbits: "1"
        parity: "0"
        mode: "0"
        cmd: "0"
        seq: "1"
        tout: "1"
        echo: "0"
        break_allow: "0"
        logoff: "^H"

    # Set Serial Port Port Name and Baud Rate Parameters
    - name: Set New port name and baud rate (115k) for port 4 of a WTI device
      cpm_serial_port_config:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false
        port: "4"
        portname: "NewPortName1"
        baud: "8"



Return Values
-------------

data (always, str, )
  The output JSON returned from the commands sent





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)

