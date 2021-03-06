#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import time
import re

if len(sys.argv) < 2:
    print("Usage: %s IFACE [INTERVAL]" % sys.argv[0])
    exit()

interval = 1
max_idle = 600
interface = sys.argv[1]

if len(sys.argv) > 2:
    interval = int(sys.argv[2])


def get_bytes():
    data = os.popen('ifconfig '+interface).read()
    m = re.search("RX (?:packets \d+\s*)bytes(?::? *)(\d+)", data)
    rxb = int(m.group(1))
    m = re.search("TX (?:packets \d+\s*)bytes(?::? *)(\d+)", data)
    txb = int(m.group(1))
    return rxb, txb


try:
    rxb0, txb0 = get_bytes()
except Exception as e:
    print("Error getting data (see other messages)")
    print(e)
    exit()

print("If you see this, it's working. Exit with Ctrl-C.")
sys.stdout.flush()


def human_format(n):
    if n > 2**20:
        return "%6.1f MB" % (n/2.0**20,)
    if n > 2**10:
        return "%6.1f KB" % (n/2.0**10,)
    return "%6d B " % n


class Blinker:
    def __init__(self):
        self.last_status = 0  # success

    def on(self):
        if self.last_status == 0:
            self.last_status = os.system('xset led 3')

    def off(self):
        if self.last_status == 0:
            self.last_status = os.system('xset -led 3')


blinker = Blinker()
idle_secs = 0
maxtx, maxrx = 0, 0
next_report = interval

while True:
    try:
        time.sleep(interval)
        blinker.off()
    except:
        print()
        break

    try:
        rxb, txb = get_bytes()
    except:
        print("Error retrieving data, quitting!")
        break

    if (rxb, txb) == (rxb0, txb0):
        idle_secs += interval
        if idle_secs == next_report:
            print(time.strftime('%H:%M:%S') + " %d seconds idle" % idle_secs)
            sys.stdout.flush()
            if next_report < max_idle:
                next_report *= 2
            else:
                next_report += max_idle
        continue
    else:
        if idle_secs > 0:
            print(time.strftime('%H:%M:%S') + " resume after %d seconds" % idle_secs)
        idle_secs = 0
        next_report = interval
    blinker.on()
    print(
        time.strftime('%H:%M:%S'),
        "Recv %s, Send %s. Total: %s, %s." % tuple(
            map(human_format, (rxb-rxb0, txb-txb0, rxb, txb))
        )
    )
    sys.stdout.flush()
    maxtx = max(maxtx, txb-txb0)
    maxrx = max(maxrx, rxb-rxb0)
    rxb0, txb0 = rxb, txb

print("Bye, max speeds were: {}/s, {}/s.".format(
    human_format(maxrx/interval), human_format(maxtx/interval)
))
