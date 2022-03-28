import sys
import uuid
import requests
import ssl
import socket
import json
import http.client
from local import Local

'''
This class implements an API consumer for Internet requested IoT based
on Tapo TP-Link devices, targeting and testing C200 cameras.

This implementation runs complete verbs with parameters, which could be
extracted and used to get automatications in your server, o simply take the
control of your device

Needs a valid username and password to get it working throw TP-Link Cloud.
'''
class Tapo(Local):

    def __init__(self,username,password):
        self.token=self.getToken(username,password)


    '''
    Overwrites local method with cloud implementation
    '''
    def getToken(self,username,password):
        params = {
            "method":"login",
            'params': {
                'appType': self.appType,
                'cloudUserName': username,
                'cloudPassword': password,
                'terminalUUID': self.clientUUID
            }
        }
        x = self.session.post(self.url, json=params, verify=False)
        response = x.json()
        self.token = response["result"]["token"] #update global token first
        return self.token #them return



    def helloCloud(self):
        body = {
            "appName" : "TP-Link_Tapo_Android",
            "appVer" : "2.1.2",
            "netType" : "wifi",
            "termID" : self.clientUUID,
            "ospf" : "Android 7.0",
            "locale" : "es_ES"
        }
        response = self.session.post(self.apiServer, json=body, verify=False).json()
        return response

    def getClockStatus(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getClockStatus",
        					"params": {
        						"system": {
        							"name": "clock_status"
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getAdvanceDeviceConfigurations(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getLedStatus",
        					"params": {
        						"harddisk_manage": {
        							"name": ["harddisk"],
        							"table": ["hd_info"]
        						},
        						"msg_alarm": {
        							"name": ["chn1_msg_alarm_info"]
        						},
        						"led": {
        							"name": ["config"]
        						},
        						"record_plan": {
        							"name": ["chn1_channel"]
        						},
        						"system": {
        							"name": ["basic"]
        						},
        						"user_management": {
        							"name": ["third_account"]
        						},
        						"wlan": {
        							"name": ["default_ap"]
        						},
        						"cet": {
        							"name": ["media_encrypt"]
        						},
        						"image": {
        							"name": ["switch"]
        						},
        						"timing_reboot": {
        							"name": ["reboot"]
        						},
        						"device_info": {
        							"name": ["basic_info", "info"]
        						},
        						"network": {
        							"name": ["wan"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getDetectionConfig(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getDetectionConfig",
        					"params": {
        						"motion_detection": {
        							"name": ["motion_det"],
        							"table": ["region_info"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getAudioConfig(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getAudioConfig",
        					"params": {
        						"audio_config": {
        							"name": ["speaker", "microphone"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getRecordPlan(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getRecordPlan",
        					"params": {
        						"record_plan": {
        							"name": ["chn1_channel"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def setRecordPlan(self,deviceId,enabled="on"):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method" : "setRecordPlan",
        					"params" : {
        						"record_plan": {
        							"chn1_channel": {
        								"enabled": enabled,
                                        "monday": "[\"0000-2400:1\"]",
                                        "tuesday": "[\"0000-2400:1\"]",
                                        "wednesday": "[\"0000-2400:1\"]",
                                        "thursday": "[\"0000-2400:1\"]",
        								"friday": "[\"0000-2400:1\"]",
        								"saturday": "[\"0000-2400:1\"]",
        								"sunday": "[\"0000-2400:1\"]"
        							}
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def searchDateWithVideo(self,deviceId,fromDate="20220301",toDate="20220331"):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "searchDateWithVideo",
        					"params": {
        						"playback": {
        							"search_year_utility": {
        								"channel": [0],
                                        "start_date": fromDate,
        								"end_date": toDate
        							}
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response


    def getCloudConfig(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getCloudConfig",
        					"params": {
        						"cloud_config": {
        							"name": ["upgrade_info"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getMsgAlarmInfo(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getAlertConfig",
        					"params": {
        						"msg_alarm": {
        							"name": ["chn1_msg_alarm_info"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    def getDeviceShareListByPage(self):
        getParams = {
            "appName" : "TP-Link_Tapo_Android",
            "appVer" : "2.1.2",
            "netType" : "wifi",
            "termID" : self.clientUUID,
            "ospf" : "Android 7.0",
            "locale" : "es_ES",
            "token" : self.token
        }
        body = {
            "method" : "getDeviceShareListByPage",
            "params" : {
                "index" : 0,
                "limit" : 20,
                "shareRole": "sharer",
                "shareStatus": "ready"
            }
        }
        response = self.session.post(self.apiServer, params=getParams, json=body, verify=False).json()
        return response

    def getDeviceUserInfo(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
            "method" : "getDeviceUserInfo",
            "params" : {
                "deviceId" : deviceId
            }
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response


    def getAppComponentList(self,deviceId):
        getParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getAppComponentList",
        					"params": {
        						"app_component": {
        							"name": "app_component_list"
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response


    '''
    Move coordinates
    '''
    def move(self,deviceId,x,y):
        getParams = {
            'token': self.token
        }

        body = {
        	"method": "passthrough",
        	"params": {
                "deviceId": deviceId,
        		"requestData": {
                	"method": "multipleRequest",
                	"params": {
                		"requests": [{
                			"method": "motorMove",
                			"params": {
                				"motor": {
                					"move": {
                                        "x_coord" : x ,
                                        "y_coord" : y
                                    }
                				}
                			}
                		}]
                	}
                }
            }
        }

        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

        '''
    TODO: Move steps (just directions: x and y)
    '''
    def moveStep(self,deviceId):
        getParams = {
            'token': self.token
        }

        body = {
        	"method": "passthrough",
        	"params": {
                "deviceId": deviceId,
        		"requestData": {
                	"method": "multipleRequest",
                	"params": {
                		"requests": [{
                			"method": "motorMove",
                			"params": {
                				"motor": {
                					"movestep": {
                                        "direction" : "x"
                                    }
                				}
                			}
                		}]
                	}
                }
            }
        }

        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response


    def getCloudInfo(self,deviceId):

        getParams = {
            'token': self.token
        }

        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": deviceId,
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getCloudConfig",
        					"params": {
        						"cloud_config": {
        							"name": ["upgrade_info"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }

        response = self.session.post(self.apiServer, json=body, params=getParams, verify=False).json()
        return response

    '''
    TODO individual method with single verb with no global search
    to get the same info than getCameraConnectionInfo but using
    deviceId and model
    '''
    def getCameraInfo(self,token,id=None,model='C200'):
        return self.getCamerasInfo(token)

    '''
    Camera alerts
    '''
    def getCameraAlarms(self,deviceId):
        requestParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
                "deviceId": deviceId,
        		"requestData": {
                	"method": "multipleRequest",
                	"params": {
                		"requests": [{
                			"method": "getLastAlarmInfo",
                			"params": {
                				"system": {
                					"name": ["last_alarm_info"]
                				}
                			}
                		}]
                	}
                }
            }
        }
        response = self.session.post(self.apiServer, params=requestParams, json=body, verify=False).json()
        return response


    '''
    Camera status info
    '''
    def getCameraStatus(self,deviceId):
        requestParams = {
            'token': self.token
        }
        body = {
        	"method": "passthrough",
        	"params": {
        		"deviceId": "" + deviceId + "",
        		"requestData": {
        			"method": "multipleRequest",
        			"params": {
        				"requests": [{
        					"method": "getLedStatus",
        					"params": {
        						"harddisk_manage": {
        							"name": ["harddisk"],
        							"table": ["hd_info"]
        						}
        					}
        				}]
        			}
        		}
        	}
        }
        response = self.session.post(self.apiServer, params=requestParams, json=body, verify=False).json()
        return response


    '''
    Wifi connection info
    '''
    def getCameraConnectionInfo(self,id=None,token=None):
        requestParams = {
            'token': token
        }
        body = {
            "method":"passthrough",
            "params":{
                "deviceId" : str(id),
                "requestData" : {
                    "method" : "multipleRequest",
                    "params" : {
                        "requests" : [{
                            "method":"getConnectionType",
                            "params": {
                                "network" : {
                                    "get_connection_type":"null"
                                }
                            }
                        }]
                    }
                }
            }
        }
        response = self.session.post(server, params=requestParams, json=body, verify=False).json()
        return response

    '''
    Search global devices linked to your account and get the target info.
    If none is marked to seek, it gets the first one of the target type.
    '''
    def getCamerasInfo(self):
        devices = []
        totaldevs = 1
        while len(devices) < totaldevs:
            getParams = {
                'token': self.token
            }

            body = {
                'method': 'getDeviceListByPage',
                'params': {
                    'deviceTypeList': [
                        self.deviceType
                    ],
                    'index': len(devices),
                    'limit': 20
                }
            }

            response = self.session.post(self.url, json=body, params=getParams, verify=False).json()

            if response['error_code'] != 0:
                print('Listing error', file=sys.stderr)
                print(response, file=sys.stderr)
                sys.exit(1)

            totaldevs = response['result']['totalNum']
            devices.extend(response['result']['deviceList'])

        info = [x for x in devices if x['alias'] == self.seekCamera]
        if len(info) != 1:
            print('Cannot find default target "%s"' % self.seekCamera, file=sys.stderr)
            print('Received devices are:', file=sys.stderr)
            print(devices, file=sys.stderr)
            if len(devices)>0:
                print("Selecting lastest:")
                info = [x for x in devices if x['deviceType'] == self.deviceType]
                if len(info) == 0:
                    print('No cameras found, exitting...', file=sys.stderr)
                    return None
                else:
                    info = info[len(info)-1]
                    self.seekCamera = info["alias"]
                    print("Selected: %s" % self.seekCamera)
        else:
            info = info[0]
        return info

    '''
    Extracted from Android app, and used to choose remote server, it
    needs to be used before get a ssl camera instruction.
    '''
    def updateParams(self,cameraInfo=None):
        if not cameraInfo:
            cameraInfo = self.getCamerasInfo(self.token)
        self.apiServer = cameraInfo['appServerUrl']
        #like the android app
        if 'aps' in cameraInfo['appServerUrl']:
            self.server = 'aps1-relay-dcipc.i.tplinknbu.com'
        elif 'euw' in cameraInfo['appServerUrl']:
            self.server = 'euw1-relay-dcipc.i.tplinknbu.com'

    '''
    Returns session and cookies information to be used in next connection
    '''
    def getCameraResponse(self,deviceId):
        params = {
            'token': self.token
        }
        body = {
            'method': 'passthrough',
            'params': {
                'deviceId': deviceId,
                'requestData': {
                    'method':'do',
                    'relay': {
                        'request_relay': {
                            'token': self.token,
                            'version': self.version,
                            'stream_type': 0,
                            'protocol': 0,
                            'relay_server': self.server,
                            'relay_port': 80,
                            'relays_port': 443,
                            'relay_req_url': '/relayservice?deviceid=%s&type=video&resolution=%s' % (deviceId,self.quality),
                            'local_req_url': '/stream'
                        }
                    }
                }
            }
        }
        response = self.session.post(self.apiServer, params=params, json=body, verify=False).json()
        return response



    def getVideo(self):
        cameraInfo=self.getCamerasInfo(self.token)
        self.updateParams(cameraInfo)
        self.writeVideo(cameraInfo['deviceId'],self.token)


    '''
    This method keeps a ssl connection to get stream and stores the video in a file.
    It needs to be after send command petition and keep the current petition so this
    is the reason to made it in the same place

    TODO: also it's able to read and write live commands, but it's not managing that
    it could be a feature request
    '''
    def writeVideo(self,deviceId,targetFile='video.mp4'):

        cameraResponse = None
        #first needs elb_cookie and sid cookies identifiers
        while not cameraResponse or 'elb_cookie' not in cameraResponse['result']['responseData']['result']:
            cameraResponse = self.getCameraResponse(deviceId,self.token)

        #next build ssl connection
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with open(targetFile,'wb') as f:
            with socket.create_connection((self.server, 443)) as sockCon:
                with context.wrap_socket(sockCon, server_hostname=self.server) as sslCon:
                    sslPipe = sslCon.makefile('rwb')

                    requestHeaders = (
                        'POST /relayservice?deviceid=%s&type=video&resolution=%s HTTP/1.1\r\n' % (deviceId,self.quality)+
                        'User-Agent: Client=%s\r\n' % self.clientHeader +
                        'Keep-Relay: 3600\r\n' +
                        'Accept: */*\r\n' +
                        'Host: %s:443\r\n' % self.server +
                        'Content-Type: multipart/mixed;boundary=--random-boundary--\r\n' +
                        'Content-Length: %s\r\n' % str(4*8*1024*1024) +
                        'X-token: %s\r\n' % self.token +
                        'X-Client-Model: sm-g930f\r\n' +
                        'X-Client-UUID: %s\r\n' % self.clientUUID +
                        'X-Client-SessionID: %s\r\n' % cameraResponse['result']['responseData']['result']['sid'] +
                        'X-Redirect-Times: 0\r\n' +
                        'Cookie: %s\r\n' % cameraResponse['result']['responseData']['result']['elb_cookie'] +
                        '\r\n'
                    )
                    requestHeaders = requestHeaders.encode('ascii')
                    sslPipe.write(requestHeaders)

                    sslPipe.write(b'----random-boundary--\r\n')

                    requestBody = {
                        "type": "request",
                        "seq": 1,
                        "params": {
                            "method": "get",
                            "preview": {
                                "channels": [0],
                                "resolutions": [self.quality],
                                "audio": ["default"]
                            }
                        }
                    }
                    requestBody = json.dumps(requestBody).encode('ascii')

                    requestHeaders = (
                        'Content-Type: application/json\r\n' +
                        'Content-Length: ' + str(len(requestBody)) + '\r\n' +
                        '\r\n'
                    )
                    requestHeaders = requestHeaders.encode('ascii')

                    sslPipe.write(requestHeaders)
                    sslPipe.write(requestBody)
                    sslPipe.flush() #by the way

                    # Read header
                    relayStatus = sslPipe.readline().decode('ascii').rstrip('\r\n')
                    if relayStatus != 'HTTP/1.1 200 OK':
                        print('Unexpected relay status: ' + relayStatus, file=sys.stderr)
                        sys.exit(1)

                    replyHeaders = http.client.parse_headers(sslPipe)

                    while True:
                        boundaryLine = sslPipe.readline().decode('ascii')
                        if len(boundaryLine) == 0:
                            print('Reached EOL', file=sys.stderr)
                            break

                        if boundaryLine != '--' + replyHeaders.get_boundary() + '\r\n':
                            print('Unexpected boundary: %s' % boundaryLine, file=sys.stderr)
                            sys.exit(1)

                        chunkHeaders = http.client.parse_headers(sslPipe)
                        chunkType = chunkHeaders.get_content_type()
                        chunkLength = int(chunkHeaders.get('content-length'))

                        chunk = sslPipe.read(chunkLength)

                        if not chunkType.startswith('video/'):
                            print('Ignoring ' + chunkType, file=sys.stderr)
                            print("Printing command data sized at: %s bytes" % str(len(chunk)), file=sys.stderr)
                            print(chunk)
                        else:
                            #sys.stdout.buffer.write(sslPipe.read(chunkLength))
                            print("Video part: %s bytes" % str(len(chunk)), file=sys.stderr)
                            f.write(chunk)

                        boundaryLine = sslPipe.readline().decode('ascii')
                        if boundaryLine != '\r\n':
                            print('End of chunk new line missing', file=sys.stderr)
                            print(boundaryLine, file=sys.stderr)
                            break
