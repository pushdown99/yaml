#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import io
import os
import subprocess
import time
import random
import secrets

def encBcrypt (password):
    return subprocess.check_output("/opt/radix/bin/bcrypt " + str(password), shell=True)

def genDigitToken(n):
    num = random.randrange(1, 10**n)
    num_with_zeros = '{:03}'.format(num)
    return (num_with_zeros)

def genSecureToken(n):
    return secrets.token_urlsafe(n)

with open("/opt/radix/bin/kaa-db.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

##############################################################################################################

PREFIX = '/opt/radix/bin'

admin = dict["tenant"]["admin"]
developer = dict["tenant"]["developer"]
application = dict["tenant"]["application"]

Timestamp = int(time.time()*1000)
KaaAdmin = { 'username': dict["admin"]["username"], 'password': encBcrypt(dict["admin"]["password"]) }
Tenant = { 'name': dict["tenant"]["name"] }
TenantAdmin = { 'username': dict["tenant"]["admin"], 'password': encBcrypt(dict["users"][admin]["password"]), 'mail': dict["users"][admin]["mail"] }
TenantDeveloper = { 'username': developer, 'password': encBcrypt(dict["users"][developer]["password"]), 'mail': dict["users"][developer]["mail"], 'verifier': dict["users"][developer]["verifier"] }
Application = { 'name': application, 'token': dict["applications"][application]["token"] }
SDK = { 'name': dict["applications"][application]["sdk"]["name"], 'token': dict["applications"][application]["sdk"]["token"] }

if (TenantDeveloper['verifier'] == None):
    TenantDeveloper['verifier'] = genDigitToken (20)

if (Application['token'] == None):
    Application['token'] = genDigitToken (20)

if (SDK['token'] == None):
    SDK['token'] = genSecureToken (10) + "-" + genSecureToken (16)

print (Tenant)
print (TenantDeveloper)
print (Application)
print (SDK)

f = open(PREFIX + "/db.properties", 'w')
d = "TIMESTAMP=%d\n" \
    "TENANT=%s\n" \
    "KAA_USERNAME=%s\n" \
    "KAA_PASSWORD=%s\n" \
    "ADMIN_USERNAME=%s\n" \
    "ADMIN_PASSWORD=%s\n" \
    "ADMIN_MAIL=%s\n" \
    "DEVELOPER_USERNAME=%s\n" \
    "DEVELOPER_PASSWORD=%s\n" \
    "DEVELOPER_MAIL=%s\n" \
    "APP_NAME=%s\n" \
    "APP_TOKEN=%s\n" \
    "USER_VERIFIER=%s\n" \
    "SDK_NAME=%s\n" \
    "SDK_TOKEN=%s\n" % (Timestamp, Tenant['name'], KaaAdmin['username'], KaaAdmin['password'], TenantAdmin['username'], TenantAdmin['password'], TenantAdmin['mail'], TenantDeveloper['username'], TenantDeveloper['password'], TenantDeveloper['mail'], Application['name'], Application['token'], TenantDeveloper['verifier'], SDK['name'], SDK['token'])

f.write(d)
f.close()

