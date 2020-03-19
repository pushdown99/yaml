# -*- coding: utf-8 -*-
import yaml
import io
import os

######################################################################################################
#
# CLUSTER CONFIGURATION: YAML
#
with open("/opt/radix/bin/logs-config.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

######################################################################################################
#
# LOG CONFIGURATION
#
conf = "/opt/radix/probe/"

if not os.path.isdir(conf):
  os.mkdir(conf)

for log in dict["logs"]:

  f = open(conf + log, 'w')
  d = "source=%s\n" % str(dict[log]["source"]).lower()
  f.write(d)
  d = "sink=%s\n" % str(dict[log]["sink"]).lower()
  f.write(d)
  f.close()

sink = "/opt/radix/sink/"

if not os.path.isdir(sink):
  os.mkdir(sink)

f = open(sink + "log-sink", 'w')
d = "source=%s\n" % str(dict["log-sink"]["sink"]).lower()
f.write(d)
f.close()

