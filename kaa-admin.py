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

conn = pymysql.connect(host='10.146.0.33', user='sqladmin', password='admin', db='kaa', charset='utf8', autocommit=True)
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
User = {}
UserVerifier = {}
SdkToken = {}
Plugin = {}
Sdk = {}

Timestamp = int(time.time()*1000)

KAA_ADMIN        = 'KAA_ADMIN'
TENANT_ADMIN     = 'TENANT_ADMIN'
TENANT_DEVELOPER = 'TENANT_DEVELOPER'
TENANT_USER      = 'TENANT_USER'

PROFILE_SCHEMS        = 'profile_schems'
SERVER_PROFILE_SCHEMS = 'server_profile_schems'
NOTIFICATION_SCHEMS   = 'notification_schems'
CONFIGURATION_SCHEMS  = 'configuration_schems'
LOG_SCHEMS            = 'log_schems'

CLASS_CREDENTIALS_TRUSTFUL = 'org.kaaproject.kaa.server.verifiers.trustful.verifier.TrustfulUserVerifier'

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

def getMaxCtlMetainfoId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM ctl_metainfo")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxCtl ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM ctl")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxPlugin ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM plugin")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxBaseSchems ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM base_schems")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxAbstractStructureId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM abstract_structure")
    if (row['id'] == None):
        return int(0)
    return int(row['id'])

def getMaxSdkTokenId ():
    row=mysqlFetchOne ("SELECT max(id) as id FROM sdk_token")
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
    row = mysqlFetchOne ("SELECT * FROM admin_user WHERE username='" + str(username) + "'")
    return row

def getKaaUser (username):
    row = mysqlFetchOne ("SELECT * FROM kaa_user WHERE user_name='" + str(username) + "'")
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

def getUserVerifier (id):
    row = mysqlFetchOne ("SELECT * FROM user_verifier WHERE id=" + str(id))
    return row

def putUserVerifier (id):
    row = getUserVerifier (id)
    if(row == None):
        mysqlExecute ("INSERT INTO user_verifier VALUES (%s,%s)", (genDigitToken(20), int(id)))
        row = getUserVerifier (id)
    return row

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

def getBaseSchems ():
    rows = mysqlFetchAll ("SELECT * FROM base_schems WHERE application_id = " + str(Application['id']))
    return rows

def putBaseSchems ():
    rows = getBaseSchems ()
    if ((rows == None) or (len(rows)==0)): 
        fqn  = 'org.kaaproject.kaa.schema.system.EmptyData'
        mysqlExecute ("INSERT INTO ctl_metainfo VALUES (%s,%s,%s,%s)",(int(getMaxCtlMetainfoId()+1), fqn, int(Application['id']), int(Tenant['id'])))

        body = '{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","version": 1,"dependencies": [],"displayName":"Empty Data","description":"Auto generated","fields": []}'
        default = ''
        mysqlExecute ("INSERT INTO ctl VALUES (%s,%s,%s,%s,%s,%s,%s)",(int(getMaxCtl()+1), body, int(Timestamp), TenantAdmin['username'], default, int(1), int(getMaxCtlMetainfoId())))

        mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantAdmin['username'], '', 'Generated', int(0), int(Application['id']), int(getMaxCtl())))
        mysqlExecute ("INSERT INTO profile_schems VALUES (%s)",(int(getMaxBaseSchems())))

        mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantAdmin['username'], '', 'Generated', int(1), int(Application['id']), int(getMaxCtl())))
        base_schems = '{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}'
        override_schems = '{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}'
        protocol_schems = '{"type":"array","items":{"type":"record","name":"deltaT","namespace":"org.kaaproject.configuration","fields":[{"name":"delta","type":[{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}]}]}}'
        mysqlExecute ("INSERT INTO configuration_schems VALUES (%s,%s,%s,%s)",(base_schems, override_schems, protocol_schems, int(getMaxBaseSchems())))

        mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantAdmin['username'], '', 'Generated', int(0), int(Application['id']), int(getMaxCtl())))
        mysqlExecute ("INSERT INTO server_profile_schems VALUES (%s)",(int(getMaxBaseSchems())))

        mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantAdmin['username'], '', 'Generated', int(1), int(Application['id']), int(getMaxCtl())))
        mysqlExecute ("INSERT INTO notification_schems VALUES (%s,%s)",(int(0), int(getMaxBaseSchems())))

        mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantAdmin['username'], '', 'Generated', int(1), int(Application['id']), int(getMaxCtl())))
        mysqlExecute ("INSERT INTO log_schems VALUES (%s)",(int(getMaxBaseSchems())))


