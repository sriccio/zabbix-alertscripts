# Zabbix alertscripts #

![PyPi downloads](https://img.shields.io/github/downloads/sriccio/zabbix-alertscripts/total.svg)

A nice and little collection of alerts scripts to be used with the [Zabbix](https://www.zabbix.com/) network monitoring solution.

At the moment the available scripts are:

* [**notify_pushbullet.py**](#pushbullet) - Send notifications using [Pushbullet](https://www.pushbullet.com/)
* [**notify_pushover.py**](#pushover) - Send notifications using [Pushover](https://www.pushover.net/)

<a name="pushbullet"></a>
## notify_pushbullet.py ##

Zabbix alert script to send notifications using [Pushbullet](https://www.pushbullet.com/)

### Requirements
```bash
pip install pushbullet.py
```
### Usage
```
usage: notify_pushbullet.py [-h] "AccessToken(|DeviceName)" "Subject Message"

Send Zabbix notification to Pushbullet enabled devices.

positional arguments:
  AccessToken(|DeviceName)
                        Pushbullet Access Token that and optional DeviceName
                        if targetting a specific device.
  Subject               Subject you want to push to the device(s).
  Message               Message you want to push to the device(s).

optional arguments:
  -h, --help            show this help message and exit
```
### Getting started
You first need to register for an account at [Pushbullet](https://www.pushbullet.com/) and download/install the clients for your devices (Android/iOS/Windows...).
You will then able to retrieve your *AccessToken* that you will need to provide in your zabbix user media configuration.

Copy the *notify_pushbullet.py* script to your Zabbix alert scripts directory. Usually this is */usr/lib/zabbix/alertscripts* but configuration can differs depending on how you installed Zabbix. In doubt, check your *zabbix_server.conf*.

### Configure the media type

Go to your Zabbix *Administration / Media types* screen and add a new media.
Specify the name of the script in script name and check that the parameters are correct.

![Configuration screen](https://raw.githubusercontent.com/sriccio/resources/master/images/zabbix-alertscripts/pushbullet_media.png)

### Configure the user media

You will need then to add the media to your users. For this just edit an user and add a media selecting the one you just created before.
Specify the Access Token in the *Send to* field.

![Configuration screen](https://raw.githubusercontent.com/sriccio/resources/master/images/zabbix-alertscripts/pushbullet_usermedia1.png)

If you have multiple devices on your Pushbullet account and want to target only one device, you can specify the device name in the *Send to* field separated from Access Token with a | .

![Configuration screen](https://raw.githubusercontent.com/sriccio/resources/master/images/zabbix-alertscripts/pushbullet_usermedia2.png)

And voila, you're ready to use Pushbullet notifications!

<a name="pushover"></a>
## notify_pushover.py ##

Zabbix alert script to send notifications using [Pushover](https://www.pushover.net/)

### Requirements
```bash
pip install python-pushover
```
### Usage
```
usage: notify_pushover.py [-h] "UserKey|AppToken" "Subject Message"

Send Zabbix notification to Pushover enabled devices.

positional arguments:
  UserKey|AppToken  Pushover User Key AND Application Token separated by |
  Subject           Subject you want to push to the device(s).
  Message           Message you want to push to the device(s).

optional arguments:
  -h, --help        show this help message and exit
```
### Getting started
You first need to register for an account at [Pushover](https://www.pushover.net/) and download/install the clients for your devices (Android/iOS/Windows...).
You will then able to retrieve your *UserKey* and *AppToken* that you will need to provide in your zabbix user media configuration.

Copy the *notify_pushover.py* script to your Zabbix alert scripts directory. Usually this is */usr/lib/zabbix/alertscripts* but configuration can differs depending on how you installed Zabbix. In doubt, check your *zabbix_server.conf*.

### Configure the media type

Go to your Zabbix *Administration / Media types* screen and add a new media.
Specify the name of the script in script name and check that the parameters are correct.

![Configuration screen](https://raw.githubusercontent.com/sriccio/resources/master/images/zabbix-alertscripts/pushover_media.png)

### Configure the user media

You will need then to add the media to your users. For this just edit an user and add a media selecting the one you just created before.
Specify the UserKey and AppToken in the *Send to* field, separated by a | .

![Configuration screen](https://raw.githubusercontent.com/sriccio/resources/master/images/zabbix-alertscripts/pushover_user_media.png)

And voila, you're ready to use Pushbullet notifications!

