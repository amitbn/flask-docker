#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.testing import TestCase
from app import flask_app
from time import sleep

class TestFlaskDocker(TestCase):

    def create_app(self):
        return flask_app

    def test_stop_when_not_running(self):
        resp = self.client.get('/stop')
        assert resp.status_code == 200
        assert 'already not running' in resp.data

    def test_all_endpoints_exist(self):
        resp = self.client.get('/status')
        assert resp.status_code == 200
        resp = self.client.get('/start')
        assert resp.status_code == 200
        resp = self.client.get('/stop')
        assert resp.status_code == 200

    def test_start_friendly_name(self):
        resp = self.client.get('/start?name=TESTNAME')
        assert resp.status_code == 200
        assert 'TESTNAME' in resp.data

        resp = self.client.get('/stop')
        assert resp.status_code == 200

    def test_start_when_already_running(self):
        resp = self.client.get('/start')
        assert resp.status_code == 200
        assert 'started docker container' in resp.data
        resp = self.client.get('/start')
        assert resp.status_code == 200
        assert 'already running' in resp.data
        
        resp = self.client.get('/stop')
        assert resp.status_code == 200

    def test_status(self):
        resp = self.client.get('/start')
        assert resp.status_code == 200
        assert 'started docker container' in resp.data

        resp = self.client.get('/status')
        assert resp.status_code == 200
        assert 'docker container status is Up' in resp.data

        resp = self.client.get('/stop')
        assert resp.status_code == 200

        resp = self.client.get('/status')
        assert resp.status_code == 200
        assert 'not running' in resp.data
