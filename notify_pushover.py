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
import syslog

#
# Settings
#
ENABLE_LOG = True
LOG_FACILITY = syslog.LOG_LOCAL5
LOG_IDENT = "pushover" 

#
# Functions
#
logConnected=False
def logMsg(msg,level=syslog.LOG_INFO):
    global LOG_FACILITY,LOG_IDENT,logConnected
    if ENABLE_LOG:
        if not logConnected:
            syslog.openlog(LOG_IDENT, syslog.LOG_PID, LOG_FACILITY)
            logConnected=True
        print("LOG: %s" % msg)
        return syslog.syslog(level,msg)
    return True

#
# Main code
#

# Arguments parser
parser = argparse.ArgumentParser(description='Send Zabbix notification to Pushover enabled devices.')
parser.add_argument('user_key_app_token', metavar=('UserKey|AppToken'), type=str, help='Pushover User Key AND Application Token separated by |')
parser.add_argument('subject', metavar=('Subject'), type=str, help='Subject you want to push to the device(s).')
parser.add_argument('message', metavar=('Message'), type=str, help='Message you want to push to the device(s).')

# Argument processing
args = parser.parse_args()
user_key_app_token = args.user_key_app_token
subject = args.subject
message = args.message

# Check if UserKey and AppToken has been supplied
if "|" in user_key_app_token:
  user_key, app_token = user_key_app_token.split("|")
else:
  logMsg("Error: you must supply both User Key and App Token separated with |",syslog.LOG_ERR)
  sys.exit(1)
  
# Try to login with AcessToken
try:
    po = pushover.Client(user_key, api_token=app_token)
except (pushover.UserError) as exc:
    logMsg("Error: Can't connect to Pushover with User Key [%s]." % user_key, syslog.LOG_ERR)
    sys.exit(1)

# Try to send the notification
try:
    po.send_message(message, title=subject)
    logMsg("Pushover to user_key %s has been sent with sunject %s" % (user_key,subject))
except (pushover.RequestError) as exc:
    logMsg("Error: Can't send notification to Pushover devices: %s" % str(exc), syslog.LOG_ERR)
    sys.exit(1)

# Exit with success
logMsg("Success: Message sent with UserKey [%s] with Subject [%s]" % (user_key, subject))
sys.exit(0)

