#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) 2019 Red Hat Inc.
# Copyright (C) 2025 Western Telematic Inc.
#
# GNU General Public License v3.0+
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Module to retrieve WTI Cellular runtime and Parameters from WTI OOB and PDU devices.
# CPM remote_management
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: cpm_cellular_info
version_added: "2.10.0"
author:
    - "Western Telematic Inc. (@wtinetworkgear)"
short_description: Get Cellular runtime information and Parameters in WTI OOB and PDU devices
description:
    - "Get Cellular runtime information and Parameters from WTI OOB and PDU devices"
options:
    cpm_url:
        description:
            - This is the URL of the WTI device to send the module.
        type: str
        required: true
    cpm_username:
        description:
            - This is the Username of the WTI device to send the module.
        type: str
        required: true
    cpm_password:
        description:
            - This is the Password of the WTI device to send the module.
        type: str
        required: true
    use_https:
        description:
            - Designates to use an https connection or http connection.
        type: bool
        required: false
        default: true
    validate_certs:
        description:
            - If false, SSL certificates will not be validated. This should only be used
            - on personally controlled sites using self-signed certificates.
        type: bool
        required: false
        default: true
    use_proxy:
        description:
            - Flag to control if the lookup will observe HTTP proxy environment variables when present.
        type: bool
        required: false
        default: false
notes:
 - Use C(groups/cpm) in C(module_defaults) to set common options used between CPM modules.)
"""

EXAMPLES = """
- name: Get the Cellular runtime information and Parameters of the device
  cpm_cellular_info:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
"""

RETURN = """
data:
  description: The output JSON returned from the commands sent
  returned: always
  type: complex
  contains:
    apn:
      description: APN for the cellular modem in the WTI device.
      returned: success
      type: str
      sample: "MA44.VZWSTATIC"
    cellenable:
      description: If the cellular modem is enabled in the WTI device.
      returned: success
      type: str
      sample: "1"
    cellstatus:
      description: Current k/v pairs of Cellular status of the WTI device.
      returned: always
      type: dict
      sample: {"phonenumber": "+19495551212", "IMEI": "240324263004458", "carrier": "Verizon",
               "band": "4G/LTE", "signalquality": "31", "attached": "1", "sessionest": "1"}
    wof:
      description: Current k/v pairs of Wake up on Failure info of the WTI device.
      returned: always
      type: dict
      sample: {"enabled": "0", "active": "0", "autorecov": "0", "autorecov": "0", "gatewayport": "0",
              "sleepmode": "0", "singlepingaddfail": "0", "interfacemon": "0", "host1": "", "host2": "",
              "pinginter1": "60", "afppinginter1": "10", "conscfail1": "5", "gatewayaddr": ""}
    passth:
      description: Current k/v pairs of IP Passthrough of the WTI device.
      returned: always
      type: dict
      sample: {"enabled": "0", "active": "0", "interfacemon": "0", "mac": "", "httptermenable": "0",
              "httpterm": "80", "httpstermenable": "0", "httpsterm": "443", "sshtermenable": "0", "host2": "",
              "sshterm": "22"}
    modresp:
      description: Current k/v pairs of Cellular Modem Response info of the WTI device.
      returned: always
      type: dict
      sample: {"CGSN": "250322873004469", "ICCID": "89038000004428783156", "FWSWITCH": "1,1", "CEMODE": "2",
              "CALLDISA": "0,0", "CGDCONT": "OK", "QCPDPP": "", "CGREG": "0,1", "COPS": "0,0,'Verizon ',7",
              "COPSCARRIER": "Verizon", "COPSSERVICE": "4G/LTE", "CSQ": "31,3", "CGMI": "Telit",
              "CGMM": "LE910C4-NF", "CGMR": "M0F.660006", "CNUM": "'Line 1','+19495753478',145",
              "GCAP": "+CGSM,+DS,+MS", "CGATT": "1", "APN_CEREG": "", "APN_CGREG": "", "APN_CREG": ""}
    signal:
      description: Current k/v pairs of CEllular Signal info of the WTI device.
      returned: always
      type: dict
      sample: {"rssi": "-62 dBm", "rsrp": "-96 dBm", "rsrq": "-12 dB", "snr": "6.6 dB", "radiointerface": "LTE",
              "bandclass": "EUTRAN-4", "band": "4", "frequency": "1700", "channel": "2100"}
"""

import base64
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text, to_bytes, to_native
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        cpm_url=dict(type='str', required=True),
        cpm_username=dict(type='str', required=True),
        cpm_password=dict(type='str', required=True, no_log=True),
        use_https=dict(type='bool', default=True),
        validate_certs=dict(type='bool', default=True),
        use_proxy=dict(type='bool', default=False)
    )

    result = dict(
        changed=False,
        data=''
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    auth = to_text(base64.b64encode(to_bytes('{0}:{1}'.format(to_native(module.params['cpm_username']), to_native(module.params['cpm_password'])),
                   errors='surrogate_or_strict')))

    if module.params['use_https'] is True:
        protocol = "https://"
    else:
        protocol = "http://"

    fullurl = ("%s%s/api/v2/config/cellular" % (protocol, to_native(module.params['cpm_url'])))

    try:
        response = open_url(fullurl, data=None, method='GET', validate_certs=module.params['validate_certs'], use_proxy=module.params['use_proxy'],
                            headers={'Content-Type': 'application/json', 'Authorization': "Basic %s" % auth})

    except HTTPError as e:
        fail_json = dict(msg='GET: Received HTTP error for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except URLError as e:
        fail_json = dict(msg='GET: Failed lookup url for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except SSLValidationError as e:
        fail_json = dict(msg='GET: Error validating the server''s certificate for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except ConnectionError as e:
        fail_json = dict(msg='GET: Error connecting to {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)

    result['data'] = json.loads(response.read())

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
