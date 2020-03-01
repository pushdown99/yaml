# -*- coding: utf-8 -*-
import yaml
import io
import os

######################################################################################################
#
# CLUSTER CONFIGURATION: YAML
#
with open("kaa-config.yaml", 'r') as stream:
    try:
        dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

######################################################################################################
#
# KAA-NODE
#
for host in dict["hosts"]:
    if not os.path.isdir("./" + host):
      #print("create '" + host + "' environment.")
      os.mkdir("./" + host)

    f = open("./" + host + "/kaa-node.properties", 'w')

    d = "control_service_enabled=%s\n" % str(dict[host]["control_service_enabled"]).lower()
    f.write(d)
    d = "bootstrap_service_enabled=%s\n" % str(dict[host]["bootstrap_service_enabled"]).lower()
    f.write(d)
    d = "operations_service_enabled=%s\n" % str(dict[host]["operations_service_enabled"]).lower()
    f.write(d)
    d = "thrift_host=%s\n" % str(dict["misc"]["thrift_host"]).lower()
    f.write(d)
    d = "thrift_port=%s\n" % str(dict["misc"]["thrift_port"]).lower()
    f.write(d)
    d = "admin_port=%s\n" % str(dict["misc"]["admin_port"]).lower()
    f.write(d)
    d = "zk_enabled=%s\n" % str(dict[host]["zk_enabled"]).lower()
    f.write(d)

    v = ""
    for h in dict["hosts"]:
      if v != "":
        v += ","
      v = v + dict[h]["public_ip"] + ':2181'

    d = "zk_host_port_list=%s\n" % str(v).lower()
    f.write(d)

    d = "zk_wait_connection_time=%s\n" % str(dict["zookeeper"]["zk_wait_connection_time"]).lower()
    f.write(d)
    d = "zk_max_retry_time=%s\n" % str(dict["zookeeper"]["zk_max_retry_time"]).lower()
    f.write(d)
    d = "zk_sleep_time=%s\n" % str(dict["zookeeper"]["zk_sleep_time"]).lower()
    f.write(d)
    d = "zk_ignore_errors=%s\n" % str(dict["zookeeper"]["zk_ignore_errors"]).lower()
    f.write(d)
    d = "loadmgmt_min_diff=%s\n" % str(dict["misc"]["loadmgmt_min_diff"]).lower()
    f.write(d)
    d = "loadmgmt_max_init_redirect_probability=%s\n" % str(dict["misc"]["loadmgmt_max_init_redirect_probability"]).lower()
    f.write(d)
    d = "loadmgmt_max_session_redirect_probability=%s\n" % str(dict["misc"]["loadmgmt_max_session_redirect_probability"]).lower()
    f.write(d)
    d = "recalculation_period=%s\n" % str(dict["misc"]["recalculation_period"]).lower()
    f.write(d)
    d = "user_hash_partitions=%s\n" % str(dict["misc"]["user_hash_partitions"]).lower()
    f.write(d)
    d = "max_number_neighbor_connections=%s\n" % str(dict["misc"]["max_number_neighbor_connections"]).lower()
    f.write(d)
    d = "ops_server_history_ttl=%s\n" % str(dict["misc"]["ops_server_history_ttl"]).lower()
    f.write(d)
    d = "worker_thread_pool=%s\n" % str(dict["misc"]["worker_thread_pool"]).lower()
    f.write(d)
    d = "bootstrap_keys_private_key_location=%s\n" % str(dict["misc"]["bootstrap_keys_private_key_location"]).lower()
    f.write(d)
    d = "bootstrap_keys_public_key_location=%s\n" % str(dict["misc"]["bootstrap_keys_public_key_location"]).lower()
    f.write(d)
    d = "operations_keys_private_key_location=%s\n" % str(dict["misc"]["operations_keys_private_key_location"]).lower()
    f.write(d)
    d = "operations_keys_public_key_location=%s\n" % str(dict["misc"]["operations_keys_public_key_location"]).lower()
    f.write(d)
    d = "support_unencrypted_connection=%s\n" % str(dict["misc"]["support_unencrypted_connection"]).lower()
    f.write(d)
    d = "transport_bind_interface=0.0.0.0\n" 
    f.write(d)
    d = "transport_public_interface=0.0.0.0\n"
    f.write(d)
    d = "metrics_enabled=%s\n" % str(dict["misc"]["metrics_enabled"]).lower()
    f.write(d)
    d = "logs_root_dir=%s\n" % str(dict["misc"]["logs_root_dir"]).lower()
    f.write(d)
    d = "date_pattern=%s\n" % str(dict["misc"]["date_pattern"]).lower()
    f.write(d)
    d = "layout_pattern=%s\n" % str(dict["misc"]["layout_pattern"]).lower()
    f.write(d)
    d = "load_stats_update_frequency=%s\n" % str(dict["misc"]["load_stats_update_frequency"]).lower()
    f.write(d)
    d = "default_ttl=%s\n" % str(dict["misc"]["default_ttl"]).lower()
    f.write(d)
    d = "additional_plugins_scan_package=%s\n" % str(dict["misc"]["additional_plugins_scan_package"]).lower()
    f.write(d)
    f.close()

    ######################################################################################################
    #
    # SQL-DAO: MYSQL
    #
    f = open("./" + host + "/sql-dao.properties", 'w')
    d = "db_name=%s\n" % str(dict["mysql"]["db_name"]).lower()
    f.write(d)
    d = "dao_max_wait_time=%s\n" % str(dict["mysql"]["dao_max_wait_time"]).lower()
    f.write(d)
    d = "hibernate_dialect=%s\n" % str(dict["mysql"]["hibernate_dialect"]).lower()
    f.write(d)
    d = "hibernate_format_sql=%s\n" % str(dict["mysql"]["hibernate_format_sql"]).lower()
    f.write(d)
    d = "hibernate_show_sql=%s\n" % str(dict["mysql"]["hibernate_show_sql"]).lower()
    f.write(d)
    d = "hibernate_hbm2ddl_auto=%s\n" % str(dict["mysql"]["hibernate_hbm2ddl_auto"]).lower()
    f.write(d)
    d = "jdbc_driver_className=%s\n" % str(dict["mysql"]["jdbc_driver_className"]).lower()
    f.write(d)
    d = "jdbc_username=%s\n" % str(dict["mysql"]["jdbc_username"]).lower()
    f.write(d)
    d = "jdbc_password=%s\n" % str(dict["mysql"]["jdbc_password"]).lower()
    f.write(d)

    v = ""
    for h in dict["hosts"]:
      if str(dict[host]["mariadb_enabled"]).lower() == "true":
        if v != "":
          v += ","
        v += dict[h]["public_ip"]+":3306"
    d = "jdbc_host_port=%s\n" % v
    f.write(d)

    d = "sql_provider_name=%s\n" % str(dict["mysql"]["sql_provider_name"]).lower()
    f.write(d)
    f.close()

    ######################################################################################################
    #
    # ADMIN-DAO: MYSQL
    #
    f = open("./" + host + "/admin-dao.properties", 'w')
    d = "hibernate_dialect=%s\n" % str(dict["mysql"]["hibernate_dialect"]).lower()
    f.write(d)
    d = "hibernate_format_sql=%s\n" % str(dict["mysql"]["hibernate_format_sql"]).lower()
    f.write(d)
    d = "hibernate_show_sql=%s\n" % str(dict["mysql"]["hibernate_show_sql"]).lower()
    f.write(d)
    d = "hibernate_hbm2ddl_auto=%s\n" % str(dict["mysql"]["hibernate_hbm2ddl_auto"]).lower()
    f.write(d)
    d = "jdbc_driver_className=%s\n" % str(dict["mysql"]["jdbc_driver_className"]).lower()
    f.write(d)
    d = "jdbc_username=%s\n" % str(dict["mysql"]["jdbc_username"]).lower()
    f.write(d)
    d = "jdbc_password=%s\n" % str(dict["mysql"]["jdbc_password"]).lower()
    f.write(d)

    v = ""
    for h in dict["hosts"]:
      if str(dict[h]["mariadb_enabled"]).lower() == "true":
        if v != "":
          v += ","
        else:
          v = "jdbc:mysql:failover://"
        v += dict[h]["public_ip"]+":3306"
    d = "jdbc_url=%s/kaa\n" % v
    f.write(d)

    f.close()

    ######################################################################################################
    #
    # ADMIN-DAO: MYSQL
    #
    f = open("./" + host + "/galera.cnf", 'w')
    d = "[mysqld]\nbinlog_format=ROW\ndefault-storage-engine=innodb\ninnodb_autoinc_lock_mode=2\nbind-address=0.0.0.0\nwsrep_on=ON\nwsrep_provider=/usr/lib/galera/libgalera_smm.so\nwsrep_cluster_name=\"galera_cluster\"\n"
    f.write(d)

    v = ""
    for h in dict["hosts"]:
      if v != "":
        v += ","
      else:
        v ="gcomm://"
      v = v + dict[h]["public_ip"]
    d = "wsrep_cluster_address=\"%s\"\nwsrep_sst_method=rsync\n" % v
    f.write(d)
    d = "wsrep_node_address=\"%s\"\n" % str(dict[host]["public_ip"]).lower()
    f.write(d)
    d = "wsrep_node_name=\"%s\"\n" % str(host).lower()
    f.write(d)

    f.close()

    ######################################################################################################
    #
    # COMMON-DAO: MONGODB
    #
    f = open("./" + host + "/common-dao-mongodb.properties", 'w')

    v = ""
    for h in dict["hosts"]:
      if str(dict[host]["mongodb_enabled"]).lower() == "true":
        if v != "":
          v += ","
        v += dict[h]["public_ip"]+":27017"
    d = "servers=%s\n" % v
    f.write(d)

    d = "db_name=kaa\nwrite_concern=acknowledged\nconnections_per_host=100\nmax_wait_time=120000\nconnection_timeout=5000\nsocket_timeout=0\nsocket_keepalive=false\n"
    f.write(d)

    f.close()
