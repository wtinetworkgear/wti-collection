> CPM_DNSSERVICES_CONFIG    (/home/pi/.ansible/collections/ansible_collections/wti/remote/plugins/modules/cpm_dnsservices_config.py)

        Set network DNS Services parameters in WTI OOB and PDU devices

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

= dnsservers
        Actual DNS Server to send to the WTI device.

        elements: str
        type: list

- index
        Index in which DNS Server should be inserted. If not defined
        entry will start at position one.
        [Default: (null)]
        elements: int
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
        options used between CPM modules.


AUTHOR: Western Telematic Inc. (@wtinetworkgear)

EXAMPLES:

# Set Network DNS Services Parameters
- name: Set the an DNS Services Parameter for a WTI device
  cpm_dnsservices_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    dnsservers: "8.8.8.8"

# Set Network DNS Services Parameters using a User Token
- name: Set the an DNS Services Parameter for a WTI device
  cpm_dnsservices_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: ""
    cpm_password: "randomusertokenfromthewtidevice"
    use_https: true
    validate_certs: false
    dnsservers: "8.8.4.4"

# Sets multiple Network DNS Services Parameters
- name: Set the DNS Services Parameters a WTI device
  cpm_dnsservices_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    index:
      - 1
      - 2
    dnsservers:
      - "8.8.8.8"
      - "8.8.4.4"


RETURN VALUES:
- data
        The output JSON returned from the commands sent

        returned: always
        type: complex

        CONTAINS:

        - dnsservices
            Current k/v pairs of interface info for the WTI device
            after module execution.

            returned: always
            sample:
              servers:
              - dnsserver1:
                - ip: 166.216.138.41
                dnsserver2:
                - ip: 166.216.138.42
                dnsserver3:
                - ip: 8.8.8.8
                dnsserver4:
                - ip: ''
            
            type: dict
