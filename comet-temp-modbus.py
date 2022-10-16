#!/usr/bin/env python3

import time
import urllib3
import requests
from pyModbusTCP.client import ModbusClient

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

  # Open Client
  c.open()
  time.sleep(1)

  # Read temperature value
  #   address => The starting register address to read from
  #              4000 is Channel 1 temperature
  #   count   => The number of registers to read
  #   c.read_holding_registers(address=40000, count=1)
  reg = c.read_holding_registers(40000, 1)
  temp = reg[0] / 10

  # Print log message
  log_message = "Comet device: P8510 IP: " + ip_address + " Proto: Modbus Temperature: " + str(temp)
  print("Log message:",log_message)

# Main
main()
