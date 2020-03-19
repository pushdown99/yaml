#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import io
import os
import subprocess
import pymysql
import time
import bcrypt
import random
import secrets
import warnings

conn = pymysql.connect(host='kaa-1.tric.kr', user='sqladmin', password='admin', db='kaa', charset='utf8', autocommit=True)
curs = conn.cursor(pymysql.cursors.DictCursor)
curs.execute('SET NAMES utf8;') 
curs.execute('SET CHARACTER SET utf8;')
curs.execute('SET character_set_connection=utf8;')
curs.execute("SET global sql_mode=%s", ("NO_BACKSLASH_ESCAPES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"))

with open("/opt/radix/bin/kaa-admin.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

##############################################################################################################

KaaAdmin = { 'username': dict["admin"]["username"], 'password': dict["admin"]["password"] }

TenantAdmin = {} 
TenantDeveloper = {} 
TenantUser = {} 
Tenant = {}
Application = {}
EndPointGroup = {}

Timestamp = int(time.time()*1000)

KAA_ADMIN        = 'KAA_ADMIN'
TENANT_ADMIN     = 'TENANT_ADMIN'
TENANT_DEVELOPER = 'TENANT_DEVELOPER'
TENANT_USER      = 'TENANT_USER'

def mysqlFetchAll (sql):
    try:
        if curs.connection:
            curs.execute(sql)
            return curs.fetchall()
        else:
            print ("[mysql] curs disconnected")
            return None
    except Exception as e:
        print (str(e))
        return None

def mysqlFetchOne (sql):
    try:
        if curs.connection:
            curs.execute(sql)
            return curs.fetchone()
        else:
            print ("[mysql] curs disconnected")
            return None
    except Exception as e:
        print (str(e))
        return None

def mysqlExecute (sql, parameters):
    try:
        curs.execute (sql, parameters)
        conn.commit()
        return None
    except Exception as e:
       print ("[mysql] %s" % (str(e)))
       return None

def mysqlRun (sql):
    sql = "set global sql_mode=\"NO_BACKSLASH_ESCAPES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION\";" + sql
    command = "/usr/bin/mysql -N -s  -usqladmin -padmin kaa -e \"%s\"" % (sql)
    os.system(command)

def getMaxTenantId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM tenant")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxAdminUserId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM admin_user")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxKaaUserId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM kaa_user")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxAdminAuthorityId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM admin_authority")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxAppId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM application")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxEndPointGroupId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM endpoint_group")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxBaseSchems ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM base_schems")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxCtlMetainfo ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM ctl_metainfo")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])


def getTenant (tenant):
    row = mysqlFetchOne ("SELECT * FROM tenant WHERE name='" + tenant + "'")
    return row

def putTenant (tenant):
    row =  getTenant (tenant)
    if (row != None):
        return row
    else:
        mysqlExecute ("INSERT INTO tenant (id, name) VALUES (%s,%s)", (int(getMaxTenantId()+1), tenant))
    return {'id':getMaxTenantId(), 'name': tenant}
        
def getAdminUser (username):
    row = mysqlFetchOne ("SELECT * FROM admin_user WHERE username='" + username + "'")
    return row

def getKaaUser (username):
    row = mysqlFetchOne ("SELECT * FROM kaa_user WHERE user_name='" + username + "'")
    return row

def getAdminAuthority (userId):
    row = mysqlFetchOne ("SELECT * FROM admin_authority WHERE user_id=" + str(userId))
    return row

def putUser(u):
    AdminUser = getAdminUser (u['username'])
    if(AdminUser == None):
        mysqlExecute ("INSERT INTO admin_user VALUES (%s,_binary %s,%s,%s,%s,%s,NULL,_binary %s,%s)",(int(getMaxAdminUserId()+1), '^A', u['firstName'], u['lastName'], u['mail'], u['password'], '\0', u['username']))
        AdminUser = getAdminUser (u['username'])
    KaaUser = getKaaUser (u['username'])
    if(KaaUser == None):
        mysqlExecute ("INSERT INTO kaa_user VALUES (%s,%s,%s,%s,%s)", (int(getMaxKaaUserId()+1), u['authority'], str(AdminUser['id']), AdminUser['username'], int(Tenant['id'])))
    AdminAuthority = getAdminAuthority (AdminUser['id'])
    if(AdminAuthority == None):
        mysqlExecute ("INSERT INTO admin_authority VALUES (%s,%s,%s)", (int(getMaxAdminAuthorityId()+1), u['authority'], int(AdminUser['id'])))
    return AdminUser

def getApp (name):
    row = mysqlFetchOne ("SELECT * FROM application WHERE name='" + name + "'")
    return row

