# -*- coding: utf-8 -*-
import yaml
import io
import os

######################################################################################################
#
# CLUSTER CONFIGURATION: YAML
#
with open("/opt/radix/bin/kaa-logs.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

######################################################################################################
#
# LOG CONFIGURATION
#
PROBE = "/opt/radix/probe/"

if not os.path.isdir(PROBE):
  os.mkdir(PROBE)

for log in dict["logs"]:

  f = open(PROBE + log, 'w')
  d = "source=%s\n" % str(dict[log]["source"]).lower()
  f.write(d)

  d = "sink=%s\n" % str(dict[dict[log]["sink"]]["sink"]).lower()
  f.write(d)

  if ((dict[log]["allow"] == None) or (len(dict[log]["allow"])==0)):
    d = "allow="
  else:
    d = "allow=grep -i \""
    for token in  dict[log]["allow"]:
      d += token + "\|"
    d += "EOF\"\n"
  f.write(d)

  if ((dict[log]["deny"] == None) or (len(dict[log]["deny"])==0)):
    d += "deny="
  else:
    d = "deny=grep -i \""
    for token in  dict[log]["deny"]:
      d += token + "\|"
    d += "EOF\"\n"
  f.write(d)

  f.close()

SINK = "/opt/radix/sink/"

if not os.path.isdir(SINK):
  os.mkdir(SINK)

f = open(SINK + "log-sink", 'w')
d = "source=%s\n" % str(dict["log-sink"]["sink"]).lower()
f.write(d)
f.close()

