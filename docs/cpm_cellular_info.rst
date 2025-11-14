.. _cpm_cellular_info_module:


cpm_cellular_info -- Get Cellular runtime information and Parameters from WTI OOB and PDU devices
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get Cellular runtime information and Parameters from WTI OOB and PDU devices






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

    
    - name: Get the Cellular runtime information and Parameters of the device
      cpm_cellular_info:
        cpm_url: "nonexist.wti.com"
        cpm_username: "super"
        cpm_password: "super"
        use_https: true
        validate_certs: false




Return Values
-------------

data (always, complex, )
  The output JSON returned from the commands sent


  apn (success, str, MA44.VZWSTATIC)
    APN for the cellular modem in the WTI device.


  cellenable (success, int, 1)
    If the cellular modem is enabled in the WTI device.


  cellstatus (always, dict, {"enabled": "0", "active": "0", "autorecov": "0", "gatewayport": "0", "sleepmode": "0", "singlepingaddfail": "0", "interfacemon": "0", "host1": "", "host2": "", "pinginter1": "60", "afppinginter1": "10", "conscfail1": "5", "gatewayaddr": ""})
    Current k/v pairs of Cellular status of the WTI device.


  wof (always, dict, {"enabled": 0, "active": 0, "autorecov": 0, "gatewayport": 0, "sleepmode": 0, "singlepingaddfail": 0, "interfacemon": 0, "host1": "", "host2": "", "pinginter1": 60, "afppinginter1": 10, "conscfail1": 5, "gatewayaddr": ""})
    Current k/v pairs of Wakeup On Fail status of the WTI device.


  passth (always, dict, { "enabled": 0, "active": 0, "interfacemon": 1, "mac": "", "httptermenable": 0, "httpterm": 80, "httpstermenable": 0, "httpsterm": 443, "sshtermenable": 1, "sshterm": 22 })
    Current k/v pairs of IP Passthrough status of the WTI device.


  modresp (always, dict, { "CGSN": "350344984005569", "ICCID": "89148000005529784167", "FWSWITCH": "1,1", "CEMODE": "2", "CALLDISA": "0,0", "CGDCONT": "OK", "QCPDPP": "", "CGREG": "0,1", "COPS": "0,0,'Verizon ',7", "COPSCARRIER": "Verizon ", "COPSSERVICE": "4G/LTE", "CSQ": "31,3", "CGMI": "Telit", "CGMM": "LE910C4-NF", "CGMR": "M0F.660006", "CNUM": "'Line 1','+19495753478',145", "GCAP": "+CGSM,+DS,+MS", "CGATT": "1", "APN_CEREG": "", "APN_CGREG": "", "APN_CREG": "" })
    Current k/v pairs of Modem response status of the WTI device.


  signal (always, dict, { "rssi": "-60 dBm", "rsrp": "-95 dBm", "rsrq": "-14 dB", "snr": "4.4 dB", "radiointerface": "LTE", "bandclass": "EUTRAN-4", "band": 4, "frequency": 1700, "channel": 2100 })
    Current k/v pairs of Signal Quality status of the WTI device.






Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Western Telematic Inc. (@wtinetworkgear)
