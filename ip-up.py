#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import sys
import subprocess

# Change paths if neccesary

config_file = "/etc/ppp/ip-up.json"
log_file = "/tmp/ip-up-vpn.log"


def load_route():
    """
    Simply returns loaded json config
    """

    try:
        json_data = open(config_file)
        data = json.load(json_data)
    except Exception, e:
        logging.critical('Config file has errors, aborting – %s' % e)
        raise e
    else:
        logging.info('Config – %s' % config_file)
    json_data.close()
    return data


def set_route(vpn):
    """
    Add specified routes for current VPN
    """
    for item in vpn:
        logging.info(
            "/sbin/route add -net {0} -interface {1}".format(item, intf))
        run = subprocess.Popen(['/sbin/route', 'add', '-net', item,
                                '-interface', intf],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out, err = run.communicate()
        if err != "":
            logging.error("Something goes wrong, aborting – %s" % err)
            raise ValueError
        if out != "":
            logging.info("Shell output – %s" % out.strip('\n'))


def get_params():
    """
    When the ppp link comes up, this script is called with
    the following parameters:
        1 the interface name used by pppd
        2 the tty device name
        3 the tty device speed
        4 the local IP address for the interface
        5 the remote IP address
        6 the parameter specified by the 'ipparam' option to pppd
    """
    if len(sys.argv) < 6:
        logging.critical("Not enough command line arguments")
        print("This script should be called from the system request. ")
        print("")
        sys.exit(1)

    logging.info("The interface name used by pppd %s" % str(sys.argv[1]))
    logging.info("The local IP %s" % str(sys.argv[4]))
    logging.info("The remote IP address %s" % str(sys.argv[5]))

    return str(sys.argv[1]), str(sys.argv[4]), str(sys.argv[5])

if __name__ == '__main__':
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Script started')

    intf, local_ip, remote_ip = get_params()
    data = (load_route())

    if remote_ip not in data['VPN']:
        logging.info("Could not find routes for %s, nothing to do" % remote_ip)
    else:
        logging.info("Configuring IP %s" % remote_ip)
        set_route(data['VPN'][remote_ip])
        logging.info("Happy end")
