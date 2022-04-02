#!/usr/bin/env python3

import time
import urllib3
import requests
from pyModbusTCP.client import ModbusClient

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

  try:
    # Initialize Modbus Client over TCP
    #   Default port is 502
    c = ModbusClient(host=ip_address, port=502, unit_id=4)
  except ValueError:
    print("Error with host or port params")
    exit()

  # Read temperature
  while True:
    if c.is_open():
      # Read temperature value
      #   address => The starting register address to read from
      #              4000 is Channel 1 temperature
      #   count   => The number of registers to read
      #   c.read_holding_registers(address=40000, count=1)
      reg = c.read_holding_registers(40000, 1)
      temp = reg[0] / 10
      break
    else:
      c.open()
      time.sleep(0.2)

  # Send to LogInsight
  log_message = "Comet device: P8510 IP: " + ip_address + " Proto: Modbus Temperature: " + str(temp)
  print("Log message:",log_message)
  response=sendMsgToLogInsight("syslog.home.uw.cz",log_message)
  print ("Response:", response)

# Main
main()
