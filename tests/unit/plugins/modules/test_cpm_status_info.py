# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import pytest

from ansible_collections.wti.remote.plugins.modules import cpm_status_info


class DummyResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


class DummyModule:
    def __init__(self, params):
        self.params = params
        self.exited = None
        self.failed = None

    def exit_json(self, **kwargs):
        self.exited = kwargs
        raise SystemExit()

    def fail_json(self, **kwargs):
        self.failed = kwargs
        raise SystemExit()


def _patch_module(monkeypatch, params):
    dummy = DummyModule(params=params)
    monkeypatch.setattr(cpm_status_info, "AnsibleModule", lambda *a, **k: dummy)
    return dummy


def test_success_https(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": True,
        "validate_certs": False,
        "use_proxy": False,
    }
    dummy = _patch_module(monkeypatch, params)

    def fake_open_url(url, **kwargs):
        assert url.startswith("https://")
        return DummyResponse({"vendor": "wti", "status": {"code": "0", "text": "OK"}})

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.exited is not None
    assert dummy.exited["changed"] is False
    assert dummy.exited["data"]["vendor"] == "wti"


def test_success_http(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": False,
        "validate_certs": True,
        "use_proxy": True,
    }
    dummy = _patch_module(monkeypatch, params)

    def fake_open_url(url, **kwargs):
        assert url.startswith("http://")
        return DummyResponse({"vendor": "wti"})

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.exited is not None
    assert dummy.exited["data"]["vendor"] == "wti"


def test_http_error(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": True,
        "validate_certs": True,
        "use_proxy": False,
    }
    dummy = _patch_module(monkeypatch, params)

    # Use the HTTPError class that your module imports
    HTTPError = cpm_status_info.HTTPError

    def fake_open_url(url, **kwargs):
        raise HTTPError(url, 401, "Unauthorized", hdrs=None, fp=None)

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.failed is not None
    assert "Received HTTP error" in dummy.failed["msg"]


def test_url_error(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": True,
        "validate_certs": True,
        "use_proxy": False,
    }
    dummy = _patch_module(monkeypatch, params)

    URLError = cpm_status_info.URLError

    def fake_open_url(url, **kwargs):
        raise URLError("DNS failed")

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.failed is not None
    assert "Failed lookup url" in dummy.failed["msg"]


def test_ssl_validation_error(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": True,
        "validate_certs": True,
        "use_proxy": False,
    }
    dummy = _patch_module(monkeypatch, params)

    SSLValidationError = cpm_status_info.SSLValidationError

    def fake_open_url(url, **kwargs):
        raise SSLValidationError("bad cert")

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.failed is not None
    assert "Error validating the server" in dummy.failed["msg"]


def test_connection_error(monkeypatch):
    params = {
        "cpm_url": "device.example",
        "cpm_username": "u",
        "cpm_password": "p",
        "use_https": True,
        "validate_certs": True,
        "use_proxy": False,
    }
    dummy = _patch_module(monkeypatch, params)

    ConnectionError = cpm_status_info.ConnectionError

    def fake_open_url(url, **kwargs):
        raise ConnectionError("refused")

    monkeypatch.setattr(cpm_status_info, "open_url", fake_open_url)

    with pytest.raises(SystemExit):
        cpm_status_info.run_module()

    assert dummy.failed is not None
    assert "Error connecting" in dummy.failed["msg"]
