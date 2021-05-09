#!/usr/bin/env python3

import requests
import json
import sys

baseURL = "https://developer-api.govee.com"
device_endpoint = baseURL + "/v1/devices"
control_endpoint = device_endpoint + "/control"

api_key = "API_KEY"

goveee_headers = {
    "Govee-API-Key": api_key,
    "Content-Type": "application/json"
}

#Get current status
devices = json.loads(requests.request("GET", url=device_endpoint, headers=goveee_headers).text)

for dev in devices['data']['devices']:
    if (dev['deviceName'] == "Monitor Ambient"):
        device_state = json.loads(requests.request("GET",
            url=device_endpoint + "/state?device=" + dev['device'] + "&" + "model=" + dev['model'],
            headers=goveee_headers).text)
        if (device_state['data']['properties'][0]['online'] == True):
            setto = ""
            if (device_state['data']['properties'][1]['powerState'] == "off"):
                setto = "on"
            else:
                setto = "off"
            command_data = {
                "device": dev["device"],
                "model": dev["model"],
                "cmd": {
                    "name": "turn",
                    "value": setto
                }
            }
            command_payload = json.dumps(command_data)
            requests.request("PUT", url=control_endpoint, headers=goveee_headers, data=command_payload)
        else:
            sys.exit(100)
