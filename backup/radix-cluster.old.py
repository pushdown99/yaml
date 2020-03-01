# -*- coding: utf-8 -*-
import yaml
import io

with open("radix-cluster.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for host in dict["hosts"]:
    f = open(host + ".properties", 'w')
	for k, v in dict[host].items():
		print(k, v)
    f.close()

print(dict["misc"]["date_pattern"])
print(dict["misc"]["layout_pattern"])



for i in range(1, 11):
    data = "%d번째 줄입니다.\n" % i
    f.write(data)
