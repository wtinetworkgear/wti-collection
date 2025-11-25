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
# Module to configure WTI Cellular runtime and Parameters from WTI OOB and PDU devices.

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
module: cpm_cellular_config
version_added: "2.10.0"
author:
    - "Western Telematic Inc. (@wtinetworkgear)"
short_description: Set  Cellular runtime information and Parameters of the WTI device.
description:
    - "Set  Cellular runtime information and Parameters of the WTI device"
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
    apn:
        description: APN for the cellular modem in the WTI device.
        type: str
        required: false
    cellenable:
        description: If the cellular modem is enabled in the WTI device.
        type: int
        required: false
        choices: [ 0, 1 ]
    wof_host1:
        description: Selects the primary host that will be pinged in order to test for failures.
        type: str
        required: false
    wof_host2:
        description: Selects the secondary host that will be pinged in order to test for failures.
        type: str
        required: false
    wof_gatewayaddr:
        description: When the cellular modem is defined as the default gateway, this determines which interface will be the default gateway.
        type: str
        required: false
    wof_enabled:
        description: Enables/disables the Wakeup on Failure feature.
        type: int
        required: false
        choices: [ 0, 1 ]
    wof_autorecov:
        description: When enabled, the cellular modem will automatically be put back into sleep state when failure is resolved.
        type: int
        required: false
    wof_gatewayport:
        description: The Ethernet port that will be used as the default gateway when the cellular modem is in the sleep state.
        type: int
        required: false
    wof_pinginter1:
        description: Determines how often the selected IP Address will be pinged.
        type: int
        required: false
    wof_afppinginter1:
        description: Determines how often the Ping command will be sent after a previous Ping command receives no response.
        type: int
        required: false
    wof_conscfail1:
        description: Determines how many consecutive failures pings must be detected in order to initiate a Wakeup on Failure..
        type: int
        required: false
    wof_sleepmode:
        description: Determines whether the cell modem will be attached or detached from the cell tower when sleep mode is active.
        type: int
        required: false
    wof_singlepingaddfail:
        description: After an Ethernet failure has triggered a Wakeup, this feature is used to manually re-enable Wakeup On Failure.
        type: int
        required: false
    wof_interfacemon:
        description: Selects the Ethernet interface(s) that will be monitored for failed ping responses.
        type: int
        required: false
    ipthru_enabled:
        description: Enables/disables the IP Passthrough feature.
        type: int
        required: false
        choices: [ 0, 1 ]
    ipthru_httpstermenable:
        description: Enables/disables HTTPS.
        type: int
        required: false
    ipthru_httpsterm:
        description: When IP Passthrough is enabled, the Cellular HTTPS Port will be incremented by 5000.
        type: int
        required: false
    ipthru_httptermenable:
        description: Enables/disables HTTP.
        type: int
        required: false
    ipthru_httpterm:
        description: When IP Passthrough is enabled, the Cellular HTTP Port will be incremented by 5000.
        type: int
        required: false
    ipthru_interfacemon:
        description: Selects the interface that your downstream device/router will be connected to.
        type: int
        required: false
    ipthru_sshtermenable:
        description: Enables/disables SSH.
        type: int
        required: false
    ipthru_sshterm:
        description: When IP Passthrough is enabled, the Cellular SSH Port will be incremented by 5000.
        type: int
        required: false
    ipthru_mac:
        description: The MAC address of your downstream device/router.
        type: str
        required: false

notes:
  - Use C(groups/cpm) in C(module_defaults) to set common options used between CPM modules.
