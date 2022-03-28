#!/bin/bash

ip="192.168.191.1"

response=$(curl -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' \
    -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' \
    -H $'Content-Length: 108' -H $'Connection: close' \
    --data-binary $'{\"method\":\"login\",\"params\":{\"hashed\":true,\"password\":\"4004117BFDADDA243025EA2CFA702A9D\",\"username\":\"admin\"}}' \
    $"https://$ip/")

echo "response is: $response"
stok=$(echo $response | jq '.result.stok' | tr -d '"')
echo "stok is: $stok"

#get device info
response=$(curl -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' -H $'Content-Length: 299' -H $'Connection: close' \
    --data-binary $'{\"method\":\"multipleRequest\",\"params\":{\"requests\":[{\"method\":\"getDeviceInfo\",\"params\":{\"device_info\":{\"name\":[\"basic_info\"]}}},{\"method\":\"getLastAlarmInfo\",\"params\":{\"system\":{\"name\":[\"last_alarm_info\"]}}},{\"method\":\"getAppComponentList\",\"params\":{\"app_component\":{\"name\":[\"app_component_list\"]}}}]}}' \
    $"https://$ip/stok=$stok/ds")

echo "respons2 is: $response"

response=$(curl -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' -H $'Content-Length: 124' -H $'Connection: close' \
    --data-binary $'{\"method\":\"multipleRequest\",\"params\":{\"requests\":[{\"method\":\"getLightFrequencyInfo\",\"params\":{\"image\":{\"name\":\"common\"}}}]}}' \
    $"https://$ip/stok=$stok/ds")

echo "response3 is: $response"

response=$(curl -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' -H $'Content-Length: 223' -H $'Connection: close' \
    --data-binary $'{\"method\":\"multipleRequest\",\"params\":{\"requests\":[{\"method\":\"getCircularRecordingConfig\",\"params\":{\"harddisk_manage\":{\"name\":[\"harddisk\"]}}},{\"method\":\"getSdCardStatus\",\"params\":{\"harddisk_manage\":{\"table\":[\"hd_info\"]}}}]}}' \
    $"https://$ip/stok=$stok/ds")

echo "\\nresponse5: $response"

response=$(curl -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' -H $'Content-Length: 245' -H $'Connection: close' \
    --data-binary $'{\"method\":\"multipleRequest\",\"params\":{\"requests\":[{\"method\":\"getClockStatus\",\"params\":{\"system\":{\"name\":\"clock_status\"}}},{\"method\":\"getTimezone\",\"params\":{\"system\":{\"name\":\"basic\"}}},{\"method\":\"getDstRule\",\"params\":{\"system\":{\"name\":\"dst\"}}}]}}' \
    $"https://$ip/stok=$stok/ds")
echo "\\nresponse6: $response"


response=$(curl -i -s -k -X $'POST' \
    -H $"Host: $ip" -H $"Referer: https://$ip:443" -H $'Accept: application/json' -H $'Accept-Encoding: gzip, deflate' -H $'User-Agent: Tapo CameraClient Android' -H $'Requestbyapp: true' -H $'Content-Type: application/json; charset=UTF-8' -H $'Content-Length: 124' -H $'Connection: close' \
    --data-binary $'{\"method\":\"multipleRequest\",\"params\":{\"requests\":[{\"method\":\"getLightFrequencyInfo\",\"params\":{\"image\":{\"name\":\"common\"}}}]}}' \
    $"https://$ip/stok=$stok/ds")

echo "\\nresponse7: $response"

#screenshot
username="tplink"
password="tplink"

ffmpeg -loglevel fatal -i "rtsp://$username:$password@$ip:554/stream1" -vframes 1 -r 1 snapshot-timestamp.jpg
