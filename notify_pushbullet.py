#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PushBullet notification script for Zabbix
# 
# Author:
#   Sébastien RICCIO - sr@swisscenter.com
#
# Purpose:
#   Push zabbix notifications to Pushbullet enabled devices
#   See: https://www.pushbullet.com
#
# Requirements:
#   pip install pushbullet.py
#
# Changelog:
#   20161231 - First revision
#

import pushbullet
import argparse
import sys
import time

#
# Settings
#
ENABLE_LOG = True
LOG_FILE = "/var/log/zabbix/notify_pushbullet.log"


#
# Functions
#
def findDevice(devices, value):
    """
    Return a device from devices if name matches (case insensitive)
    """
    for device in devices:
        if value.lower() == device.nickname.lower(): return device.nickname
    
          
def l(msg):
    """
    Send log line to stdout and to LOG_FILE if logging is enabled
    """
    msg = "[%s] %s" % (logTimeStamp(), msg)

    # Print to stdout
    print(msg)

    # Output to logfile
    if ENABLE_LOG:
        try:
            lf = open(LOG_FILE, 'a')
            lf.write("%s\n" % (msg))

        except (OSError) as exc:
            print("Error while trying to log event: %s" % rlb(str(exc)))
            return False
        
        lf.close()    

    return True


def logTimeStamp():
    """
    Return current date/time formatted for log output
    """
    return  time.strftime('%a %b %d %H:%M:%S %Y')


#
# Main code
#

# Arguments parser
parser = argparse.ArgumentParser(description='Send Zabbix notification to Pushbullet enabled devices.')
parser.add_argument('access_token', metavar=('AccessToken'), type=str, help='Pushbullet access token that you can generate on Pushbullet website.')
parser.add_argument('subject', metavar=('Subject'), type=str, help='Subject you want to push to the device(s).')
parser.add_argument('message', metavar=('Message'), type=str, help='Message you want to push to the device(s).')

# Argument processing
args = parser.parse_args()
access_token = args.access_token
subject = args.subject
message = args.message

# Check if a destination device has been supplied
device = "all"
if "|" in access_token:
    access_token, device = access_token.split("|")
    
# Try to login with AcessToken
try:
    pb = pushbullet.Pushbullet(access_token)
except (pushbullet.InvalidKeyError) as exc:
    l("Error: Can't connect to Pushbullet with AccessToken [%s]: %s" % (access_token, str(exc)))
    sys.exit(1)

# Select the right device if specified
if not device == "all":
    found_device = findDevice(pb.devices, device)
    if not found_device:
        l("Error: Device [%s] not found." % device)
        sys.exit(1)

    else: device = found_device    
    
    try:
        pb = pb.get_device(found_device)
    except (pushbullet.InvalidKeyError) as exc:
        l("Error: Cannot select device [%s]." % device)
        sys.exit(1)

# Try to send the notification
try:
    push = pb.push_note(subject, message)
except (pushbullet.PushError) as exc:
    l("Error: Can't send notification to Pushbullet devices [%s]." % found_device)
    sys.exit(1)

# Exit with success
l("Success: Message sent with AccessToken [%s] to device [%s]!" % (access_token, device))
sys.exit(0)