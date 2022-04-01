#!/usr/bin/env python3

import time
from pyModbusTCP.client import ModbusClient

try:
    c = ModbusClient(host="192.168.4.94", port=502, unit_id=4)
except ValueError:
    print("Error with host or port params")
    exit()

# Read temperature
while True:
  if c.is_open():
    reg = c.read_holding_registers(40000, 1)
    temp = reg[0] / 10
    print("Temp:",temp)
    break
  else:
    c.open()
    time.sleep(0.2)
