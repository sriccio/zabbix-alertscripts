#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pushover notification script for Zabbix
# 
# Author:
#   Sébastien RICCIO - sr@swisscenter.com
#
# Purpose:
#   Push zabbix notifications to Pushover enabled devices
#   See: https://pushover.net/
#
# Requirements:
#   pip install python-pushover
#
# Changelog:
#   20170101 - First revision
#

import argparse
import sys
import time
import pushover

#
# Settings
#
ENABLE_LOG = True
LOG_FILE = "/var/log/zabbix/notify_pushover.log"


#
# Functions
#
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


def rlb(thing):
  """
  Return thing with line breaks replaced by spaces
  """
  return thing.replace("\r", " ").replace("\n", " ")

#
# Main code
#

# Arguments parser
parser = argparse.ArgumentParser(description='Send Zabbix notification to Pushover enabled devices.')
parser.add_argument('apptoken', metavar=('AppToken'), type=str, help='Pushover Application Token')
parser.add_argument('userkey', metavar=('UserKey'), type=str, help='Pushover User Key')
parser.add_argument('subject', metavar=('Subject'), type=str, help='Subject you want to push to the device(s)')
parser.add_argument('message', metavar=('Message'), type=str, help='Message you want to push to the device(s)')

# Argument processing
args = parser.parse_args()
user_key = args.userkey
app_token = args.apptoken
subject = args.subject
message = args.message

#Check if AppToken has been supplied
if not app_token:
  l("Error: you must supply an App Token")
  sys.exit(1)

# Check if UserKey and AppToken has been supplied
if not app_token:
  l("Error: you must supply a User Key")
sys.exit(1)

# Try to login with AcessToken
try:
    po = pushover.Client(user_key, api_token=app_token)
except (pushover.UserError) as exc:
    l("Error: Can't connect to Pushover with User Key [%s]." % user_key)
    sys.exit(1)

# Try to send the notification
try:
    po.send_message(message, title=subject)
except (pushover.RequestError) as exc:
    l("Error: Can't send notification to Pushover devices: %s" % rlb(str(exc)))
    sys.exit(1)

# Exit with success
l("Success: Message sent with UserKey [%s] to AppToken [%s]" % (user_key, app_token))
sys.exit(0)
