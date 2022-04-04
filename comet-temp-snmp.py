#!/usr/bin/env python3

import time
import urllib3
import requests
from pysnmp.hlapi import *

################################################
# Send Message to VMware LogInsight via REST API
################################################
def sendMsgToLogInsight(ip,msg):
  api_url = "https://" + ip + ":9543/api/v1/events/ingest/1"
  json_msg = {"events": [{"text": msg }]}
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  response = requests.post(api_url, json=json_msg, verify=False)
  return response

##########################################
# Main app code - read temperature 
##########################################
def main():
  ip_address = "192.168.4.94"
  temp = "none"

  for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in bulkCmd(SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((ip_address, 161)),
        ContextData(),
        0, 10,  # fetch up to 10 OIDs one-shot
        ObjectType(ObjectIdentity('.1.3.6.1.4.1.22626.1.5.2.1.2.0'))):
    if errorIndication or errorStatus:
        print(errorIndication or errorStatus)
        break
    else:
        print(varBinds)
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

  # Send to LogInsight
  log_message = "Comet device: P8510 IP: " + ip_address + " Proto: SNMP Temperature: " + str(temp)
  print("Log message:",log_message)
  response=sendMsgToLogInsight("syslog.home.uw.cz",log_message)
  print ("Response:", response)

# Main
main()
