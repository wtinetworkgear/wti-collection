> CPM_WEB_CONFIG    (/home/pi/.ansible/collections/ansible_collections/wti/remote/plugins/modules/cpm_web_config.py)

        Set network WEB parameters in WTI OOB and PDU devices

OPTIONS (= is mandatory):

= cpm_password
        This is the Password of the WTI device to send the module. If
        the
        cpm_username is blank, this parameter is presumed to be a User
        Token.

        type: str

= cpm_url
        This is the URL of the WTI device to send the module.

        type: str

- cpm_username
        This is the Username of the WTI device to send the module. If
        this value
        is blank, then the cpm_password is presumed to be a User
        Token.
        [Default: (null)]
        type: str

- harden
        Security level for the WEB the device will respond to 0 = Off,
        1 = Medium, 2 = High.
        (Choices: 0, 1, 2)[Default: (null)]
        type: int

- hsts
        If HTTP Strict Transport Security (HSTS) is enabled/disabled
        for the WEB.
        (Choices: 0, 1)[Default: (null)]
        type: int

- httpenable
        Activates unsecure WEB for the specified interface.
        (Choices: 0, 1)[Default: (null)]
        type: int

- httpport
        Port used by the insecure WEB.
        [Default: (null)]
        type: int

- httpsenable
        Activates secure WEB for the specified interface.
        (Choices: 0, 1)[Default: (null)]
        type: int

- httpsport
        Port used by the secure WEB.
        [Default: (null)]
        type: int

- inter_filename
        Intermediate Certificate to be assigned to the Device.
        [Default: (null)]
        type: str

= interface
        The ethernet port for the SNMP we are defining.
        (Choices: eth0, eth1, ppp0, qmimux0)
        type: str

- ocsp
        Current state of the Online Certificate Status Protocol (OCSP)
        for the Web Server.
        (Choices: 0, 1)[Default: (null)]
        type: int

- private_filename
        Private Certificate to be assigned to the Device.
        [Default: (null)]
        type: str

- signed_filename
        Signed Certificate to be assigned to the Device.
        [Default: (null)]
        type: str

- timeout
        Inactivity timeout of a user when logged into the web server
        (valid from 0 to 9999 minutes) 0 is no timeout.
        [Default: (null)]
        type: int

- tlsmode
        Which TLS the WEB will use 0 = TLSv1.1, 1 = TLSv1.1/TLSv1.2, 2
        = TLSv1.2/TLSv1.3, 3 = TLSv1.3
        (Choices: 0, 1, 2, 3)[Default: (null)]
        type: int

- trace
        Current state of TRACE requests for thw Web Server.
        (Choices: 0, 1)[Default: (null)]
        type: int

- use_https
        Designates to use an https connection or http connection.
        [Default: True]
        type: bool

- use_proxy
        Flag to control if the lookup will observe HTTP proxy
        environment variables when present.
        [Default: False]
        type: bool

- validate_certs
        If false, SSL certificates will not be validated. This should
        only be used
        on personally controlled sites using self-signed certificates.
        [Default: True]
        type: bool

- webterm
        Current state of the CLI over Web for the Web Server.
        (Choices: 0, 1)[Default: (null)]
        type: int


NOTES:
      * Use `groups/cpm' in `module_defaults' to set common
        options used between CPM modules.


AUTHOR: Western Telematic Inc. (@wtinetworkgear)

EXAMPLES:

# Sets the device WEB Parameters
- name: Set the an WEB Parameter for a WTI device
  cpm_snmp_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    interface: "eth0"
    use_https: true
    validate_certs: false
    private_filename: "/tmp/private.key"
    signed_filename:  "/tmp/signed.key"
    inter_filename:   "/tmp/intermediate.key"

# Sets the device WEB Parameters using a User Token
- name: Set the an WEB Parameter for a WTI device
  cpm_snmp_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: ""
    cpm_password: "randomusertokenfromthewtidevice"
    interface: "eth0"
    use_https: true
    validate_certs: false

# Sets the device WEB Parameters
- name: Set the WEB Parameters a WTI device
  cpm_snmp_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false


RETURN VALUES:
- data
        The output JSON returned from the commands sent

        returned: always
        type: complex

        CONTAINS:

        - ocsp
            Current state of the Online Certificate Status Protocol
            (OCSP) for the Web Server.

            returned: success
            sample: 1
            
            type: int

        - timeout
            Inactivity timeout of a user. (valid from 0 to 9999
            minutes) 0 is no timeout.

            returned: success
            sample: 0
            
            type: int

        - totalports
            Total port being returned from the current call.

            returned: success
            sample: 1
            
            type: int

        - trace
            Current state of TRACE requests for the Web Server.

            returned: success
            sample: 0
            
            type: int

        - web
            Current k/v pairs of Web info for the WTI device after
            module execution.

            returned: always
            sample:
            - harden: '2'
              hsts: '0'
              httpenable: '1'
              httpport: '80'
              httpsenable: '1'
              httpsport: '443'
              name: eth0
              tlsmode: '2'
            
            type: dict

        - webterm
            Current state of the CLI over Web for the Web Server.

            returned: success
            sample: 0
            
            type: int
