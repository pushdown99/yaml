#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import io
import os

######################################################################################################
#
# RADIX SERVICES: YAML
#
with open("/opt/radix/bin/kaa-service.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

    if not os.path.isdir("/opt/"):
      os.mkdir("/opt/")
    if not os.path.isdir("/opt/radix/"):
      os.mkdir("/opt/radix/")
    if not os.path.isdir("/opt/radix/conf"):
      os.mkdir("/opt/radix/conf")

    ######################################################################################################
    #
    # SERVICES: /opt/radix/conf/services
    #
    f = open("/opt/radix/conf/services", 'w')
    
    for service in dict["services"]:
        d = "%s=%s\n" % (service, dict["port"][service])
        f.write(d)
    f.close()

    ######################################################################################################
    #
    # TTY: /opt/radix/conf/tty
    #
    f = open("/opt/radix/conf/tty", 'w')
    d = "host=%s\n" % (dict["tty"]["host"])
    f.write(d)
    d = "username=%s\n" % (dict["tty"]["username"])
    f.write(d)
    d = "password=%s\n" % (dict["tty"]["password"])
    f.write(d)
    d = "ssl-cert=%s\n" % (dict["tty"]["ssl-cert"])
    f.write(d)
    d = "ssl-key=%s\n" % (dict["tty"]["ssl-key"])
    f.write(d)
    d = "token=%s\n" % (dict["tty"]["token"])
    f.write(d)
    f.close()