def putApp (a):
    row = getApp (a['name']) 
    if (row == None):
        mysqlExecute ("INSERT INTO application VALUES (%s,%s,%s,%s,%s,%s)",(int(getMaxAppId()+1), a['token'], a['credentials'], a['name'], int(0), int(Tenant['id'])))
        row = getApp(a['name'])
    return row

def getEndPointGroup (id, name='All'):
    row = mysqlFetchOne ("SELECT * FROM endpoint_group WHERE application_id = " + str(id) + " and name='" + name + "'")
    return row

def putEndPointGroup (a):
    row = getEndPointGroup (Application['id'])
    if (row == None):
        mysqlExecute ("INSERT INTO endpoint_group VALUES (%s,%s,%s,NULL,0,%s,0,0,%s)",(int(getMaxEndPointGroupId()+1), int(Timestamp), TenantAdmin['username'], "All", Application['id']))
        row = getEndPointGroup (Application['id'])
    return row

def getBaseSchems (application_id, ctl_id):
    row = mysqlFetchAll ("SELECT * FROM ctl_metainfo WHERE application_id = " + str(application_id) + " and ctl_id=" + str(ctl_id))
    return row

def putBaseSchems ():
    row = getBaseSchems ()

def getCtlMetainfo (c):
    row = mysqlFetchOne ("SELECT * FROM ctl_metainfo  WHERE fqn = '" + c['fqn'] + "' and application_id = " + str(Application['id']) + " and tenant_id=" + str(Tenant['id']))
    return row

def putCtlMetainfo (c):
    row = getCtlMetainfo (c)
    if (row == None):
        mysqlExecute ("INSERT INTO ctl_metainfo VALUES (%s,%s,%s,%s)",(int(getMaxCtlMetainfo()+1), c['fqn'], Application['id'], Tenant['id']))
        row = getCtlMetainfo (c)
    return row

def getCtl (c):
    row = mysqlFetchOne ("SELECT * FROM ctl  WHERE metainfo_id = " + str(c['metainfo_id']))
    return row

def putCtl (c):
    row = getCtl (c)
    if (row == None):
        row = putCtlMetainfo (c)
        c['metainfo_id'] = row['id']
    return row

def encrypt (password):
    return subprocess.check_output("/opt/radix/bin/bcrypt " + str(password), shell=True)
    return bcrypt.hashpw(password, bcrypt.gensalt())

def genDigitToken(n):
    num = random.randrange(1, 10**n)
    num_with_zeros = '{:03}'.format(num)
    return (num_with_zeros)

def genSecureToken(n):
    return secrets.token_urlsafe(n)

def getUserYaml (user, authority):
    if (dict["users"][user] == None):
        return None
    return {'username': user, 'mail': dict["users"][user]["mail"], 'password': encrypt(dict["users"][user]["password"]), 'firstName': dict["users"][user]["firstName"], 'lastName': dict["users"][user]["lastName"], 'authority': authority}

def getAppYaml (name):
    if (dict["applications"][name] == None):
        return None
    token = dict["applications"][name]["token"]
    credentials = dict["applications"][name]["credentials"]
    
    if ((token == None) or (len(token) == 0)):
        token = genDigitToken (20)
    if ((credentials == None) or (len(credentials) == 0)):
        credentials = "Trustful"
    return {'name': name, 'token': token, 'credentials': credentials}

def getCtlYaml (name):
    if (dict["ctls"][name] == None):
        return None
    return {'name': name, 'owner': dict["ctls"][name]["owner"], 'schems': dict["ctls"][name]["schems"], 'fqn': dict["ctls"][name]["fqn"], 'body': dict["ctls"][name]["body"], 'metainfo_id': 0}

##############################################################################################################

def doRunIt():
    for name in dict["tenant"]:
        global Tenant, TenantAdmin, TenantDeveloper, TenantUser, Application

        Tenant = putTenant(name)
        TenantAdmin = putUser (getUserYaml (dict[name]["admin"], TENANT_ADMIN))

        for usr in dict[name]["developer"]:
            TenantDeveloper = putUser (getUserYaml (usr, TENANT_DEVELOPER))

        for usr in dict[name]["user"]:
            TenantUser = putUser (getUserYaml (usr, TENANT_USER))

        for app in dict[name]["application"]:
            Application = putApp (getAppYaml(app))
            EndPointGroup = putEndPointGroup (getAppYaml(app))
            for ctl in dict["applications"][app]["ctl"]:
                Ctl = putCtl (getCtlYaml(ctl))
#                print ("INSERT ctl")
#                print ("INSERT crl_metainfo")
#                print ("INSERT base_schems")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    doRunIt ()
    conn.close()