def putCtlSchems (c):
    row = getCtlMetainfo (c) 
    if row == None:
        return
    c['metainfo_id'] = row['id']
    row = getCtl (c)

    mysqlExecute ("INSERT INTO base_schems VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxBaseSchems()+1), int(Timestamp), TenantDeveloper['username'], '', c['name'], int(1), int(Application['id']),row['id']))

    if (c['schems'] == "profile"):
        mysqlExecute ("INSERT INTO profile_schems VALUES (%s)",(int(getMaxBaseSchems())))
    elif (c['schems'] == "server_profile"):
        mysqlExecute ("INSERT INTO server_profile_schems VALUES (%s)",(int(getMaxBaseSchems())))
    elif (c['schems'] == "notification"):
        mysqlExecute ("INSERT INTO notification_schems VALUES (%s,%s)",(int(0), int(getMaxBaseSchems())))
    elif (c['schems'] == "configuration"):
        mysqlExecute ("INSERT INTO configuration_schems VALUES (%s,%s,%s,%s)",(c['base_schems'], c['override_schems'], c['protocol_schems'], int(getMaxBaseSchems())))
    elif (c['schems'] == "log"):
        mysqlExecute ("INSERT INTO log_schems VALUES (%s)",(int(getMaxBaseSchems())))
    else:
        print ("Unkown Schems: " + c['schems'])


def getCtlMetainfo (c):
    row = mysqlFetchOne ("SELECT * FROM ctl_metainfo  WHERE fqn = '" + c['fqn'] + "' and application_id = " + str(Application['id']) + " and tenant_id=" + str(Tenant['id']))
    return row

def putCtlMetainfo (c):
    row = getCtlMetainfo (c)
    if (row == None):
        mysqlExecute ("INSERT INTO ctl_metainfo VALUES (%s,%s,%s,%s)",(int(getMaxCtlMetainfoId()+1), c['fqn'], Application['id'], Tenant['id']))
        row = getCtlMetainfo (c)
    return row

def getCtl (c):
    row = mysqlFetchOne ("SELECT * FROM ctl  WHERE metainfo_id = " + str(c['metainfo_id']))
    return row

def putCtl (c):
    row = getCtlMetainfo (c)
    if (row == None):
        row = putCtlMetainfo (c)
        c['metainfo_id'] = row['id']
        row = getCtl (c)
        if (row == None):
            mysqlExecute ("INSERT INTO ctl VALUES (%s,%s,%s,%s,%s,%s,%s)",(int(getMaxCtl()+1), c['body'], int(Timestamp), TenantAdmin['username'], c['default'], int(1), int(c['metainfo_id'])))
    else:
        c['metainfo_id'] = row['id']
    row = getCtl (c)
    putCtlSchems (c)
        
    return row

def getAbstractStructure (name, id):
    row = mysqlFetchOne ("SELECT * FROM abstract_structure  WHERE created_username = '" + name + "' and application_id = " + str(id))
    return row

def putAbstractStructure ():
    row = getAbstractStructure (TenantAdmin['username'], Application['id'])
    if (row == None):
        mysqlExecute ("INSERT INTO abstract_structure VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxAbstractStructureId()+1), int(Timestamp), TenantAdmin['username'], int(Timestamp), TenantAdmin['username'], int(0), '', 'Generated', int(0), int(Timestamp),  TenantAdmin['username'], int(1), 'ACTIVE', int(1), Application['id'], EndPointGroup['id']))

    row = getAbstractStructure (TenantDeveloper['username'], Application['id'])
    if (row == None):
        mysqlExecute ("INSERT INTO abstract_structure VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(int(getMaxAbstractStructureId()+1), int(Timestamp), TenantDeveloper['username'], int(Timestamp), TenantDeveloper['username'], int(0), '', 'Generated', int(0), int(Timestamp),  TenantDeveloper['username'], int(1), 'ACTIVE', int(1), Application['id'], EndPointGroup['id']))

def getPlugin (name):
    row = mysqlFetchOne ("SELECT * FROM plugin  WHERE plugin_class_name = '" + name + "' and application_id = " + str(Application['id']))
    return row

def putPlugin (name):
    row = getPlugin (name)
    if (row == None):
        if (name == CLASS_CREDENTIALS_TRUSTFUL):
            mysqlExecute ("INSERT INTO plugin VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(getMaxPlugin()+1), int(Timestamp), TenantDeveloper['username'], '', 'User Verifier', 'org.kaaproject.kaa.server.verifiers.trustful.verifier.TrustfulUserVerifier', 'Trustful verifier', '', int(Application['id'])))
            row = getPlugin (name)
    return row

def getSdkToken (id):
    row = mysqlFetchOne ("SELECT * FROM sdk_token  WHERE application_id = " + str(id))
    return row

def putSdkToken (s):
    row = getSdkToken (Application['id'])
    if (row == None):
        mysqlExecute ("INSERT INTO sdk_token VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (int(getMaxSdkTokenId()+1), int(2), int(Timestamp), TenantDeveloper['username'], UserVerifier['verifier_token'], int(0), int(2), str(s['name']), int(1), int(0), str(s['token']), int(Application['id'])))
        row = getSdkToken (Application['id'])
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
    return {'name': name, 'owner': dict["ctls"][name]["owner"], 'schems': dict["ctls"][name]["schems"], 'fqn': dict["ctls"][name]["fqn"], 'body': dict["ctls"][name]["body"], 'default': dict["ctls"][name]["default"], 'metainfo_id': 0, 'base_schems': dict["ctls"][name]["base_schems"],'override_schems': dict["ctls"][name]["override_schems"],'protocol_schems': dict["ctls"][name]["protocol_schems"]}

def getSdkYaml (name):
    if (dict["applications"][name] == None):
        return None
    if (dict["applications"][name]["sdk"] == None):
        return None

    token = dict["applications"][name]["sdk"]["token"];
    if ((token == None) or (token == '')):
        token = genSecureToken(10) + "-" + genSecureToken(16)

    return {'name': dict["applications"][name]["sdk"]["name"], 'token': token }

##############################################################################################################

def doRunIt():
    for name in dict["tenant"]:
        global Tenant, TenantAdmin, TenantDeveloper, TenantUser, Application, EndPointGroup, Plugin, UserVerifier

        Tenant = putTenant(name)
        TenantAdmin = putUser (getUserYaml (dict[name]["admin"], TENANT_ADMIN))

        for usr in dict[name]["developer"]:
            TenantDeveloper = putUser (getUserYaml (usr, TENANT_DEVELOPER))

        for usr in dict[name]["user"]:
            TenantUser = putUser (getUserYaml (usr, TENANT_USER))

        for app in dict[name]["application"]:
            Application = putApp (getAppYaml(app))
            if (Application['credentials_service'] == 'Trustful'):
                Plugin = putPlugin(CLASS_CREDENTIALS_TRUSTFUL)
                UserVerifier = putUserVerifier (Plugin['id'])
                putSdkToken(getSdkYaml (app))
            EndPointGroup = putEndPointGroup (getAppYaml(app))

            putAbstractStructure ()
            putBaseSchems ()

            for ctl in dict["applications"][app]["ctl"]:
                Ctl = putCtl (getCtlYaml(ctl))

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    doRunIt ()
    conn.close()
