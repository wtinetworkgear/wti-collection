#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) 2019 Red Hat Inc.
# Copyright (C) 2019 Western Telematic Inc.
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
# Module to upgeade the firmware on WTI OOB and PDU devices.
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
module: cpm_firmware_update
version_added: "2.9.0"
author: "Western Telematic Inc. (@wtinetworkgear)"
short_description: Set Serial port parameters in WTI OOB and PDU devices
description:
    - "Set Serial port parameters in WTI OOB and PDU devices"
options:
    cpm_url:
        description:
            - This is the URL of the WTI device to send the module.
        required: true
        type: str
    cpm_username:
        description:
            - This is the Username of the WTI device to send the module.
        required: true
        type: str
    cpm_password:
        description:
            - This is the Password of the WTI device to send the module.
        required: true
        type: str
    cpm_path:
        description:
            - This is the directory path to store the WTI device configuration file.
        required: false
        type: str
        default: "/tmp/"
    cpm_file:
        description:
            - If a file is defined, this file will be used to update the WTI device.
        required: false
        type: str
    use_force:
        description:
            - If set to True, the upgrade will happen even if the device doesnt need it.
        required: false
        type: bool
        default: false
    use_https:
        description:
            - Designates to use an https connection or http connection.
        required: false
        type: bool
        default: true
    validate_certs:
        description:
            - If false, SSL certificates will not be validated. This should only be used
              - on personally controlled sites using self-signed certificates.
        required: false
        type: bool
        default: true
    use_proxy:
        description: Flag to control if the lookup will observe HTTP proxy environment variables when present.
        required: false
        type: bool
        default: false
    family:
        description:
            - Force the download to both either Console (1) or Power (0)
        required: false
        type: int
        default: 1
        choices: [ 0, 1 ]
    removefileonexit:
        description:
            - After an upgrade, remove the upgrade OS image
        required: false
        type: int
        default: 1
        choices: [ 0, 1 ]
    ignoreincremental:
        description:
            - If there are any incremental upgrades, do not install them
        required: false
        type: int
        default: 0
        choices: [ 0, 1 ]
    bootafterincremental:
        description:
            - If set to 1, the WTI device will reboot after an incremental update is sucessfully uploaded
        required: false
        type: int
        default: 1
        choices: [ 0, 1 ]
    max_console_version:
        description:
            - If defined, this will be the maximum version that will be searched for all console units
        required: false
        type: float
    max_power_version:
        description:
            - If defined, this will be the maximum version that will be searched for all power units
        required: false
        type: float

notes:
    - Use C(groups/cpm) in C(module_defaults) to set common options used between CPM modules.
"""

EXAMPLES = """
# Upgrade the firmware of a WTI device
- name: Upgrade the firmware of a WTI device
  cpm_firmware_update:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false


# Upgrade the firmware of a WTI device and keep the download OS image after exit
- name: Upgrade the firmware of a WTI device and keep the download OS image after exit
  cpm_firmware_update:
    cpm_url: "nonexist.wti.com"
    cpm_username: "super"
    cpm_password: "super"
    use_https: true
    validate_certs: false
    removefileonexit: "0"
"""

RETURN = """
data:
    description: The output XML configuration of the WTI device being updated
    returned: always
    type: complex
    contains:
        filelength:
            description: Length of the file uploaded in bytes
            returned: success
            type: int
            sample:
                - filelength: 329439
        status:
            description: List of status returns from backup operation
            returned: success
            type: list
            sample:
                - code: 0
                - text: "ok"
                - unittimestamp: "2020-02-14T00:18:57+00:00"
