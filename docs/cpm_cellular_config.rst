> WTI.REMOTE.CPM_CELLULAR_CONFIG    (./wti/remote/plugins/modules/cpm_cellular_config.py)

        Set  Cellular runtime information and Parameters of the WTI
        device

ADDED IN: version 2.10.0 of wti.remote

OPTIONS (= is mandatory):

- apn
        APN for the cellular modem in the WTI device.
        default: null
        type: str

- cellenable
        If the cellular modem is enabled in the WTI device.
        choices: [0, 1]
        default: null
        type: int

= cpm_password
        This is the Password of the WTI device to send the module.
        type: str

= cpm_url
        This is the URL of the WTI device to send the module.
        type: str

= cpm_username
        This is the Username of the WTI device to send the module.
        type: str

- ipthru_enabled
        Enables/disables the IP Passthrough feature.
        choices: [0, 1]
        default: null
        type: int

- ipthru_httpsterm
        When IP Passthrough is enabled, the Cellular HTTPS Port will
        be incremented by 5000.
        default: null
        type: int

- ipthru_httpstermenable
        Enables/disables HTTPS.
        default: null
        type: int

- ipthru_httpterm
        When IP Passthrough is enabled, the Cellular HTTP Port will be
        incremented by 5000.
        default: null
        type: int

- ipthru_httptermenable
        Enables/disables HTTP.
        default: null
        type: int

- ipthru_interfacemon
        Selects the interface that your downstream device/router will
        be connected to.
        default: null
        type: int

- ipthru_mac
        The MAC address of your downstream device/router.
        default: null
        type: str

- ipthru_sshterm
        When IP Passthrough is enabled, the Cellular SSH Port will be
        incremented by 5000.
        default: null
        type: int

- ipthru_sshtermenable
        Enables/disables SSH.
        default: null
        type: int

- use_https
        Designates to use an https connection or http connection.
        default: true
        type: bool

- use_proxy
        Flag to control if the lookup will observe HTTP proxy
        environment variables when present.
        default: false
        type: bool

- validate_certs
        If false, SSL certificates will not be validated. This should
        only be used
        on personally controlled sites using self-signed certificates.
        default: true
        type: bool

- wof_afppinginter1
        Determines how often the Ping command will be sent after a
        previous Ping command receives no response.
        default: null
        type: int

- wof_autorecov
        When enabled, the cellular modem will automatically be put
        back into sleep state when failure is resolved.
        default: null
        type: int

- wof_conscfail1
        Determines how many consecutive failures pings must be
        detected in order to initiate a Wakeup on Failure..
        default: null
        type: int

- wof_enabled
        Enables/disables the Wakeup on Failure feature.
        choices: [0, 1]
        default: null
        type: int

- wof_gatewayaddr
        When the cellular modem is defined as the default gateway,
        this determines which interface will be the default gateway.
        default: null
        type: str

- wof_gatewayport
        The Ethernet port that will be used as the default gateway
        when the cellular modem is in the sleep state.
        default: null
        type: int

- wof_host1
        Selects the primary host that will be pinged in order to test
        for failures.
        default: null
        type: str

- wof_host2
        Selects the secondary host that will be pinged in order to
        test for failures.
        default: null
        type: str

- wof_interfacemon
        Selects the Ethernet interface(s) that will be monitored for
        failed ping responses.
        default: null
        type: int

- wof_pinginter1
        Determines how often the selected IP Address will be pinged.
        default: null
        type: int

- wof_singlepingaddfail
        After an Ethernet failure has triggered a Wakeup, this feature
        is used to manually re-enable Wakeup On Failure.
        default: null
        type: int

- wof_sleepmode
        Determines whether the cell modem will be attached or detached
        from the cell tower when sleep mode is active.
        default: null
        type: int


NOTES:
      * Use `groups/cpm' in `module_defaults' to set common
        options used between CPM modules.


AUTHOR: Western Telematic Inc. (@wtinetworkgear)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community

EXAMPLES:

# Set a static time/date and timezone of a WTI device
- name: Set APN and enable cellular modem in a WTI device
  cpm_time_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    apn: "vzwent.south"
    cellenable: "1"


RETURN VALUES:
- data
        The output JSON returned from the commands sent
        returned: always
        type: complex

        CONTAINS:

        - apn
            APN for the cellular modem in the WTI device.
            returned: success
            sample: MA44.VZWSTATIC
            type: str

        - cellenable
            If the cellular modem is enabled in the WTI device.
            returned: success
            sample: '1'
            type: str

        - cellstatus
            Current k/v pairs of Cellular status of the WTI device.
            returned: always
            sample:
              IMEI: '240324263004458'
              attached: '1'
              band: 4G/LTE
              carrier: Verizon
              phonenumber: '+19495551212'
              sessionest: '1'
              signalquality: '31'
            type: dict

        - modresp
            Current k/v pairs of Cellular Modem Response info of the
            WTI device.
            returned: always
            sample:
              APN_CEREG: ''
              APN_CGREG: ''
              APN_CREG: ''
              CALLDISA: 0,0
              CEMODE: '2'
              CGATT: '1'
              CGDCONT: OK
              CGMI: Telit
              CGMM: LE910C4-NF
              CGMR: M0F.660006
              CGREG: 0,1
              CGSN: '250322873004469'
              CNUM: '''Line 1'',''+19495753478'',145'
              COPS: 0,0,'Verizon ',7
              COPSCARRIER: Verizon
              COPSSERVICE: 4G/LTE
              CSQ: 31,3
              FWSWITCH: 1,1
              GCAP: +CGSM,+DS,+MS
              ICCID: '89038000004428783156'
              QCPDPP: ''
            type: dict

        - passth
            Current k/v pairs of IP Passthrough of the WTI device.
            returned: always
            sample:
              active: '0'
              enabled: '0'
              host2: ''
              httpsterm: '443'
              httpstermenable: '0'
              httpterm: '80'
              httptermenable: '0'
              interfacemon: '0'
              mac: ''
              sshterm: '22'
              sshtermenable: '0'
            type: dict

        - signal
            Current k/v pairs of CEllular Signal info of the WTI
            device.
            returned: always
            sample:
              band: '4'
              bandclass: EUTRAN-4
              channel: '2100'
              frequency: '1700'
              radiointerface: LTE
              rsrp: -96 dBm
              rsrq: -12 dB
              rssi: -62 dBm
              snr: 6.6 dB
            type: dict

        - wof
            Current k/v pairs of Wake up on Failure info of the WTI
            device.
            returned: always
            sample:
              active: '0'
              afppinginter1: '10'
              autorecov: '0'
              conscfail1: '5'
              enabled: '0'
              gatewayaddr: ''
              gatewayport: '0'
              host1: ''
              host2: ''
              interfacemon: '0'
              pinginter1: '60'
              singlepingaddfail: '0'
              sleepmode: '0'
            type: dict
