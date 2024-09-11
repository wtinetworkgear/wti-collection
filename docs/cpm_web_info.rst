> CPM_WEB_INFO    (/home/pi/.ansible/collections/ansible_collections/wti/remote/plugins/modules/cpm_web_info.py)

        Get network Web parameters from WTI OOB and PDU devices

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

- include_certs
        If true, will return the Signed, Private and Intermediate Keys
        from the WTI device.
        [Default: False]
        type: bool

- interface
        This is the ethernet port name that is getting retrieved. It
        can include a single ethernet
        port name, multiple ethernet port names separated by commas or
        not defined for all ports.
        (Choices: eth0, eth1, ppp0, qmimux0)[Default: (null)]
        elements: str
        type: list

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


NOTES:
      * Use `groups/cpm' in `module_defaults' to set common
        options used between CPM modules.)


AUTHOR: Western Telematic Inc. (@wtinetworkgear)

EXAMPLES:

- name: Get the network Web Parameters for all interfaces of a WTI device.
  cpm_web_info:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false

- name: Get the network Web Parameters for all interfaces of a WTI device using a User Token.
  cpm_web_info:
    cpm_url: "nonexist.wti.com"
    cpm_username: ""
    cpm_password: "randomusertokenfromthewtidevice"
    use_https: true
    validate_certs: false

- name: Get the network Web Parameters for eth0 of a WTI device, include the certificates in the response.
  cpm_web_info:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    include_certs: true
    use_https: false
    validate_certs: false
    interface: "eth0"


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

        - totalports
            Total port being returned from the current call.

            returned: success
            sample: 1
            
            type: int

        - trace
            Current state of TRACE requests for thw Web Server.

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
