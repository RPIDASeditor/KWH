#!/usr/bin/env python

import sys
import time
import pigpio

RX = 9 #21
TX = 10 #19
TXRX = 27 #13

MSGLEN = 256
baud = 1200
bits = 8
char_time = 10 / float(baud)

# Request for voltage
# 01  04  00  00  00  02  71  BC

MASK=(1<<bits)-1
msg = [0] * (MSGLEN)
for i in range(len(msg)):
	if i < 10:
		msg[i] = 0 & MASK
	else:
		msg[i] = 170 & MASK

#msg[0] = 1 & MASK
#msg[1] = 4 & MASK
#msg[2] = 0 & MASK
#msg[3] = 0 & MASK
#msg[4] = 0 & MASK
#msg[5] = 2 & MASK
#msg[6] = 114 & MASK
#msg[7] = 188 & MASK

pi = pigpio.pi()
pi.set_mode(TX, pigpio.OUTPUT)
pi.set_mode(RX, pigpio.INPUT)
pi.set_mode(TXRX, pigpio.OUTPUT)
pi.write(TXRX, 1)
pigpio.exceptions = False
pi.bb_serial_read_close(RX)
pigpio.exceptions = True
pi.wave_clear()
print ("")
msg = sys.argv[1]
print ("Transmitting: ", msg)

#sending the wave
pi.wave_add_new()
pi.wave_add_serial(TX, baud, msg, 8, 8)
wid = pi.wave_create()
pi.wave_send_once(wid)
while (pi.wave_tx_busy()):
        time.sleep(0.1)
pi.wave_delete(wid)

#receiving the wave
text = ""
nonsense = 0
pi.write(TXRX, 0)
pi.bb_serial_read_open(RX, baud)
while (True):
    (count, data) = pi.bb_serial_read(RX)
    if (count):
        text += data
    nonsense += 1
    if (nonsense > 1000):
        break

print ("data: ", text)

pi.bb_serial_read_close(RX)
print ''.join('{:02b}'.format(x) for x in text)
pi.stop()



