from unittest.mock import patch
from unittest import mock
from wsgiref import headers
import pytest
import sys
from gym.gym_reg import app, add, test2
import json





@pytest.fixture()
def client():
    return app.test_client()

def get_test_profile():
    return json.load(open("test_add_profile.json","r"))

def test_view(client):
    resp = client.get("/",headers={"Content-Type": "application/json","x-api-key":"selva"})
    assert resp

def test_add(client):
    data = get_test_profile()
    resp = client.post("/add",
                    headers={"Content-Type": "application/json", "x-api-key":"selva"},
                         data=json.dumps(data))
    print(resp.text)
    assert resp.text == "Success"

def test_add_mock(mocker):
    mocker.patch('gym.gym_reg.get_value', return_value=get_test_profile())
    resp = add()
    assert resp == "Success"

def test_test2(mocker):
    mocker.patch('gym.gym_reg.tesst1', return_value="Success")
    resp = test2()
    assert resp == "Success"