import sys
import uuid
import requests
import ssl
import socket
import json
import http.client

'''
Sample class to get Tapo TP-Link C200 devices working in local area

It's a superclass to be implemented by Tapo class.

At this moment Local is a simple implementation of prove of concept used to
manage and exploit at local way device services.

Could be improved in the future with new features
'''
class Local:

    LOCAL_IP = "192.168.191.1" #when you have no paired device this is the AP server

    clientUUID = str(uuid.uuid4()) #random one
    token = ''
    url = "https://n-wap-gw.tplinkcloud.com"
    apiServer = 'https://n-euw1-wap-gw.tplinkcloud.com'
    server = 'euw1-relay-dcipc.i.tplinknbu.com'
    appType = 'Tapo_Android'
    version = "1.3"
    clientHeader = 'Tapo CameraClient Android 11.2.1/%s' % version
    deviceType='SMART.IPCAMERA' #
    seekCamera = '' #Camera name
    deviceId = ''
    quality = 'FHD' #'SD','VGA','HD' or 'FHD' - 'lq' & 'hq'

    session = requests.Session()

    def __init__(self):
        pass

    '''
    Autentication method with local admin default password (hashed) which
    returns token used to launch all verbs

    This method is needed to consume all interesting services
    '''
    def getToken(self):
        headers = {
            "Accept" : "application/json",
            "User-Agent": "Tapo CameraClient Android",
            "Requestbyapp": "true"
        }

        body = {
            "method" : "login",
            "params": {
                "hashed": "true",
                "password": "4004117BFDADDA243025EA2CFA702A9D",
                "username": "admin"
            }
        }

        response = self.session.post("https://%s:443" % self.LOCAL_IP, headers=headers, json=body, verify=False).json()
        return response

    '''
    Prove of concept, data will be extracted from local tests scripts and
    implemented at this way. All verbs could be implemented using this method
    and changing body structure.

    This method explain how consume a service from LOCAL_IP API
    '''
    def getDeviceInfo(self,token):
        body = {
            'method': 'multipleRequest',
            'params': {
                'requests': [{
                    'method':'getDeviceInfo',
                    'params':{
                        "device_info":{
                            "name":["info"]
                        }
                    }
                }]
            }
        }

        response = self.session.post("https://%s:443/stok=%s/ds" % (self.LOCAL_IP,token), json=body, verify=False).json()
        return response

    def payload(self):
        token=self.getToken()["result"]["stok"]
        r=self.getDeviceInfo(token)
        return r
