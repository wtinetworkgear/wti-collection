#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) 2019 Red Hat Inc.
# Copyright (C) 2021 Western Telematic Inc.
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
# Module to execute WTI hostname parameters from WTI OOB and PDU devices.
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
module: cpm_ssh_config
version_added: "2.11.0"
author:
    - "Western Telematic Inc. (@wtinetworkgear)"
short_description: Set SSH parameters that are defined in WTI OOB and PDU devices
description:
    - "Set SSH parameters that are defined in  WTI OOB and PDU devices"
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
            - "Flag to control if the lookup will observe HTTP proxy environment variables when present."
        type: bool
        required: false
        default: false
    ssh_enable:
        description:
            - "This is the Site ID to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_port:
        description:
            - "This is the Location to be set for the WTI OOB and PDU device."
        type: int
        required: false
    ssh_level:
        description:
            - "This is the Hostname to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_viewenable:
        description:
            - "This is the Domain to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_viewbidirect:
        description:
            - "This is the Asset Tag to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_allowpseudo:
        description:
            - "This is the Asset Tag to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_disablepassauth:
        description:
            - "This is the Asset Tag to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
    ssh_disablechacha20:
        description:
            - "This is the Asset Tag to be set for the WTI OOB and PDU device."
        type: int
        required: false
        choices: [ 0, 1 ]
notes:
  - "Use C(groups/cpm) in C(module_defaults) to set common options used between CPM modules."
"""

EXAMPLES = """
# Set Hostname, Location and Site-ID variables of a WTI device
- name: Set known fixed hostname variables of a WTI device
  cpm_hostname_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    ssh_enable: 1
    ssh_port: 22

# Set the Hostname variable of a WTI device
- name: Set the Hostname of a WTI device
  cpm_hostname_config:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    ssh_enable: 1
    ssh_port: 22
    ssh_level: 1
    ssh_disablepassauth: 1
"""

RETURN = """
data:
  description: "The output JSON returned from the commands sent"
  returned: always
  type: complex
  contains:
    ssh_enable:
      description: "Enables/Disables SSH access to the device."
      returned: success
      type: int
      sample: 1
    ssh_port:
      description: "Port that is open and accepting connections for the SSH Server."
      returned: success
      type: int
      sample: 22
    ssh_level:
      description: "Security Level of SSH, High chooses stronger Ciphers: 0 - Normal, 1 - High."
      returned: success
      type: int
      sample: 1
    ssh_viewenable:
      description: "SSH View Port Enable/Disable."
      returned: success
      type: int
      sample: 0
    ssh_viewbidirect:
      description: "SSH View Port Bidirection Enable/Disable."
      returned: success
      type: int
      sample: 0
    ssh_allowpseudo:
      description: "Allow Pseudo-Terminal Enable/Disable."
      returned: success
      type: int
      sample: 0
    ssh_disablepassauth:
      description: "Disable Password Auth Enable/Disable."
      returned: success
      type: int
      sample: 0
    ssh_disablechacha20:
      description: "Disable/Enable the ChaCha20 Cipher from being used by the SSH server."
      returned: success
      type: int
      sample: 0