"""

EXAMPLES = """
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
      sample: {"enabled": "0", "active": "0", "autorecov": "0", "gatewayport": "0",
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
import socket

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text, to_bytes, to_native
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


def assemble_json(cpmmodule, existing):
    total_change = 0
    json_load = ietfstring = ""

    localapn = localcellenable = None
    local_wof_enabled = local_wof_autorecov = local_wof_gatewayport = 0
    local_wof_pinginter1 = local_wof_afppinginter1 = local_wof_conscfail1 = 0
    local_wof_sleepmode = local_wof_singlepingaddfail = local_wof_interfacemon = 0
    local_wof_host1 = local_wof_host2 = local_wof_gatewayaddr = ""

    local_pass_enabled = 0
    local_pass_httpsterm = local_pass_httpstermenable = local_pass_httpterm = 0
    local_pass_httptermenable = local_pass_interfacemon = 0
    local_pass_sshterm = local_pass_sshtermenable = 0
    local_pass_mac = ""

#    cpmmodule.warn("This is a existing debug message: x=%s" % existing)

    # Cellular Enable / APN Parameters
    if cpmmodule.params["cellenable"] is not None:
        if (existing["cellenable"] != cpmmodule.params["cellenable"]):
            total_change = (total_change | 1)
            localcellenable = cpmmodule.params["cellenable"]

    if cpmmodule.params["apn"] is not None:
        if (existing["apn"] != to_native(cpmmodule.params["apn"])):
            total_change = (total_change | 2)
            localapn = to_native(cpmmodule.params["apn"])

    # WOF Parameters (if change all - 32764)
    if cpmmodule.params["wof_host1"] is not None:
        if (existing["wof"]["host1"] != to_native(cpmmodule.params["wof_host1"])):
            total_change = (total_change | 4)
            local_wof_host1 = to_native(cpmmodule.params["wof_host1"])

    if cpmmodule.params["wof_host2"] is not None:
        if (existing["wof"]["host2"] != to_native(cpmmodule.params["wof_host2"])):
            total_change = (total_change | 8)
            local_wof_host2 = to_native(cpmmodule.params["wof_host2"])

    if cpmmodule.params["wof_gatewayaddr"] is not None:
        if (existing["wof"]["gatewayaddr"] != to_native(cpmmodule.params["wof_gatewayaddr"])):
            total_change = (total_change | 16)
            local_wof_gatewayaddr = to_native(cpmmodule.params["wof_gatewayaddr"])

    if cpmmodule.params["wof_enabled"] is not None:
        if (existing["wof"]["enabled"] != cpmmodule.params["wof_enabled"]):
            total_change = (total_change | 32)
            local_wof_enabled = cpmmodule.params["wof_enabled"]

    if cpmmodule.params["wof_autorecov"] is not None:
        if (existing["wof"]["autorecov"] != cpmmodule.params["wof_autorecov"]):
            total_change = (total_change | 64)
            local_wof_autorecov = cpmmodule.params["wof_autorecov"]

    if cpmmodule.params["wof_gatewayport"] is not None:
        if (existing["wof"]["gatewayport"] != cpmmodule.params["wof_gatewayport"]):
            total_change = (total_change | 128)
            local_wof_gatewayport = cpmmodule.params["wof_gatewayport"]

    if cpmmodule.params["wof_pinginter1"] is not None:
        if (existing["wof"]["pinginter1"] != cpmmodule.params["wof_pinginter1"]):
            total_change = (total_change | 256)
            local_wof_pinginter1 = cpmmodule.params["wof_pinginter1"]

    if cpmmodule.params["wof_afppinginter1"] is not None:
        if (existing["wof"]["afppinginter1"] != cpmmodule.params["wof_afppinginter1"]):
            total_change = (total_change | 512)
            local_wof_afppinginter1 = cpmmodule.params["wof_afppinginter1"]

    if cpmmodule.params["wof_conscfail1"] is not None:
        if (existing["wof"]["conscfail1"] != cpmmodule.params["wof_conscfail1"]):
            total_change = (total_change | 1024)
            local_wof_conscfail1 = cpmmodule.params["wof_conscfail1"]

    if cpmmodule.params["wof_sleepmode"] is not None:
        if (existing["wof"]["sleepmode"] != cpmmodule.params["wof_sleepmode"]):
            total_change = (total_change | 2048)
            local_wof_sleepmode = cpmmodule.params["wof_sleepmode"]

    if cpmmodule.params["wof_singlepingaddfail"] is not None:
        if (existing["wof"]["singlepingaddfail"] != cpmmodule.params["wof_singlepingaddfail"]):
            total_change = (total_change | 4096)
            local_wof_singlepingaddfail = cpmmodule.params["wof_singlepingaddfail"]

    if cpmmodule.params["wof_interfacemon"] is not None:
        if (existing["wof"]["interfacemon"] != cpmmodule.params["wof_interfacemon"]):
            total_change = (total_change | 8192)
            local_wof_interfacemon = cpmmodule.params["wof_interfacemon"]

    # IP Passthrough Parameters (if change all - 8372224)
    if cpmmodule.params["ipthru_mac"] is not None:
        if (existing["passth"]["mac"] != to_native(cpmmodule.params["ipthru_mac"])):
            total_change = (total_change | 16384)
            local_pass_mac = to_native(cpmmodule.params["ipthru_mac"])

    if cpmmodule.params["ipthru_enabled"] is not None:
        if (existing["passth"]["enabled"] != cpmmodule.params["ipthru_enabled"]):
            total_change = (total_change | 32768)
            local_pass_enabled = to_native(cpmmodule.params["ipthru_enabled"])

    if cpmmodule.params["ipthru_httpstermenable"] is not None:
        if (existing["passth"]["httptermenable"] != cpmmodule.params["ipthru_httpstermenable"]):
            total_change = (total_change | 65536)
            local_pass_httpstermenable = to_native(cpmmodule.params["ipthru_httpstermenable"])

    if cpmmodule.params["ipthru_httpsterm"] is not None:
        if (existing["passth"]["httpsterm"] != cpmmodule.params["ipthru_httpsterm"]):
            total_change = (total_change | 131072)
            local_pass_httpsterm = to_native(cpmmodule.params["ipthru_httpsterm"])

    if cpmmodule.params["ipthru_httptermenable"] is not None:
        if (existing["passth"]["httptermenable"] != cpmmodule.params["ipthru_httptermenable"]):
            total_change = (total_change | 262144)
            local_pass_httptermenable = to_native(cpmmodule.params["ipthru_httptermenable"])

    if cpmmodule.params["ipthru_httpterm"] is not None:
        if (existing["passth"]["httpsterm"] != cpmmodule.params["ipthru_httpterm"]):
            total_change = (total_change | 524288)
            local_pass_httpterm = to_native(cpmmodule.params["ipthru_httpterm"])

    if cpmmodule.params["ipthru_interfacemon"] is not None:
        if (existing["passth"]["interfacemon"] != cpmmodule.params["ipthru_interfacemon"]):
            total_change = (total_change | 1048576)
            local_pass_interfacemon = to_native(cpmmodule.params["ipthru_interfacemon"])

    if cpmmodule.params["ipthru_sshtermenable"] is not None:
        if (existing["passth"]["sshtermenable"] != cpmmodule.params["ipthru_sshtermenable"]):
            total_change = (total_change | 2097152)
            local_pass_sshtermenable = to_native(cpmmodule.params["ipthru_sshtermenable"])

    if cpmmodule.params["ipthru_sshterm"] is not None:
        if (existing["passth"]["sshterm"] != cpmmodule.params["ipthru_sshterm"]):
            total_change = (total_change | 4194304)
            local_pass_sshterm = to_native(cpmmodule.params["ipthru_sshterm"])

    if (total_change > 0):
        ietfstring = ""

        if (localapn is not None):
            ietfstring = '%s"apn": "%s"' % (ietfstring, localapn)

        if (localcellenable is not None):
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"cellenable": %s' % (ietfstring, localcellenable)

        if ((total_change & 32764) > 0):
            pastheader = 0
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"wof": {' % (ietfstring)

            if (local_wof_enabled is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"enabled": "%s"' % (ietfstring, local_wof_enabled)
                pastheader = 1
            if (local_wof_autorecov is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"autorecov": "%s"' % (ietfstring, local_wof_autorecov)
                pastheader = 1
            if (local_wof_gatewayport is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"gatewayport": "%s"' % (ietfstring, local_wof_gatewayport)
                pastheader = 1
            if (local_wof_pinginter1 is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"pinginter1": "%s"' % (ietfstring, local_wof_pinginter1)
                pastheader = 1
            if (local_wof_afppinginter1 is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"afppinginter1": "%s"' % (ietfstring, local_wof_afppinginter1)
                pastheader = 1
            if (local_wof_conscfail1 is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"conscfail1": "%s"' % (ietfstring, local_wof_conscfail1)
                pastheader = 1
            if (local_wof_sleepmode is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"sleepmode": "%s"' % (ietfstring, local_wof_sleepmode)
                pastheader = 1
            if (local_wof_singlepingaddfail is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"singlepingaddfail": "%s"' % (ietfstring, local_wof_singlepingaddfail)
                pastheader = 1
            if (local_wof_interfacemon is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"interfacemon": "%s"' % (ietfstring, local_wof_interfacemon)
                pastheader = 1
            if (local_wof_host1 is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"host1": "%s"' % (ietfstring, local_wof_host1)
                pastheader = 1
            if (local_wof_host2 is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"host2": "%s"' % (ietfstring, local_wof_host2)
                pastheader = 1
            if (local_wof_gatewayaddr is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"gatewayaddr": "%s"' % (ietfstring, local_wof_gatewayaddr)
                pastheader = 1
            ietfstring = '%s}' % (ietfstring)

        if ((total_change & 8372224) > 0):
            pastheader = 0
            if (len(ietfstring) > 0):
                ietfstring = '%s,' % (ietfstring)
            ietfstring = '%s"passth": {' % (ietfstring)

            if (local_pass_enabled is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"enabled": "%s"' % (ietfstring, local_pass_enabled)
                pastheader = 1
            if (local_pass_interfacemon is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"interfacemon": "%s"' % (ietfstring, local_pass_interfacemon)
                pastheader = 1
            if (local_pass_httptermenable is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"httptermenable": "%s"' % (ietfstring, local_pass_httptermenable)
                pastheader = 1
            if (local_pass_httpterm is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"httpterm": "%s"' % (ietfstring, local_pass_httpterm)
                pastheader = 1
            if (local_pass_httpstermenable is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"httpstermenable": "%s"' % (ietfstring, local_pass_httpstermenable)
                pastheader = 1
            if (local_pass_httpsterm is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"httpsterm": "%s"' % (ietfstring, local_pass_httpsterm)
                pastheader = 1
            if (local_pass_sshtermenable is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"sshtermenable": "%s"' % (ietfstring, local_pass_sshtermenable)
                pastheader = 1
            if (local_pass_sshterm is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"sshterm": "%s"' % (ietfstring, local_pass_sshterm)
                pastheader = 1
            if (local_pass_mac is not None):
                if ((len(ietfstring) > 0) & (pastheader == 1)):
                    ietfstring = '%s,' % (ietfstring)
                ietfstring = '%s"mac": "%s"' % (ietfstring, local_pass_mac)
                pastheader = 1

            ietfstring = '%s}' % (ietfstring)

        json_load = "{"
        json_load = '%s%s' % (json_load, ietfstring)
        json_load = '%s}' % (json_load)
        cpmmodule.warn("This is a existing debug message: x=%s" % json_load)

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
        apn=dict(type='str', required=False, default=None),
        cellenable=dict(type='int', required=False, default=None, choices=[0, 1]),
        wof_host1=dict(type='str', required=False, default=None),
        wof_host2=dict(type='str', required=False, default=None),
        wof_gatewayaddr=dict(type='str', required=False, default=None),
        wof_enabled=dict(type='int', required=False, default=None, choices=[0, 1]),
        wof_autorecov=dict(type='int', required=False, default=None),
        wof_gatewayport=dict(type='int', required=False, default=None),
        wof_pinginter1=dict(type='int', required=False, default=None),
        wof_afppinginter1=dict(type='int', required=False, default=None),
        wof_conscfail1=dict(type='int', required=False, default=None),
        wof_sleepmode=dict(type='int', required=False, default=None),
        wof_singlepingaddfail=dict(type='int', required=False, default=None),
        wof_interfacemon=dict(type='int', required=False, default=None),
        ipthru_enabled=dict(type='int', required=False, default=None, choices=[0, 1]),
        ipthru_mac=dict(type='str', required=False, default=None),
        ipthru_httpstermenable=dict(type='int', required=False, default=None),
        ipthru_httpsterm=dict(type='int', required=False, default=None),
        ipthru_httptermenable=dict(type='int', required=False, default=None),
        ipthru_httpterm=dict(type='int', required=False, default=None),
        ipthru_interfacemon=dict(type='int', required=False, default=None),
        ipthru_sshtermenable=dict(type='int', required=False, default=None),
        ipthru_sshterm=dict(type='int', required=False, default=None),
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
    except socket.timeout as e:
        fail_json = dict(msg='POST: Connection timed out for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
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
            fullurl = ("%s%s/api/v2/config/cellular" % (protocol, to_native(module.params['cpm_url'])))
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
            except socket.timeout as e:
                fail_json = dict(msg='POST: Connection timed out for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
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