"""

import base64
import os
import json
import tempfile
import re
import time

try:
    import requests
    HAS_REQUESTS_LIBRARY = True
except ImportError:
    HAS_REQUESTS_LIBRARY = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text, to_bytes, to_native
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


def run_module():
    # define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        cpm_url=dict(type='str', required=True),
        cpm_username=dict(type='str', required=True),
        cpm_password=dict(type='str', required=True, no_log=True),
        cpm_path=dict(type='str', default="/tmp/"),
        cpm_file=dict(type='str', default=None),
        family=dict(type='int', default=1, choices=[0, 1]),
        removefileonexit=dict(type='int', default=1, choices=[0, 1]),
        ignoreincremental=dict(type='int', default=0, choices=[0, 1]),
        bootafterincremental=dict(type='int', default=1, choices=[0, 1]),
        max_console_version=dict(type='float', default=None),
        max_power_version=dict(type='float', default=None),
        use_force=dict(type='bool', default=False),
        use_https=dict(type='bool', default=True),
        validate_certs=dict(type='bool', default=True),
        use_proxy=dict(type='bool', default=False)
    )

    result = dict(
        changed=False,
        data=''
    )

    family = None
    online_file_location = None
    usersuppliedfilename = None
    forceupgrade = False
    localfilefamily = -1
    ignoreincremental = 0

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    verbosity = module._verbosity

    if HAS_REQUESTS_LIBRARY is False:
        fail_json = dict(msg='IMPORT: requests import not installed', changed=False)
        module.fail_json(**fail_json)

    if module.params['cpm_file'] is not None:
        usersuppliedfilename = ("%s%s" % (to_native(module.params['cpm_path']), to_native(module.params['cpm_file'])))

    if module.params['use_force'] is True:
        forceupgrade = True

    if (int(module.params['ignoreincremental']) > 0):
        ignoreincremental = 1

    # if a local file was defined lets see what family it is: Console or Power
    if (usersuppliedfilename is not None):
        try:
            ifilesize = os.path.getsize(usersuppliedfilename)
            file = open(usersuppliedfilename, 'rb')
            file.seek(ifilesize - 20)
            fileread = file.read()
            if (fileread.find(b"TSM") >= 0):
                localfilefamily = 1
            elif (fileread.find(b"VMR") >= 0):
                localfilefamily = 0
            elif (fileread.find(b"INCUPDATE") >= 0):
                localfilefamily = 2
                module.warn("INC UPDATE type., versions need to match")

            file.close()

            if (localfilefamily == 2):
                module.warn("User Supplied file [%s] is a Incremental type." % (usersuppliedfilename,))
            else:
                module.warn("User Supplied file [%s] is a %s type." % (usersuppliedfilename, ("Console" if localfilefamily == 1 else "Power")))

        except Exception as e:
            fail_json = dict(msg='FILE: User Supplied file {0} does not exist : {1}'.format(usersuppliedfilename, to_native(e)), changed=False)
            module.fail_json(**fail_json)

    auth = to_text(base64.b64encode(to_bytes('{0}:{1}'.format(to_native(module.params['cpm_username']), to_native(module.params['cpm_password'])),
                   errors='surrogate_or_strict')))

    if module.params['use_https'] is True:
        protocol = "https://"
    else:
        protocol = "http://"

    # 1. Get the Version of the WTI device
    fullurl = ("%s%s/api/v2/status/firmware" % (protocol, to_native(module.params['cpm_url'])))
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

    result['data'] = json.loads(response.read())
    statuscode = result['data']["status"]["code"]

    try:
        # Extract incremental array
        local_incremental_list = result['data']["config"]["incremental"]

        if (verbosity):
            # Print or use the list
            module.warn("1A. local_incremental_list  [%s]." % (local_incremental_list))

            for item in local_incremental_list:
                module.warn("2A. item['title']  [%s]." % (item["title"]))
                module.warn("3A. item['vpart']  [%s], item['vinc']: [%s]." % (item["vpart"], item["vinc"]))

    except Exception as e:
        local_incremental_list = ""
        if (verbosity):
            module.warn("EXCEPTION 1 %s" % (str(e)))

    local_release_version = result['data']["config"]["firmware"]

    # remove any 'alpha' or 'beta' designations if they are present)
    match = re.match(r"^\d+(\.\d+)?", local_release_version)
    if match:
        local_release_version = float(match.group())

    try:
        family = int(result['data']["config"]["family"])
    except Exception as e:
        family = 1

    if (localfilefamily != -1):
        if (family != localfilefamily):
            fail_json = dict(msg='FAMILY MISMATCH: Your local file is a: %s type, the device is a %s type, localfilefamily: (%d)'
                             % (("Console" if localfilefamily == 1 else "Power"), ("Console" if family == 1 else "Power"), localfilefamily), changed=False)
            module.fail_json(**fail_json)

    versioncap = ""
    if (family == 2):
        if module.params['max_power_version'] is not None:
            if (float(module.params['max_power_version']) > 0):
                versioncap = ("&versioncap=%s" % (module.params['max_power_version']))
    else:
        if module.params['max_console_version'] is not None:
            if (float(module.params['max_console_version']) > 0):
                versioncap = ("&versioncap=%s" % (module.params['max_console_version']))

    # 2. Go online and find the latest version of the os image for this device family
    wti_incremental_list = ""
    if (localfilefamily == -1):
        fullurl = ("https://my.wti.com/update/version.aspx?fam=%s%s" % (family, versioncap))

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

        result['data'] = json.loads(response.read())
        remote_release_version = result['data']["config"]["firmware"]

        if module.params['max_console_version'] is not None:
            if (float(module.params['max_console_version']) > 0):
                if (float(module.params['max_console_version']) < (float(remote_release_version))):
                    remote_release_version = float(module.params['max_console_version'])

        # if the local version is less than the online latest version ignore all incremental upgrades
        wti_incremental_total = 0

        if ((float(local_release_version)) == (float(remote_release_version))):
            if (((float(local_release_version) < 8.09) & (family == 1)) | ((float(local_release_version) < 4.05) & (family == 0))):
                ignoreincremental = 1
            try:
                if (ignoreincremental == 0):
                    # Extract incremental array
                    wti_incremental_list = result['data']["config"]["incremental"]
                    if (verbosity):
                        module.warn("wti_incremental_list size (%d)" % (len(wti_incremental_list)))

                    # Print or use the list
                    if (verbosity):
                        module.warn("1B. local_release_version  [%s]." % (wti_incremental_list))
                        module.warn("1B. local_incremental_list  [%s]." % (local_incremental_list))

                        # Loop through the my.wti.com complete incremental available updates
                        module.warn("1c. length wti_incremental_list  (%d)." % (len(wti_incremental_list)))
                        module.warn("1c. length local_incremental_list (%d)." % (len(local_incremental_list)))

                    new_wti_list = []
                    for item_wti in wti_incremental_list:
                        matched = False
                        if (verbosity):
                            module.warn("loop item_wti item_wti['title']:   [%s], item_wti['vpart']:   (%d), item_wti['vinc']: (%d)"
                                        % (item_wti["title"], int(item_wti['vpart']), int(item_wti['vinc'])))

                        if (len(local_incremental_list) > 0):
                            for item_local in local_incremental_list:
                                if (verbosity):
                                    module.warn("   -> COMPARE item_local['title']  [%s], item_local['vpart']: (%d), item_local['vinc']: (%d)"
                                                % (item_local["title"], int(item_local['vpart']), int(item_local['vinc'])))
                                    module.warn("   -> AND     item_wti['title']    [%s], item_wti['vpart']:   (%d), item_wti['vinc']:   (%d)"
                                                % (item_wti["title"], int(item_wti['vpart']), int(item_wti['vinc'])))

                                if (int(item_local['vpart']) == int(item_wti['vpart'])):
                                    matched = True
                                    if int(item_wti['vinc']) > int(item_local['vinc']):
                                        if (verbosity):
                                            module.warn(
                                                "-> 1. New version online item_local['title'] [%s], "
                                                "item_local['vpart']: (%d), item_local['vinc']: (%d)"
                                                % (
                                                    item_local["title"], int(item_local["vpart"]), int(item_local["vinc"]),
                                                )
                                            )

                                            module.warn(
                                                "-> 1. New version online item_wti['title'] [%s], "
                                                "item_wti['vpart']: (%d), item_wti['vinc']: (%d)"
                                                % (
                                                    item_wti["title"], int(item_wti["vpart"]), int(item_wti["vinc"]),
                                                )
                                            )

                                        new_wti_list.append(item_wti)
                                        matched = True
                                        break
                            if not matched:
                                if (verbosity):
                                    module.warn("   -> NO - MATCH/DELETE item_local['title']    [%s], item_local['vpart']:   (%d), item_local['vinc']: (%d)"
                                                % (item_local["title"], int(item_local['vpart']), int(item_local['vinc'])))
                                    module.warn("   -> NO - MATCH/DELETE item_wti['title']    [%s], item_wti['vpart']:   (%d), item_wti['vinc']: (%d)"
                                                % (item_wti["title"], int(item_wti['vpart']), int(item_wti['vinc'])))
                                new_wti_list.append(item_wti)
                        else:
                            if (verbosity):
                                module.warn("   -> 2. New version online item_wti['title']    [%s], item_wti['vpart']:   (%d), item_wti['vinc']: (%d)"
                                            % (item_wti["title"], int(item_wti['vpart']), int(item_wti['vinc'])))
                            new_wti_list.append(item_wti)
                    # Replace the original list with the filtered one
                    wti_incremental_list = new_wti_list

            except Exception as e:
                wti_incremental_list = ""
                if (verbosity):
                    module.warn("EXCEPTION 2 %s." % (str(e)))

        if ((float(local_release_version) < 6.58) & (family == 1)) | ((float(local_release_version) < 2.15) & (family == 0)):
            fail_json = dict(msg='ERROR: WTI Device does not support remote upgrade', changed=False)
            module.fail_json(**fail_json)
        statuscode = result['data']['status']['code']
    else:
        remote_release_version = 0

    wti_incremental_total = len(wti_incremental_list)

    if (verbosity):
        module.warn("Number of items in wti_incremental_list: %d" % len(wti_incremental_list))

    if (verbosity):
        if (wti_incremental_total > 0):
            for item_wti in wti_incremental_list:
                module.warn("4a. item_wti['title']  [%s], item_wti['vpart']: (%d)" % (item_wti["title"], int(item_wti['vpart'])))
                module.warn("4a. item_wti['imageurl']  [%s], item_wti['vinc']: (%d)" % (item_wti["imageurl"], int(item_wti['vinc'])))

    INCString = INCTitle = ""
    INCPart = is_incremental = 0
    if (int(statuscode) == 0):
        local_filename = None
        if ((float(local_release_version) < float(remote_release_version)) or (forceupgrade == 1)) or (localfilefamily >= 0) or (wti_incremental_total > 0):
            if (module.check_mode is False):
                if (localfilefamily == -1):
                    INCPart = 0
                    while wti_incremental_total != -1:
                        time.sleep(5)

                        if (wti_incremental_total == 0):
                            online_file_location = result['data']["config"]["imageurl"]
                            wti_incremental_total = -1  # only go through one time
                        else:
                            is_incremental = is_incremental + 1
                            online_file_location = wti_incremental_list[0]['imageurl']
                            INCPart = int(wti_incremental_list[0]['vpart'])
                            INCTitle = (wti_incremental_list[0]['title'])
                            wti_incremental_total = wti_incremental_total - 1
                            wti_incremental_list.remove(wti_incremental_list[0])

                            if (wti_incremental_total == 0):
                                wti_incremental_total = -1  # Done with loop

                        local_filename = online_file_location[online_file_location.rfind("/") + 1:]
                        local_filename = tempfile.gettempdir() + "/" + local_filename

                        response = requests.get(online_file_location, stream=True)
                        handle = open(local_filename, "wb")
                        for chunk in response.iter_content(chunk_size=512):
                            if chunk:  # filter out keep-alive new chunks
                                handle.write(chunk)
                        handle.close()

                        # SEND the file to the WTI device
                        # 3. upload new os image to WTI device
                        fullurl = ("%s%s/cgi-bin/getfile" % (protocol, to_native(module.params['cpm_url'])))
                        files = {'file': ('name.binary', open(local_filename, 'rb'), 'application/octet-stream')}

                        try:
                            response = requests.post(fullurl, files=files, auth=(to_native(module.params['cpm_username']),
                                                     to_native(module.params['cpm_password'])), verify=(module.params['validate_certs']), stream=True)
                            result['data'] = response.json()
                            if (verbosity):
                                module.warn("    Data return:  [%s]" % (result['data']))

                            # Is it an incremental upgrade
                            if (is_incremental > 0):
                                if (len(INCString) > 0):
                                    INCString = INCString + ","

                                INCString = (
                                    "%s{ 'title': '%s', 'vpart': %d, 'code': '%s', 'filelength': '%s' }"
                                    % (
                                        INCString,
                                        INCTitle,
                                        INCPart,
                                        result['data']['status']['code'],
                                        result['data']['filelength'],
                                    )
                                )

                                if (verbosity):
                                    module.warn("INCString [%s]" % (INCString))

                            if (response.status_code == 200):
                                if (int(result['data']['status']['code']) == 0):
                                    result['changed'] = True
                                    if (len(INCString)):
                                        result['data'] = "{'incremental': [" + INCString + "]}"
                                else:
                                    fail_json = dict(msg='FAIL: Upgrade Failed for {0}'.format(fullurl), changed=False)
                                    module.fail_json(**fail_json)

                        except requests.exceptions.RequestException as e:  # This is the correct syntax
                            fail_json = dict(msg='GET: Received HTTP error for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                            module.fail_json(**fail_json)

                        # only remove if the file was downloaded
                        if (localfilefamily == -1):
                            if (int(module.params['removefileonexit']) == 1):
                                os.remove(local_filename)

                else:
                    if (family == localfilefamily):
                        local_filename = usersuppliedfilename
                    else:
                        module.log(msg="FAMILY MISMATCH: Your local file and the device do not match family types.")
                        fail_json = dict(msg='FAIL: (3) Upgrade Failed for {0}'.format(fullurl), changed=False)
                        module.fail_json(**fail_json)

                    # SEND the file to the WTI device
                    # 3. upload new os image to WTI device
                    fullurl = ("%s%s/cgi-bin/getfile" % (protocol, to_native(module.params['cpm_url'])))
                    files = {'file': ('name.binary', open(local_filename, 'rb'), 'application/octet-stream')}

                    if (verbosity):
                        module.warn("fullurl [%s]" % (fullurl))

                    try:
                        response = requests.post(fullurl, files=files, auth=(to_native(module.params['cpm_username']),
                                                 to_native(module.params['cpm_password'])), verify=(module.params['validate_certs']), stream=True)
                        result['data'] = response.json()

                        if (response.status_code == 200):
                            if (int(result['data']['status']['code']) == 0):
                                result['changed'] = True
                            else:
                                fail_json = dict(msg='FAIL: Upgrade Failed for {0}'.format(fullurl), changed=False)
                                module.fail_json(**fail_json)

                    except requests.exceptions.RequestException as e:  # This is the correct syntax
                        fail_json = dict(msg='GET: Received HTTP error for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
                        module.fail_json(**fail_json)

                    # only remove if the file was downloaded
                    if (localfilefamily == -1):
                        if (int(module.params['removefileonexit']) == 1):
                            os.remove(local_filename)
        else:
            result['data'] = "{ \"filelength\": \"0\", \"status\": { \"code\": \"1\", \"text\": \"device up to date\" } }"
    else:
        result['data'] = "{ \"filelength\": \"0\", \"status\": { \"code\": \"2\", \"text\": \"device bad family code: %s\" } }" % (family)

    if (int(module.params['bootafterincremental']) == 1):
        if (is_incremental > 0):
            if result['changed']:
                # Reboot device after incremental upgrade
                fullurl = ("%s%s/api/v2/config/rebootlocalunit" % (protocol, to_native(module.params['cpm_url'])))
                method = 'GET'
                try:
                    response = open_url(fullurl, data=None, method=method, validate_certs=module.params['validate_certs'], use_proxy=module.params['use_proxy'],
                                        headers={'Content-Type': 'application/json', 'Authorization': "Basic %s" % auth})

                except Exception as e:
                    fail_json = dict(msg="On Reboot: Unexpected error for {0} : {1}".format(fullurl, to_native(e)), changed=False)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
