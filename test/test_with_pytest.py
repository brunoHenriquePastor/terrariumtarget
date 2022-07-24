#!/usr/bin/env/ python
# -*- coding: utf8 -*-

from datetime import date


def test_request_returns_200(client):
    assert client.get("broker.emqx.io").status_code == 200


