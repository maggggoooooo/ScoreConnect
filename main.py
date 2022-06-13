#!/user/bin/env
import time

import serial

ser = serial.Serial(
  port='/dev/ttyUSB2',
  baudrate=19200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

while 1:
  msg=ser.readline()
  print(msg.decode('utf-8'))