"""

import base64
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text, to_bytes, to_native
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


def assemble_json(cpmmodule, existing):
    total_change = 0
    json_load = ietfstring = ""

    local_enable = local_port = local_level = local_viewenable = local_viewbidirect = None
    local_allowpseudo = local_disablepassauth = local_disablechacha20 = None

    if cpmmodule.params["ssh_enable"] is not None:
        if (int(existing["ssh"]["enable"]) != int(to_native(cpmmodule.params["ssh_enable"]))):
            total_change = (total_change | 1)
            local_enable = to_native(cpmmodule.params["ssh_enable"])
    if cpmmodule.params["ssh_port"] is not None:
        if (int(existing["ssh"]["port"]) != int(to_native(cpmmodule.params["ssh_port"]))):
            total_change = (total_change | 2)
            local_port = to_native(cpmmodule.params["ssh_port"])
    if cpmmodule.params["ssh_level"] is not None:
        if (int(existing["ssh"]["level"]) != int(to_native(cpmmodule.params["ssh_level"]))):
            total_change = (total_change | 4)
            local_level = to_native(cpmmodule.params["ssh_level"])
    if cpmmodule.params["ssh_viewenable"] is not None:
        if (int(existing["ssh"]["viewenable"]) != int(to_native(cpmmodule.params["ssh_viewenable"]))):
            total_change = (total_change | 8)
            local_viewenable = to_native(cpmmodule.params["ssh_viewenable"])
    if cpmmodule.params["ssh_viewbidirect"] is not None:
        if (int(existing["ssh"]["viewbidirect"]) != int(to_native(cpmmodule.params["ssh_viewbidirect"]))):
            total_change = (total_change | 16)
            local_viewbidirect = to_native(cpmmodule.params["ssh_viewbidirect"])
    if cpmmodule.params["ssh_allowpseudo"] is not None:
        if (int(existing["ssh"]["allowpseudo"]) != int(to_native(cpmmodule.params["ssh_allowpseudo"]))):
            total_change = (total_change | 32)
            local_allowpseudo = to_native(cpmmodule.params["ssh_allowpseudo"])
    if cpmmodule.params["ssh_disablepassauth"] is not None:
        if (int(existing["ssh"]["disablepassauth"]) != int(to_native(cpmmodule.params["ssh_disablepassauth"]))):
            total_change = (total_change | 64)
            local_disablepassauth = to_native(cpmmodule.params["ssh_disablepassauth"])
    if cpmmodule.params["ssh_disablechacha20"] is not None:
        if (int(existing["ssh"]["disablechacha20"]) != int(to_native(cpmmodule.params["ssh_disablechacha20"]))):
            total_change = (total_change | 128)
            local_disablechacha20 = to_native(cpmmodule.params["ssh_disablechacha20"])

    if (total_change > 0):
        ietfstring = ""

        if (local_enable is not None):
            ietfstring = '%s"enable": "%s"' % (ietfstring, local_enable)

        if (local_port is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"port": "%s"' % (ietfstring, local_port)

        if (local_level is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"level": "%s"' % (ietfstring, local_level)

        if (local_viewenable is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"viewenable": "%s"' % (ietfstring, local_viewenable)

        if (local_viewbidirect is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"viewbidirect": "%s"' % (ietfstring, local_viewbidirect)

        if (local_allowpseudo is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"allowpseudo": "%s"' % (ietfstring, local_allowpseudo)

        if (local_disablepassauth is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"disablepassauth": "%s"' % (ietfstring, local_disablepassauth)

        if (local_disablechacha20 is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"disablechacha20": "%s"' % (ietfstring, local_disablechacha20)

        json_load = '{"ssh": {'
        json_load = '%s%s' % (json_load, ietfstring)
        json_load = '%s}}' % (json_load)
    else:
        json_load = None
    return json_load


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        cpm_url=dict(type='str', required=True),
        cpm_username=dict(type='str', required=True),
        cpm_password=dict(type='str', required=True, no_log=True),
        ssh_enable=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_port=dict(type='int', required=False, default=None),
        ssh_level=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_viewenable=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_viewbidirect=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_allowpseudo=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_disablepassauth=dict(type='int', required=False, default=None, choices=[0, 1]),
        ssh_disablechacha20=dict(type='int', required=False, default=None, choices=[0, 1]),
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

    fullurl = ("%s%s/api/v2/config/ssh" % (protocol, to_native(module.params['cpm_url'])))
    method = 'GET'
    try:
        response = open_url(fullurl, data=None, method=method, validate_certs=module.params['validate_certs'], use_proxy=module.params['use_proxy'],
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

    result['data'] = response.read()
    payload = assemble_json(module, json.loads(result['data']))

    if module.check_mode:
        if payload is not None:
            result['changed'] = True
    else:
        if payload is not None:
            fullurl = ("%s%s/api/v2/config/ssh" % (protocol, to_native(module.params['cpm_url'])))
            method = 'POST'

            try:
                response = open_url(fullurl, data=payload, method=method, validate_certs=module.params['validate_certs'], use_proxy=module.params['use_proxy'],
                                    headers={'Content-Type': 'application/json', 'Authorization': "Basic %s" % auth})

            except HTTPError as e:
                fail_json = dict(msg='POST: Received HTTP error for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                module.fail_json(**fail_json)
            except URLError as e:
                fail_json = dict(msg='POST: Failed lookup url for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                module.fail_json(**fail_json)
            except SSLValidationError as e:
                fail_json = dict(msg='POST: Error validating the server''s certificate for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                module.fail_json(**fail_json)
            except ConnectionError as e:
                fail_json = dict(msg='POST: Error connecting to {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                module.fail_json(**fail_json)

            result['changed'] = True
            result['data'] = json.loads(response.read())

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
