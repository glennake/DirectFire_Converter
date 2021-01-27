#!/usr/bin/env python

# Import modules

import logger
import sys

import re

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
common.common_regex()
interface_lookup = common.interface_lookup
ipv4_prefix_to_mask = common.ipv4_prefix_to_mask

# Initiate logging

logger = logging.getLogger(__name__)

# Parser

def parse(src_config, routing_info=""):

    logger.info(__name__ + ": parser module started")

    # Initialise data

    """
    May need to process XML to ET, JSON etc here
    """

    # Initialise variables

    data = {}

    data["system"] = {}

    data["interfaces"] = {}
    data["zones"] = {}

    data["routes"] = []
    data["routes6"] = []

    data["network_objects"] = {}
    data["network6_objects"] = {}
    data["network_groups"] = {}
    data["network6_groups"] = {}

    data["service_objects"] = {}
    data["service_groups"] = {}

    data["policies"] = []

    data["nat"] = []

    # Parser specific variables

    """
    Parser specific variables
    """

    # Define default service objects

    default_service_objects = {}

    default_service_objects["any"] = {}
    default_service_objects["any"]["description"] = ""
    default_service_objects["any"]["dst_port"] = ""
    default_service_objects["any"]["protocol"] = "0"
    default_service_objects["any"]["source_port"] = ""
    default_service_objects["any"]["type"] = "service"

    default_service_objects["junos-ftp"] = {}
    default_service_objects["junos-ftp"]["description"] = ""
    default_service_objects["junos-ftp"]["dst_port"] = "21"
    default_service_objects["junos-ftp"]["protocol"] = "6"
    default_service_objects["junos-ftp"]["source_port"] = ""
    default_service_objects["junos-ftp"]["type"] = ""

    default_service_objects["junos-ftp-data"] = {}
    default_service_objects["junos-ftp-data"]["description"] = ""
    default_service_objects["junos-ftp-data"]["dst_port"] = "20"
    default_service_objects["junos-ftp-data"]["protocol"] = "6"
    default_service_objects["junos-ftp-data"]["source_port"] = ""
    default_service_objects["junos-ftp-data"]["type"] = ""

    default_service_objects["junos-tftp"] = {}
    default_service_objects["junos-tftp"]["description"] = ""
    default_service_objects["junos-tftp"]["dst_port"] = "69"
    default_service_objects["junos-tftp"]["protocol"] = "17"
    default_service_objects["junos-tftp"]["source_port"] = ""
    default_service_objects["junos-tftp"]["type"] = ""

    default_service_objects["junos-twamp"] = {}
    default_service_objects["junos-twamp"]["description"] = ""
    default_service_objects["junos-twamp"]["dst_port"] = "862"
    default_service_objects["junos-twamp"]["protocol"] = "6"
    default_service_objects["junos-twamp"]["source_port"] = ""
    default_service_objects["junos-twamp"]["type"] = ""

    default_service_objects["junos-rtsp"] = {}
    default_service_objects["junos-rtsp"]["description"] = ""
    default_service_objects["junos-rtsp"]["dst_port"] = "554"
    default_service_objects["junos-rtsp"]["protocol"] = "6"
    default_service_objects["junos-rtsp"]["source_port"] = ""
    default_service_objects["junos-rtsp"]["type"] = ""

    default_service_objects["junos-netbios-session"] = {}
    default_service_objects["junos-netbios-session"]["description"] = ""
    default_service_objects["junos-netbios-session"]["dst_port"] = "139"
    default_service_objects["junos-netbios-session"]["protocol"] = "6"
    default_service_objects["junos-netbios-session"]["source_port"] = ""
    default_service_objects["junos-netbios-session"]["type"] = ""

    default_service_objects["junos-smb-session"] = {}
    default_service_objects["junos-smb-session"]["description"] = ""
    default_service_objects["junos-smb-session"]["dst_port"] = "445"
    default_service_objects["junos-smb-session"]["protocol"] = "6"
    default_service_objects["junos-smb-session"]["source_port"] = ""
    default_service_objects["junos-smb-session"]["type"] = ""

    default_service_objects["junos-ssh"] = {}
    default_service_objects["junos-ssh"]["description"] = ""
    default_service_objects["junos-ssh"]["dst_port"] = "22"
    default_service_objects["junos-ssh"]["protocol"] = "6"
    default_service_objects["junos-ssh"]["source_port"] = ""
    default_service_objects["junos-ssh"]["type"] = ""

    default_service_objects["junos-telnet"] = {}
    default_service_objects["junos-telnet"]["description"] = ""
    default_service_objects["junos-telnet"]["dst_port"] = "23"
    default_service_objects["junos-telnet"]["protocol"] = "6"
    default_service_objects["junos-telnet"]["source_port"] = ""
    default_service_objects["junos-telnet"]["type"] = ""

    default_service_objects["junos-smtp"] = {}
    default_service_objects["junos-smtp"]["description"] = ""
    default_service_objects["junos-smtp"]["dst_port"] = "25"
    default_service_objects["junos-smtp"]["protocol"] = "6"
    default_service_objects["junos-smtp"]["source_port"] = ""
    default_service_objects["junos-smtp"]["type"] = ""

    default_service_objects["junos-tacacs"] = {}
    default_service_objects["junos-tacacs"]["description"] = ""
    default_service_objects["junos-tacacs"]["dst_port"] = "49"
    default_service_objects["junos-tacacs"]["protocol"] = "6"
    default_service_objects["junos-tacacs"]["source_port"] = ""
    default_service_objects["junos-tacacs"]["type"] = ""

    default_service_objects["junos-tacacs-ds"] = {}
    default_service_objects["junos-tacacs-ds"]["description"] = ""
    default_service_objects["junos-tacacs-ds"]["dst_port"] = "65"
    default_service_objects["junos-tacacs-ds"]["protocol"] = "6"
    default_service_objects["junos-tacacs-ds"]["source_port"] = ""
    default_service_objects["junos-tacacs-ds"]["type"] = ""

    default_service_objects["junos-dhcp-client"] = {}
    default_service_objects["junos-dhcp-client"]["description"] = ""
    default_service_objects["junos-dhcp-client"]["dst_port"] = "68"
    default_service_objects["junos-dhcp-client"]["protocol"] = "17"
    default_service_objects["junos-dhcp-client"]["source_port"] = ""
    default_service_objects["junos-dhcp-client"]["type"] = ""

    default_service_objects["junos-dhcp-server"] = {}
    default_service_objects["junos-dhcp-server"]["description"] = ""
    default_service_objects["junos-dhcp-server"]["dst_port"] = "67"
    default_service_objects["junos-dhcp-server"]["protocol"] = "17"
    default_service_objects["junos-dhcp-server"]["source_port"] = ""
    default_service_objects["junos-dhcp-server"]["type"] = ""

    default_service_objects["junos-bootpc"] = {}
    default_service_objects["junos-bootpc"]["description"] = ""
    default_service_objects["junos-bootpc"]["dst_port"] = "68"
    default_service_objects["junos-bootpc"]["protocol"] = "17"
    default_service_objects["junos-bootpc"]["source_port"] = ""
    default_service_objects["junos-bootpc"]["type"] = ""

    default_service_objects["junos-bootps"] = {}
    default_service_objects["junos-bootps"]["description"] = ""
    default_service_objects["junos-bootps"]["dst_port"] = "67"
    default_service_objects["junos-bootps"]["protocol"] = "17"
    default_service_objects["junos-bootps"]["source_port"] = ""
    default_service_objects["junos-bootps"]["type"] = ""

    default_service_objects["junos-finger"] = {}
    default_service_objects["junos-finger"]["description"] = ""
    default_service_objects["junos-finger"]["dst_port"] = "79"
    default_service_objects["junos-finger"]["protocol"] = "6"
    default_service_objects["junos-finger"]["source_port"] = ""
    default_service_objects["junos-finger"]["type"] = ""

    default_service_objects["junos-http"] = {}
    default_service_objects["junos-http"]["description"] = ""
    default_service_objects["junos-http"]["dst_port"] = "80"
    default_service_objects["junos-http"]["protocol"] = "6"
    default_service_objects["junos-http"]["source_port"] = ""
    default_service_objects["junos-http"]["type"] = ""

    default_service_objects["junos-https"] = {}
    default_service_objects["junos-https"]["description"] = ""
    default_service_objects["junos-https"]["dst_port"] = "443"
    default_service_objects["junos-https"]["protocol"] = "6"
    default_service_objects["junos-https"]["source_port"] = ""
    default_service_objects["junos-https"]["type"] = ""

    default_service_objects["junos-pop3"] = {}
    default_service_objects["junos-pop3"]["dst_port"] = "110"
    default_service_objects["junos-pop3"]["protocol"] = "6"
    default_service_objects["junos-pop3"]["source_port"] = ""
    default_service_objects["junos-pop3"]["type"] = ""

    default_service_objects["junos-ident"] = {}
    default_service_objects["junos-ident"]["description"] = ""
    default_service_objects["junos-ident"]["dst_port"] = "113"
    default_service_objects["junos-ident"]["protocol"] = "6"
    default_service_objects["junos-ident"]["source_port"] = ""
    default_service_objects["junos-ident"]["type"] = ""

    default_service_objects["junos-nntp"] = {}
    default_service_objects["junos-nntp"]["description"] = ""
    default_service_objects["junos-nntp"]["dst_port"] = "119"
    default_service_objects["junos-nntp"]["protocol"] = "6"
    default_service_objects["junos-nntp"]["source_port"] = ""
    default_service_objects["junos-nntp"]["type"] = ""

    default_service_objects["junos-ntp"] = {}
    default_service_objects["junos-ntp"]["description"] = ""
    default_service_objects["junos-ntp"]["dst_port"] = "123"
    default_service_objects["junos-ntp"]["protocol"] = "17"
    default_service_objects["junos-ntp"]["source_port"] = ""
    default_service_objects["junos-ntp"]["type"] = ""

    default_service_objects["junos-imap"] = {}
    default_service_objects["junos-imap"]["description"] = ""
    default_service_objects["junos-imap"]["dst_port"] = "143"
    default_service_objects["junos-imap"]["protocol"] = "6"
    default_service_objects["junos-imap"]["source_port"] = ""
    default_service_objects["junos-imap"]["type"] = ""

    default_service_objects["junos-imaps"] = {}
    default_service_objects["junos-imaps"]["description"] = ""
    default_service_objects["junos-imaps"]["dst_port"] = "993"
    default_service_objects["junos-imaps"]["protocol"] = "6"
    default_service_objects["junos-imaps"]["source_port"] = ""
    default_service_objects["junos-imaps"]["type"] = ""

    default_service_objects["junos-bgp"] = {}
    default_service_objects["junos-bgp"]["description"] = ""
    default_service_objects["junos-bgp"]["dst_port"] = "179"
    default_service_objects["junos-bgp"]["protocol"] = "6"
    default_service_objects["junos-bgp"]["source_port"] = ""
    default_service_objects["junos-bgp"]["type"] = ""

    default_service_objects["junos-ldap"] = {}
    default_service_objects["junos-ldap"]["description"] = ""
    default_service_objects["junos-ldap"]["dst_port"] = "389"
    default_service_objects["junos-ldap"]["protocol"] = "6"
    default_service_objects["junos-ldap"]["source_port"] = ""
    default_service_objects["junos-ldap"]["type"] = ""

    default_service_objects["junos-snpp"] = {}
    default_service_objects["junos-snpp"]["description"] = ""
    default_service_objects["junos-snpp"]["dst_port"] = "444"
    default_service_objects["junos-snpp"]["protocol"] = "6"
    default_service_objects["junos-snpp"]["source_port"] = ""
    default_service_objects["junos-snpp"]["type"] = ""

    default_service_objects["junos-biff"] = {}
    default_service_objects["junos-biff"]["description"] = ""
    default_service_objects["junos-biff"]["dst_port"] = "512"
    default_service_objects["junos-biff"]["protocol"] = "17"
    default_service_objects["junos-biff"]["source_port"] = ""
    default_service_objects["junos-biff"]["type"] = ""

    default_service_objects["junos-who"] = {}
    default_service_objects["junos-who"]["description"] = ""
    default_service_objects["junos-who"]["dst_port"] = "513"
    default_service_objects["junos-who"]["protocol"] = "17"
    default_service_objects["junos-who"]["source_port"] = ""
    default_service_objects["junos-who"]["type"] = ""

    default_service_objects["junos-syslog"] = {}
    default_service_objects["junos-syslog"]["description"] = ""
    default_service_objects["junos-syslog"]["dst_port"] = "514"
    default_service_objects["junos-syslog"]["protocol"] = "17"
    default_service_objects["junos-syslog"]["source_port"] = ""
    default_service_objects["junos-syslog"]["type"] = ""

    default_service_objects["junos-printer"] = {}
    default_service_objects["junos-printer"]["description"] = ""
    default_service_objects["junos-printer"]["dst_port"] = "515"
    default_service_objects["junos-printer"]["protocol"] = "6"
    default_service_objects["junos-printer"]["source_port"] = ""
    default_service_objects["junos-printer"]["type"] = ""

    default_service_objects["junos-rip"] = {}
    default_service_objects["junos-rip"]["description"] = ""
    default_service_objects["junos-rip"]["dst_port"] = "520"
    default_service_objects["junos-rip"]["protocol"] = "17"
    default_service_objects["junos-rip"]["source_port"] = ""
    default_service_objects["junos-rip"]["type"] = ""

    default_service_objects["junos-radius"] = {}
    default_service_objects["junos-radius"]["description"] = ""
    default_service_objects["junos-radius"]["dst_port"] = "1812"
    default_service_objects["junos-radius"]["protocol"] = "17"
    default_service_objects["junos-radius"]["source_port"] = ""
    default_service_objects["junos-radius"]["type"] = ""

    default_service_objects["junos-radacct"] = {}
    default_service_objects["junos-radacct"]["dst_port"] = "1813"
    default_service_objects["junos-radacct"]["protocol"] = "17"
    default_service_objects["junos-radacct"]["source_port"] = ""
    default_service_objects["junos-radacct"]["type"] = ""

    default_service_objects["junos-nfsd-tcp"] = {}
    default_service_objects["junos-nfsd-tcp"]["description"] = ""
    default_service_objects["junos-nfsd-tcp"]["dst_port"] = "2049"
    default_service_objects["junos-nfsd-tcp"]["protocol"] = "6"
    default_service_objects["junos-nfsd-tcp"]["source_port"] = ""
    default_service_objects["junos-nfsd-tcp"]["type"] = ""

    default_service_objects["junos-nfsd-udp"] = {}
    default_service_objects["junos-nfsd-udp"]["description"] = ""
    default_service_objects["junos-nfsd-udp"]["dst_port"] = "2049"
    default_service_objects["junos-nfsd-udp"]["protocol"] = "17"
    default_service_objects["junos-nfsd-udp"]["source_port"] = ""
    default_service_objects["junos-nfsd-udp"]["type"] = ""

    default_service_objects["junos-cvspserver"] = {}
    default_service_objects["junos-cvspserver"]["description"] = ""
    default_service_objects["junos-cvspserver"]["dst_port"] = "2401"
    default_service_objects["junos-cvspserver"]["protocol"] = "6"
    default_service_objects["junos-cvspserver"]["source_port"] = ""
    default_service_objects["junos-cvspserver"]["type"] = ""

    default_service_objects["junos-ldp-tcp"] = {}
    default_service_objects["junos-ldp-tcp"]["description"] = ""
    default_service_objects["junos-ldp-tcp"]["dst_port"] = "646"
    default_service_objects["junos-ldp-tcp"]["protocol"] = "6"
    default_service_objects["junos-ldp-tcp"]["source_port"] = ""
    default_service_objects["junos-ldp-tcp"]["type"] = ""

    default_service_objects["junos-ldp-udp"] = {}
    default_service_objects["junos-ldp-udp"]["description"] = ""
    default_service_objects["junos-ldp-udp"]["dst_port"] = "646"
    default_service_objects["junos-ldp-udp"]["protocol"] = "17"
    default_service_objects["junos-ldp-udp"]["source_port"] = ""
    default_service_objects["junos-ldp-udp"]["type"] = ""

    default_service_objects["junos-xnm-ssl"] = {}
    default_service_objects["junos-xnm-ssl"]["description"] = ""
    default_service_objects["junos-xnm-ssl"]["dst_port"] = "3220"
    default_service_objects["junos-xnm-ssl"]["protocol"] = "6"
    default_service_objects["junos-xnm-ssl"]["source_port"] = ""
    default_service_objects["junos-xnm-ssl"]["type"] = ""

    default_service_objects["junos-xnm-clear-text"] = {}
    default_service_objects["junos-xnm-clear-text"]["description"] = ""
    default_service_objects["junos-xnm-clear-text"]["dst_port"] = "3221"
    default_service_objects["junos-xnm-clear-text"]["protocol"] = "6"
    default_service_objects["junos-xnm-clear-text"]["source_port"] = ""
    default_service_objects["junos-xnm-clear-text"]["type"] = ""

    default_service_objects["junos-ike"] = {}
    default_service_objects["junos-ike"]["description"] = ""
    default_service_objects["junos-ike"]["dst_port"] = "500"
    default_service_objects["junos-ike"]["protocol"] = "17"
    default_service_objects["junos-ike"]["source_port"] = ""
    default_service_objects["junos-ike"]["type"] = ""

    default_service_objects["any"] = {}
    default_service_objects["any"]["description"] = ""
    default_service_objects["any"]["protocol"] = "0"
    default_service_objects["any"]["source_port"] = ""
    default_service_objects["any"]["type"] = ""

    default_service_objects["junos-aol"] = {}
    default_service_objects["junos-aol"]["description"] = ""
    default_service_objects["junos-aol"]["dst_port"] = "5190-5193"
    default_service_objects["junos-aol"]["protocol"] = "6"
    default_service_objects["junos-aol"]["source_port"] = ""
    default_service_objects["junos-aol"]["type"] = ""

    default_service_objects["junos-chargen"] = {}
    default_service_objects["junos-chargen"]["description"] = ""
    default_service_objects["junos-chargen"]["dst_port"] = "19"
    default_service_objects["junos-chargen"]["protocol"] = "17"
    default_service_objects["junos-chargen"]["source_port"] = ""
    default_service_objects["junos-chargen"]["type"] = ""

    default_service_objects["junos-dhcp-relay"] = {}
    default_service_objects["junos-dhcp-relay"]["description"] = ""
    default_service_objects["junos-dhcp-relay"]["dst_port"] = "67"
    default_service_objects["junos-dhcp-relay"]["protocol"] = "17"
    default_service_objects["junos-dhcp-relay"]["source_port"] = ""
    default_service_objects["junos-dhcp-relay"]["type"] = ""

    default_service_objects["junos-discard"] = {}
    default_service_objects["junos-discard"]["description"] = ""
    default_service_objects["junos-discard"]["dst_port"] = "9"
    default_service_objects["junos-discard"]["protocol"] = "17"
    default_service_objects["junos-discard"]["source_port"] = ""
    default_service_objects["junos-discard"]["type"] = ""

    default_service_objects["junos-dns-udp"] = {}
    default_service_objects["junos-dns-udp"]["description"] = ""
    default_service_objects["junos-dns-udp"]["dst_port"] = "53"
    default_service_objects["junos-dns-udp"]["protocol"] = "17"
    default_service_objects["junos-dns-udp"]["source_port"] = ""
    default_service_objects["junos-dns-udp"]["type"] = ""

    default_service_objects["junos-dns-tcp"] = {}
    default_service_objects["junos-dns-tcp"]["description"] = ""
    default_service_objects["junos-dns-tcp"]["dst_port"] = "53"
    default_service_objects["junos-dns-tcp"]["protocol"] = "6"
    default_service_objects["junos-dns-tcp"]["source_port"] = ""
    default_service_objects["junos-dns-tcp"]["type"] = ""

    default_service_objects["junos-echo"] = {}
    default_service_objects["junos-echo"]["description"] = ""
    default_service_objects["junos-echo"]["dst_port"] = "7"
    default_service_objects["junos-echo"]["protocol"] = "17"
    default_service_objects["junos-echo"]["source_port"] = ""
    default_service_objects["junos-echo"]["type"] = ""

    default_service_objects["junos-gopher"] = {}
    default_service_objects["junos-gopher"]["description"] = ""
    default_service_objects["junos-gopher"]["dst_port"] = "70"
    default_service_objects["junos-gopher"]["protocol"] = "6"
    default_service_objects["junos-gopher"]["source_port"] = ""
    default_service_objects["junos-gopher"]["type"] = ""

    default_service_objects["junos-gtp"] = {}
    default_service_objects["junos-gtp"]["description"] = ""
    default_service_objects["junos-gtp"]["dst_port"] = "2123"
    default_service_objects["junos-gtp"]["protocol"] = "17"
    default_service_objects["junos-gtp"]["source_port"] = ""
    default_service_objects["junos-gtp"]["type"] = ""

    default_service_objects["junos-gprs-gtp-c"] = {}
    default_service_objects["junos-gprs-gtp-c"]["description"] = ""
    default_service_objects["junos-gprs-gtp-c"]["dst_port"] = "2123"
    default_service_objects["junos-gprs-gtp-c"]["protocol"] = "17"
    default_service_objects["junos-gprs-gtp-c"]["source_port"] = ""
    default_service_objects["junos-gprs-gtp-c"]["type"] = ""

    default_service_objects["junos-gprs-gtp-u"] = {}
    default_service_objects["junos-gprs-gtp-u"]["description"] = ""
    default_service_objects["junos-gprs-gtp-u"]["dst_port"] = "2152"
    default_service_objects["junos-gprs-gtp-u"]["protocol"] = "17"
    default_service_objects["junos-gprs-gtp-u"]["source_port"] = ""
    default_service_objects["junos-gprs-gtp-u"]["type"] = ""

    default_service_objects["junos-gprs-gtp-v0"] = {}
    default_service_objects["junos-gprs-gtp-v0"]["dst_port"] = "3386"
    default_service_objects["junos-gprs-gtp-v0"]["protocol"] = "17"
    default_service_objects["junos-gprs-gtp-v0"]["source_port"] = ""
    default_service_objects["junos-gprs-gtp-v0"]["type"] = ""

    default_service_objects["junos-gprs-sctp"] = {}
    default_service_objects["junos-gprs-sctp"]["description"] = ""
    default_service_objects["junos-gprs-sctp"]["dst_port"] = "0"
    default_service_objects["junos-gprs-sctp"]["protocol"] = "132"
    default_service_objects["junos-gprs-sctp"]["source_port"] = ""
    default_service_objects["junos-gprs-sctp"]["type"] = ""

    default_service_objects["junos-gnutella"] = {}
    default_service_objects["junos-gnutella"]["description"] = ""
    default_service_objects["junos-gnutella"]["dst_port"] = "6346-6347"
    default_service_objects["junos-gnutella"]["protocol"] = "17"
    default_service_objects["junos-gnutella"]["source_port"] = ""
    default_service_objects["junos-gnutella"]["type"] = ""

    default_service_objects["junos-gre"] = {}
    default_service_objects["junos-gre"]["description"] = ""
    default_service_objects["junos-gre"]["protocol"] = "47"
    default_service_objects["junos-gre"]["source_port"] = ""
    default_service_objects["junos-gre"]["type"] = ""

    default_service_objects["junos-icmp-all"] = {}
    default_service_objects["junos-icmp-all"]["description"] = ""
    default_service_objects["junos-icmp-all"]["protocol"] = "1"
    default_service_objects["junos-icmp-all"]["source_port"] = ""
    default_service_objects["junos-icmp-all"]["type"] = ""

    default_service_objects["junos-icmp-ping"] = {}
    default_service_objects["junos-icmp-ping"]["description"] = ""
    default_service_objects["junos-icmp-ping"]["icmp_type"] = "8"
    default_service_objects["junos-icmp-ping"]["protocol"] = "1"
    default_service_objects["junos-icmp-ping"]["source_port"] = ""
    default_service_objects["junos-icmp-ping"]["type"] = ""

    default_service_objects["junos-http-ext"] = {}
    default_service_objects["junos-http-ext"]["description"] = ""
    default_service_objects["junos-http-ext"]["dst_port"] = "7001"
    default_service_objects["junos-http-ext"]["protocol"] = "6"
    default_service_objects["junos-http-ext"]["source_port"] = ""
    default_service_objects["junos-http-ext"]["type"] = ""

    default_service_objects["junos-internet-locator-service"] = {}
    default_service_objects["junos-internet-locator-service"]["description"] = ""
    default_service_objects["junos-internet-locator-service"]["dst_port"] = "389"
    default_service_objects["junos-internet-locator-service"]["protocol"] = "6"
    default_service_objects["junos-internet-locator-service"]["source_port"] = ""
    default_service_objects["junos-internet-locator-service"]["type"] = ""

    default_service_objects["junos-ike-nat"] = {}
    default_service_objects["junos-ike-nat"]["description"] = ""
    default_service_objects["junos-ike-nat"]["dst_port"] = "4500"
    default_service_objects["junos-ike-nat"]["protocol"] = "17"
    default_service_objects["junos-ike-nat"]["source_port"] = ""
    default_service_objects["junos-ike-nat"]["type"] = ""

    default_service_objects["junos-irc"] = {}
    default_service_objects["junos-irc"]["description"] = ""
    default_service_objects["junos-irc"]["dst_port"] = "6660-6669"
    default_service_objects["junos-irc"]["protocol"] = "6"
    default_service_objects["junos-irc"]["source_port"] = ""
    default_service_objects["junos-irc"]["type"] = ""

    default_service_objects["junos-l2tp"] = {}
    default_service_objects["junos-l2tp"]["dst_port"] = "1701"
    default_service_objects["junos-l2tp"]["protocol"] = "17"
    default_service_objects["junos-l2tp"]["source_port"] = ""
    default_service_objects["junos-l2tp"]["type"] = ""

    default_service_objects["junos-lpr"] = {}
    default_service_objects["junos-lpr"]["description"] = ""
    default_service_objects["junos-lpr"]["dst_port"] = "515"
    default_service_objects["junos-lpr"]["protocol"] = "6"
    default_service_objects["junos-lpr"]["source_port"] = ""
    default_service_objects["junos-lpr"]["type"] = ""

    default_service_objects["junos-mail"] = {}
    default_service_objects["junos-mail"]["description"] = ""
    default_service_objects["junos-mail"]["dst_port"] = "25"
    default_service_objects["junos-mail"]["protocol"] = "6"
    default_service_objects["junos-mail"]["source_port"] = ""
    default_service_objects["junos-mail"]["type"] = ""

    default_service_objects["junos-mgcp-ua"] = {}
    default_service_objects["junos-mgcp-ua"]["description"] = ""
    default_service_objects["junos-mgcp-ua"]["dst_port"] = "2427"
    default_service_objects["junos-mgcp-ua"]["protocol"] = "17"
    default_service_objects["junos-mgcp-ua"]["source_port"] = ""
    default_service_objects["junos-mgcp-ua"]["type"] = ""

    default_service_objects["junos-mgcp-ca"] = {}
    default_service_objects["junos-mgcp-ca"]["description"] = ""
    default_service_objects["junos-mgcp-ca"]["dst_port"] = "2727"
    default_service_objects["junos-mgcp-ca"]["protocol"] = "17"
    default_service_objects["junos-mgcp-ca"]["source_port"] = ""
    default_service_objects["junos-mgcp-ca"]["type"] = ""

    default_service_objects["junos-msn"] = {}
    default_service_objects["junos-msn"]["description"] = ""
    default_service_objects["junos-msn"]["dst_port"] = "1863"
    default_service_objects["junos-msn"]["protocol"] = "6"
    default_service_objects["junos-msn"]["source_port"] = ""
    default_service_objects["junos-msn"]["type"] = ""

    default_service_objects["junos-ms-rpc-tcp"] = {}
    default_service_objects["junos-ms-rpc-tcp"]["description"] = ""
    default_service_objects["junos-ms-rpc-tcp"]["dst_port"] = "135"
    default_service_objects["junos-ms-rpc-tcp"]["protocol"] = "6"
    default_service_objects["junos-ms-rpc-tcp"]["source_port"] = ""
    default_service_objects["junos-ms-rpc-tcp"]["type"] = ""

    default_service_objects["junos-ms-rpc-udp"] = {}
    default_service_objects["junos-ms-rpc-udp"]["description"] = ""
    default_service_objects["junos-ms-rpc-udp"]["dst_port"] = "135"
    default_service_objects["junos-ms-rpc-udp"]["protocol"] = "17"
    default_service_objects["junos-ms-rpc-udp"]["source_port"] = ""
    default_service_objects["junos-ms-rpc-udp"]["type"] = ""

    default_service_objects["junos-ms-sql"] = {}
    default_service_objects["junos-ms-sql"]["description"] = ""
    default_service_objects["junos-ms-sql"]["dst_port"] = "1433"
    default_service_objects["junos-ms-sql"]["protocol"] = "6"
    default_service_objects["junos-ms-sql"]["source_port"] = ""
    default_service_objects["junos-ms-sql"]["type"] = ""

    default_service_objects["junos-nbname"] = {}
    default_service_objects["junos-nbname"]["description"] = ""
    default_service_objects["junos-nbname"]["dst_port"] = "137"
    default_service_objects["junos-nbname"]["protocol"] = "17"
    default_service_objects["junos-nbname"]["source_port"] = ""
    default_service_objects["junos-nbname"]["type"] = ""

    default_service_objects["junos-nbds"] = {}
    default_service_objects["junos-nbds"]["description"] = ""
    default_service_objects["junos-nbds"]["dst_port"] = "138"
    default_service_objects["junos-nbds"]["protocol"] = "17"
    default_service_objects["junos-nbds"]["source_port"] = ""
    default_service_objects["junos-nbds"]["type"] = ""

    default_service_objects["junos-nfs"] = {}
    default_service_objects["junos-nfs"]["description"] = ""
    default_service_objects["junos-nfs"]["dst_port"] = "111"
    default_service_objects["junos-nfs"]["protocol"] = "17"
    default_service_objects["junos-nfs"]["source_port"] = ""
    default_service_objects["junos-nfs"]["type"] = ""

    default_service_objects["junos-ns-global"] = {}
    default_service_objects["junos-ns-global"]["description"] = ""
    default_service_objects["junos-ns-global"]["dst_port"] = "15397"
    default_service_objects["junos-ns-global"]["protocol"] = "6"
    default_service_objects["junos-ns-global"]["source_port"] = ""
    default_service_objects["junos-ns-global"]["type"] = ""

    default_service_objects["junos-ns-global-pro"] = {}
    default_service_objects["junos-ns-global-pro"]["description"] = ""
    default_service_objects["junos-ns-global-pro"]["dst_port"] = "15397"
    default_service_objects["junos-ns-global-pro"]["protocol"] = "6"
    default_service_objects["junos-ns-global-pro"]["source_port"] = ""
    default_service_objects["junos-ns-global-pro"]["type"] = ""

    default_service_objects["junos-nsm"] = {}
    default_service_objects["junos-nsm"]["description"] = ""
    default_service_objects["junos-nsm"]["dst_port"] = "69"
    default_service_objects["junos-nsm"]["protocol"] = "17"
    default_service_objects["junos-nsm"]["source_port"] = ""
    default_service_objects["junos-nsm"]["type"] = ""

    default_service_objects["junos-ospf"] = {}
    default_service_objects["junos-ospf"]["description"] = ""
    default_service_objects["junos-ospf"]["dst_port"] = ""
    default_service_objects["junos-ospf"]["protocol"] = "89"
    default_service_objects["junos-ospf"]["source_port"] = ""
    default_service_objects["junos-ospf"]["type"] = ""

    default_service_objects["junos-pc-anywhere"] = {}
    default_service_objects["junos-pc-anywhere"]["description"] = ""
    default_service_objects["junos-pc-anywhere"]["dst_port"] = "5632"
    default_service_objects["junos-pc-anywhere"]["protocol"] = "17"
    default_service_objects["junos-pc-anywhere"]["source_port"] = ""
    default_service_objects["junos-pc-anywhere"]["type"] = ""

    default_service_objects["junos-ping"] = {}
    default_service_objects["junos-ping"]["description"] = ""
    default_service_objects["junos-ping"]["protocol"] = "1"
    default_service_objects["junos-ping"]["icmp_code"] = ""
    default_service_objects["junos-ping"]["icmp_type"] = ""
    default_service_objects["junos-ping"]["type"] = ""

    default_service_objects["junos-pingv6"] = {}
    default_service_objects["junos-pingv6"]["description"] = ""
    default_service_objects["junos-pingv6"]["protocol"] = "58"
    default_service_objects["junos-pingv6"]["icmp6_code"] = ""
    default_service_objects["junos-pingv6"]["icmp6_type"] = ""
    default_service_objects["junos-pingv6"]["type"] = ""

    default_service_objects["junos-icmp6-dst-unreach-addr"] = {}
    default_service_objects["junos-icmp6-dst-unreach-addr"]["description"] = ""
    default_service_objects["junos-icmp6-dst-unreach-addr"]["icmp6_code"] = "3"
    default_service_objects["junos-icmp6-dst-unreach-addr"]["icmp6_type"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-addr"]["protocol"] = "58"
    default_service_objects["junos-icmp6-dst-unreach-addr"]["type"] = ""

    default_service_objects["junos-icmp6-dst-unreach-admin"] = {}
    default_service_objects["junos-icmp6-dst-unreach-admin"]["description"] = ""
    default_service_objects["junos-icmp6-dst-unreach-admin"]["icmp6_code"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-admin"]["icmp6_type"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-admin"]["protocol"] = "58"
    default_service_objects["junos-icmp6-dst-unreach-admin"]["type"] = ""

    default_service_objects["junos-icmp6-dst-unreach-beyond"] = {}
    default_service_objects["junos-icmp6-dst-unreach-beyond"]["description"] = ""
    default_service_objects["junos-icmp6-dst-unreach-beyond"]["icmp6_code"] = "2"
    default_service_objects["junos-icmp6-dst-unreach-beyond"]["icmp6_type"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-beyond"]["protocol"] = "58"
    default_service_objects["junos-icmp6-dst-unreach-beyond"]["type"] = ""

    default_service_objects["junos-icmp6-dst-unreach-port"] = {}
    default_service_objects["junos-icmp6-dst-unreach-port"]["description"] = ""
    default_service_objects["junos-icmp6-dst-unreach-port"]["icmp6_code"] = "4"
    default_service_objects["junos-icmp6-dst-unreach-port"]["icmp6_type"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-port"]["protocol"] = "58"
    default_service_objects["junos-icmp6-dst-unreach-port"]["type"] = ""

    default_service_objects["junos-icmp6-dst-unreach-route"] = {}
    default_service_objects["junos-icmp6-dst-unreach-route"]["description"] = ""
    default_service_objects["junos-icmp6-dst-unreach-route"]["icmp6_code"] = "0"
    default_service_objects["junos-icmp6-dst-unreach-route"]["icmp6_type"] = "1"
    default_service_objects["junos-icmp6-dst-unreach-route"]["protocol"] = "58"
    default_service_objects["junos-icmp6-dst-unreach-route"]["type"] = ""

    default_service_objects["junos-icmp6-echo-reply"] = {}
    default_service_objects["junos-icmp6-echo-reply"]["description"] = ""
    default_service_objects["junos-icmp6-echo-reply"]["icmp6_code"] = ""
    default_service_objects["junos-icmp6-echo-reply"]["icmp6_type"] = "129"
    default_service_objects["junos-icmp6-echo-reply"]["protocol"] = "58"
    default_service_objects["junos-icmp6-echo-reply"]["type"] = ""

    default_service_objects["junos-icmp6-echo-request"] = {}
    default_service_objects["junos-icmp6-echo-request"]["description"] = ""
    default_service_objects["junos-icmp6-echo-request"]["icmp6_code"] = ""
    default_service_objects["junos-icmp6-echo-request"]["icmp6_type"] = "128"
    default_service_objects["junos-icmp6-echo-request"]["protocol"] = "58"
    default_service_objects["junos-icmp6-echo-request"]["type"] = ""

    default_service_objects["junos-icmp6-packet-too-big"] = {}
    default_service_objects["junos-icmp6-packet-too-big"]["description"] = ""
    default_service_objects["junos-icmp6-packet-too-big"]["icmp6_code"] = "0"
    default_service_objects["junos-icmp6-packet-too-big"]["icmp6_type"] = "2"
    default_service_objects["junos-icmp6-packet-too-big"]["protocol"] = "58"
    default_service_objects["junos-icmp6-packet-too-big"]["type"] = ""

    default_service_objects["junos-icmp6-param-prob-header"] = {}
    default_service_objects["junos-icmp6-param-prob-header"]["description"] = ""
    default_service_objects["junos-icmp6-param-prob-header"]["icmp6_code"] = "0"
    default_service_objects["junos-icmp6-param-prob-header"]["icmp6_type"] = "4"
    default_service_objects["junos-icmp6-param-prob-header"]["protocol"] = "58"
    default_service_objects["junos-icmp6-param-prob-header"]["type"] = ""

    default_service_objects["junos-icmp6-param-prob-nexthdr"] = {}
    default_service_objects["junos-icmp6-param-prob-nexthdr"]["description"] = ""
    default_service_objects["junos-icmp6-param-prob-nexthdr"]["icmp6_code"] = "1"
    default_service_objects["junos-icmp6-param-prob-nexthdr"]["icmp6_type"] = "4"
    default_service_objects["junos-icmp6-param-prob-nexthdr"]["protocol"] = "58"
    default_service_objects["junos-icmp6-param-prob-nexthdr"]["type"] = ""

    default_service_objects["junos-icmp6-param-prob-option"] = {}
    default_service_objects["junos-icmp6-param-prob-option"]["description"] = ""
    default_service_objects["junos-icmp6-param-prob-option"]["icmp6_code"] = "2"
    default_service_objects["junos-icmp6-param-prob-option"]["icmp6_type"] = "4"
    default_service_objects["junos-icmp6-param-prob-option"]["protocol"] = "58"
    default_service_objects["junos-icmp6-param-prob-option"]["type"] = ""

    default_service_objects["junos-icmp6-time-exceed-reassembly"] = {}
    default_service_objects["junos-icmp6-time-exceed-reassembly"]["description"] = ""
    default_service_objects["junos-icmp6-time-exceed-reassembly"]["icmp6_code"] = "1"
    default_service_objects["junos-icmp6-time-exceed-reassembly"]["icmp6_type"] = "3"
    default_service_objects["junos-icmp6-time-exceed-reassembly"]["protocol"] = "58"
    default_service_objects["junos-icmp6-time-exceed-reassembly"]["type"] = ""

    default_service_objects["junos-icmp6-time-exceed-transit"] = {}
    default_service_objects["junos-icmp6-time-exceed-transit"]["description"] = ""
    default_service_objects["junos-icmp6-time-exceed-transit"]["icmp6_code"] = "0"
    default_service_objects["junos-icmp6-time-exceed-transit"]["icmp6_type"] = "3"
    default_service_objects["junos-icmp6-time-exceed-transit"]["protocol"] = "58"
    default_service_objects["junos-icmp6-time-exceed-transit"]["type"] = ""

    default_service_objects["junos-icmp6-all"] = {}
    default_service_objects["junos-icmp6-all"]["description"] = ""
    default_service_objects["junos-icmp6-all"]["icmp6_code"] = ""
    default_service_objects["junos-icmp6-all"]["icmp6_type"] = ""
    default_service_objects["junos-icmp6-all"]["protocol"] = "58"
    default_service_objects["junos-icmp6-all"]["type"] = ""

    default_service_objects["junos-pptp"] = {}
    default_service_objects["junos-pptp"]["description"] = ""
    default_service_objects["junos-pptp"]["dst_port"] = "1723"
    default_service_objects["junos-pptp"]["protocol"] = "6"
    default_service_objects["junos-pptp"]["source_port"] = ""
    default_service_objects["junos-pptp"]["type"] = ""

    default_service_objects["junos-realaudio"] = {}
    default_service_objects["junos-realaudio"]["description"] = ""
    default_service_objects["junos-realaudio"]["dst_port"] = "554"
    default_service_objects["junos-realaudio"]["protocol"] = "6"
    default_service_objects["junos-realaudio"]["source_port"] = ""
    default_service_objects["junos-realaudio"]["type"] = ""

    default_service_objects["junos-sccp"] = {}
    default_service_objects["junos-sccp"]["description"] = ""
    default_service_objects["junos-sccp"]["dst_port"] = "2000"
    default_service_objects["junos-sccp"]["protocol"] = "6"
    default_service_objects["junos-sccp"]["source_port"] = ""
    default_service_objects["junos-sccp"]["type"] = ""

    default_service_objects["junos-sctp-any"] = {}
    default_service_objects["junos-sctp-any"]["description"] = ""
    default_service_objects["junos-sctp-any"]["dst_port"] = ""
    default_service_objects["junos-sctp-any"]["protocol"] = "132"
    default_service_objects["junos-sctp-any"]["source_port"] = ""
    default_service_objects["junos-sctp-any"]["type"] = ""

    default_service_objects["junos-rsh"] = {}
    default_service_objects["junos-rsh"]["description"] = ""
    default_service_objects["junos-rsh"]["dst_port"] = "514"
    default_service_objects["junos-rsh"]["protocol"] = "6"
    default_service_objects["junos-rsh"]["source_port"] = ""
    default_service_objects["junos-rsh"]["type"] = ""

    default_service_objects["junos-sql-monitor"] = {}
    default_service_objects["junos-sql-monitor"]["description"] = ""
    default_service_objects["junos-sql-monitor"]["dst_port"] = "1434"
    default_service_objects["junos-sql-monitor"]["protocol"] = "17"
    default_service_objects["junos-sql-monitor"]["source_port"] = ""
    default_service_objects["junos-sql-monitor"]["type"] = ""

    default_service_objects["junos-sqlnet-v1"] = {}
    default_service_objects["junos-sqlnet-v1"]["description"] = ""
    default_service_objects["junos-sqlnet-v1"]["dst_port"] = "1525"
    default_service_objects["junos-sqlnet-v1"]["protocol"] = "6"
    default_service_objects["junos-sqlnet-v1"]["source_port"] = ""
    default_service_objects["junos-sqlnet-v1"]["type"] = ""

    default_service_objects["junos-sqlnet-v2"] = {}
    default_service_objects["junos-sqlnet-v2"]["description"] = ""
    default_service_objects["junos-sqlnet-v2"]["dst_port"] = "1521"
    default_service_objects["junos-sqlnet-v2"]["protocol"] = "6"
    default_service_objects["junos-sqlnet-v2"]["source_port"] = ""
    default_service_objects["junos-sqlnet-v2"]["type"] = ""

    default_service_objects["junos-sun-rpc-tcp"] = {}
    default_service_objects["junos-sun-rpc-tcp"]["description"] = ""
    default_service_objects["junos-sun-rpc-tcp"]["dst_port"] = "111"
    default_service_objects["junos-sun-rpc-tcp"]["protocol"] = "6"
    default_service_objects["junos-sun-rpc-tcp"]["source_port"] = ""
    default_service_objects["junos-sun-rpc-tcp"]["type"] = ""

    default_service_objects["junos-sun-rpc-udp"] = {}
    default_service_objects["junos-sun-rpc-udp"]["description"] = ""
    default_service_objects["junos-sun-rpc-udp"]["dst_port"] = "111"
    default_service_objects["junos-sun-rpc-udp"]["protocol"] = "17"
    default_service_objects["junos-sun-rpc-udp"]["source_port"] = ""
    default_service_objects["junos-sun-rpc-udp"]["type"] = ""

    default_service_objects["junos-tcp-any"] = {}
    default_service_objects["junos-tcp-any"]["description"] = ""
    default_service_objects["junos-tcp-any"]["dst_port"] = ""
    default_service_objects["junos-tcp-any"]["protocol"] = "6"
    default_service_objects["junos-tcp-any"]["source_port"] = ""
    default_service_objects["junos-tcp-any"]["type"] = ""

    default_service_objects["junos-udp-any"] = {}
    default_service_objects["junos-udp-any"]["description"] = ""
    default_service_objects["junos-udp-any"]["source_port"] = ""
    default_service_objects["junos-udp-any"]["protocol"] = "17"
    default_service_objects["junos-udp-any"]["source_port"] = ""
    default_service_objects["junos-udp-any"]["type"] = ""

    default_service_objects["junos-uucp"] = {}
    default_service_objects["junos-uucp"]["description"] = ""
    default_service_objects["junos-uucp"]["dst_port"] = "540"
    default_service_objects["junos-uucp"]["protocol"] = "17"
    default_service_objects["junos-uucp"]["source_port"] = ""
    default_service_objects["junos-uucp"]["type"] = ""

    default_service_objects["junos-vdo-live"] = {}
    default_service_objects["junos-vdo-live"]["description"] = ""
    default_service_objects["junos-vdo-live"]["dst_port"] = "7000-7010"
    default_service_objects["junos-vdo-live"]["protocol"] = "17"
    default_service_objects["junos-vdo-live"]["source_port"] = ""
    default_service_objects["junos-vdo-live"]["type"] = ""

    default_service_objects["junos-wais"] = {}
    default_service_objects["junos-wais"]["description"] = ""
    default_service_objects["junos-wais"]["dst_port"] = "210"
    default_service_objects["junos-wais"]["protocol"] = "6"
    default_service_objects["junos-wais"]["source_port"] = ""
    default_service_objects["junos-wais"]["type"] = ""

    default_service_objects["junos-whois"] = {}
    default_service_objects["junos-whois"]["description"] = ""
    default_service_objects["junos-whois"]["dst_port"] = "43"
    default_service_objects["junos-whois"]["protocol"] = "6"
    default_service_objects["junos-whois"]["source_port"] = ""
    default_service_objects["junos-whois"]["type"] = ""

    default_service_objects["junos-winframe"] = {}
    default_service_objects["junos-winframe"]["description"] = ""
    default_service_objects["junos-winframe"]["dst_port"] = "1494"
    default_service_objects["junos-winframe"]["protocol"] = "6"
    default_service_objects["junos-winframe"]["source_port"] = ""
    default_service_objects["junos-winframe"]["type"] = ""

    default_service_objects["junos-x-windows"] = {}
    default_service_objects["junos-x-windows"]["description"] = ""
    default_service_objects["junos-x-windows"]["dst_port"] = "6000-6063"
    default_service_objects["junos-x-windows"]["protocol"] = "6"
    default_service_objects["junos-x-windows"]["source_port"] = ""
    default_service_objects["junos-x-windows"]["type"] = ""

    default_service_objects["junos-wxcontrol"] = {}
    default_service_objects["junos-wxcontrol"]["description"] = ""
    default_service_objects["junos-wxcontrol"]["dst_port"] = "3578"
    default_service_objects["junos-wxcontrol"]["protocol"] = "6"
    default_service_objects["junos-wxcontrol"]["source_port"] = ""
    default_service_objects["junos-wxcontrol"]["type"] = ""

    default_service_objects["junos-snmp-agentx"] = {}
    default_service_objects["junos-snmp-agentx"]["description"] = ""
    default_service_objects["junos-snmp-agentx"]["dst_port"] = "705"
    default_service_objects["junos-snmp-agentx"]["protocol"] = "6"
    default_service_objects["junos-snmp-agentx"]["source_port"] = ""
    default_service_objects["junos-snmp-agentx"]["type"] = ""

    default_service_objects["junos-persistent-nat"] = {}
    default_service_objects["junos-persistent-nat"]["description"] = ""
    default_service_objects["junos-persistent-nat"]["dst_port"] = "65535"
    default_service_objects["junos-persistent-nat"]["protocol"] = "255"
    default_service_objects["junos-persistent-nat"]["source_port"] = "65535"
    default_service_objects["junos-persistent-nat"]["type"] = ""

    default_service_objects["junos-r2cp"] = {}
    default_service_objects["junos-r2cp"]["description"] = ""
    default_service_objects["junos-r2cp"]["dst_port"] = "28672"
    default_service_objects["junos-r2cp"]["protocol"] = "17"
    default_service_objects["junos-r2cp"]["source_port"] = ""
    default_service_objects["junos-r2cp"]["type"] = ""

    default_service_objects["junos-rdp"] = {}
    default_service_objects["junos-rdp"]["description"] = ""
    default_service_objects["junos-rdp"]["dst_port"] = "3389"
    default_service_objects["junos-rdp"]["protocol"] = "6"
    default_service_objects["junos-rdp"]["source_port"] = ""
    default_service_objects["junos-rdp"]["type"] = ""

    default_service_objects["junos-sip-tcp5060"] = {}
    default_service_objects["junos-sip-tcp5060"]["description"] = ""
    default_service_objects["junos-sip-tcp5060"]["dst_port"] = "5060"
    default_service_objects["junos-sip-tcp5060"]["protocol"] = "6"
    default_service_objects["junos-sip-tcp5060"]["source_port"] = ""
    default_service_objects["junos-sip-tcp5060"]["type"] = ""

    default_service_objects["junos-sip-udp5060"] = {}
    default_service_objects["junos-sip-udp5060"]["description"] = ""
    default_service_objects["junos-sip-udp5060"]["dst_port"] = "5060"
    default_service_objects["junos-sip-udp5060"]["protocol"] = "17"
    default_service_objects["junos-sip-udp5060"]["source_port"] = ""
    default_service_objects["junos-sip-udp5060"]["type"] = ""

    default_service_objects["junos-smb-tcp139"] = {}
    default_service_objects["junos-smb-tcp139"]["description"] = ""
    default_service_objects["junos-smb-tcp139"]["dst_port"] = "139"
    default_service_objects["junos-smb-tcp139"]["protocol"] = "6"
    default_service_objects["junos-smb-tcp139"]["source_port"] = ""
    default_service_objects["junos-smb-tcp139"]["type"] = ""

    default_service_objects["junos-smb-tcp445"] = {}
    default_service_objects["junos-smb-tcp445"]["description"] = ""
    default_service_objects["junos-smb-tcp445"]["dst_port"] = "445"
    default_service_objects["junos-smb-tcp445"]["protocol"] = "6"
    default_service_objects["junos-smb-tcp445"]["source_port"] = ""
    default_service_objects["junos-smb-tcp445"]["type"] = ""

    default_service_objects["junos-talk-tcp517"] = {}
    default_service_objects["junos-talk-tcp517"]["description"] = ""
    default_service_objects["junos-talk-tcp517"]["dst_port"] = "517"
    default_service_objects["junos-talk-tcp517"]["protocol"] = "6"
    default_service_objects["junos-talk-tcp517"]["source_port"] = ""
    default_service_objects["junos-talk-tcp517"]["type"] = ""

    default_service_objects["junos-talk-udp517"] = {}
    default_service_objects["junos-talk-udp517"]["description"] = ""
    default_service_objects["junos-talk-udp517"]["dst_port"] = "517"
    default_service_objects["junos-talk-udp517"]["protocol"] = "17"
    default_service_objects["junos-talk-udp517"]["source_port"] = ""
    default_service_objects["junos-talk-udp517"]["type"] = ""

    default_service_objects["junos-ntalk-tcp518"] = {}
    default_service_objects["junos-ntalk-tcp518"]["description"] = ""
    default_service_objects["junos-ntalk-tcp518"]["dst_port"] = "518"
    default_service_objects["junos-ntalk-tcp518"]["protocol"] = "6"
    default_service_objects["junos-ntalk-tcp518"]["source_port"] = ""
    default_service_objects["junos-ntalk-tcp518"]["type"] = ""

    default_service_objects["junos-ntalk-udp518"] = {}
    default_service_objects["junos-ntalk-udp518"]["description"] = ""
    default_service_objects["junos-ntalk-udp518"]["dst_port"] = "518"
    default_service_objects["junos-ntalk-udp518"]["protocol"] = "17"
    default_service_objects["junos-ntalk-udp518"]["source_port"] = ""
    default_service_objects["junos-ntalk-udp518"]["type"] = ""

    default_service_objects["junos-vnc-tcp5800"] = {}
    default_service_objects["junos-vnc-tcp5800"]["description"] = ""
    default_service_objects["junos-vnc-tcp5800"]["dst_port"] = "5800"
    default_service_objects["junos-vnc-tcp5800"]["protocol"] = "6"
    default_service_objects["junos-vnc-tcp5800"]["source_port"] = ""
    default_service_objects["junos-vnc-tcp5800"]["type"] = ""

    default_service_objects["junos-vnc-tcp5900"] = {}
    default_service_objects["junos-vnc-tcp5900"]["description"] = ""
    default_service_objects["junos-vnc-tcp5900"]["dst_port"] = "5900"
    default_service_objects["junos-vnc-tcp5900"]["protocol"] = "6"
    default_service_objects["junos-vnc-tcp5900"]["source_port"] = ""
    default_service_objects["junos-vnc-tcp5900"]["type"] = ""

    default_service_objects["junos-ymsg-tcp5000-5010"] = {}
    default_service_objects["junos-ymsg-tcp5000-5010"]["description"] = ""
    default_service_objects["junos-ymsg-tcp5000-5010"]["dst_port"] = "5000-5010"
    default_service_objects["junos-ymsg-tcp5000-5010"]["protocol"] = "6"
    default_service_objects["junos-ymsg-tcp5000-5010"]["source_port"] = ""
    default_service_objects["junos-ymsg-tcp5000-5010"]["type"] = ""

    default_service_objects["junos-ymsg-tcp5050"] = {}
    default_service_objects["junos-ymsg-tcp5050"]["description"] = ""
    default_service_objects["junos-ymsg-tcp5050"]["dst_port"] = "5050"
    default_service_objects["junos-ymsg-tcp5050"]["protocol"] = "6"
    default_service_objects["junos-ymsg-tcp5050"]["source_port"] = ""
    default_service_objects["junos-ymsg-tcp5050"]["type"] = ""

    default_service_objects["junos-ymsg-udp5000-5010"] = {}
    default_service_objects["junos-ymsg-udp5000-5010"]["description"] = ""
    default_service_objects["junos-ymsg-udp5000-5010"]["dst_port"] = "5000-5010"
    default_service_objects["junos-ymsg-udp5000-5010"]["protocol"] = "17"
    default_service_objects["junos-ymsg-udp5000-5010"]["source_port"] = ""
    default_service_objects["junos-ymsg-udp5000-5010"]["type"] = ""

    default_service_objects["junos-ymsg-udp5050"] = {}
    default_service_objects["junos-ymsg-udp5050"]["description"] = ""
    default_service_objects["junos-ymsg-udp5050"]["dst_port"] = "5050"
    default_service_objects["junos-ymsg-udp5050"]["protocol"] = "17"
    default_service_objects["junos-ymsg-udp5050"]["source_port"] = ""
    default_service_objects["junos-ymsg-udp5050"]["type"] = ""

    default_service_objects["junos-stun-tcp3478-3479"] = {}
    default_service_objects["junos-stun-tcp3478-3479"]["description"] = ""
    default_service_objects["junos-stun-tcp3478-3479"]["dst_port"] = "3478-3479"
    default_service_objects["junos-stun-tcp3478-3479"]["protocol"] = "6"
    default_service_objects["junos-stun-tcp3478-3479"]["source_port"] = ""
    default_service_objects["junos-stun-tcp3478-3479"]["type"] = ""

    default_service_objects["junos-stun-udp3478-3479"] = {}
    default_service_objects["junos-stun-udp3478-3479"]["description"] = ""
    default_service_objects["junos-stun-udp3478-3479"]["dst_port"] = "3478-3479"
    default_service_objects["junos-stun-udp3478-3479"]["protocol"] = "17"
    default_service_objects["junos-stun-udp3478-3479"]["source_port"] = ""
    default_service_objects["junos-stun-udp3478-3479"]["type"] = ""

    default_service_objects["junos-smtps-tcp465"] = {}
    default_service_objects["junos-smtps-tcp465"]["description"] = ""
    default_service_objects["junos-smtps-tcp465"]["dst_port"] = "465"
    default_service_objects["junos-smtps-tcp465"]["protocol"] = "6"
    default_service_objects["junos-smtps-tcp465"]["source_port"] = ""
    default_service_objects["junos-smtps-tcp465"]["type"] = ""

    default_service_objects["junos-smtps-tcp587"] = {}
    default_service_objects["junos-smtps-tcp587"]["description"] = ""
    default_service_objects["junos-smtps-tcp587"]["dst_port"] = "587"
    default_service_objects["junos-smtps-tcp587"]["protocol"] = "6"
    default_service_objects["junos-smtps-tcp587"]["source_port"] = ""
    default_service_objects["junos-smtps-tcp587"]["type"] = ""

    default_service_objects["junos-h323-tcp389"] = {}
    default_service_objects["junos-h323-tcp389"]["description"] = ""
    default_service_objects["junos-h323-tcp389"]["dst_port"] = "389"
    default_service_objects["junos-h323-tcp389"]["protocol"] = "6"
    default_service_objects["junos-h323-tcp389"]["source_port"] = ""
    default_service_objects["junos-h323-tcp389"]["type"] = ""

    default_service_objects["junos-h323-tcp522"] = {}
    default_service_objects["junos-h323-tcp522"]["description"] = ""
    default_service_objects["junos-h323-tcp522"]["dst_port"] = "522"
    default_service_objects["junos-h323-tcp522"]["protocol"] = "6"
    default_service_objects["junos-h323-tcp522"]["source_port"] = ""
    default_service_objects["junos-h323-tcp522"]["type"] = ""

    default_service_objects["junos-h323-tcp1503"] = {}
    default_service_objects["junos-h323-tcp1503"]["description"] = ""
    default_service_objects["junos-h323-tcp1503"]["dst_port"] = "1503"
    default_service_objects["junos-h323-tcp1503"]["protocol"] = "6"
    default_service_objects["junos-h323-tcp1503"]["source_port"] = ""
    default_service_objects["junos-h323-tcp1503"]["type"] = ""

    default_service_objects["junos-h323-tcp1720"] = {}
    default_service_objects["junos-h323-tcp1720"]["description"] = ""
    default_service_objects["junos-h323-tcp1720"]["dst_port"] = "1720"
    default_service_objects["junos-h323-tcp1720"]["protocol"] = "6"
    default_service_objects["junos-h323-tcp1720"]["source_port"] = ""
    default_service_objects["junos-h323-tcp1720"]["type"] = ""

    default_service_objects["junos-h323-tcp1731"] = {}
    default_service_objects["junos-h323-tcp1731"]["description"] = ""
    default_service_objects["junos-h323-tcp1731"]["dst_port"] = "1731"
    default_service_objects["junos-h323-tcp1731"]["protocol"] = "6"
    default_service_objects["junos-h323-tcp1731"]["source_port"] = ""
    default_service_objects["junos-h323-tcp1731"]["type"] = ""

    default_service_objects["junos-h323-udp1719"] = {}
    default_service_objects["junos-h323-udp1719"]["description"] = ""
    default_service_objects["junos-h323-udp1719"]["dst_port"] = "1719"
    default_service_objects["junos-h323-udp1719"]["protocol"] = "17"
    default_service_objects["junos-h323-udp1719"]["source_port"] = ""
    default_service_objects["junos-h323-udp1719"]["type"] = ""

    ## default_service_objects["junos-"] = {}
    ## default_service_objects["junos-"]["description"] = ""
    ## default_service_objects["junos-"]["dst_port"] = ""
    ## default_service_objects["junos-"]["protocol"] = ""
    ## default_service_objects["junos-"]["source_port"] = ""
    ## default_service_objects["junos-"]['type'] = 'service'

    # Define default service groups

    default_service_groups = {}

    default_service_groups["junos-sip"] = {}
    default_service_groups["junos-sip"]["description"] = ""
    default_service_groups["junos-sip"]["members"] = [
        "junos-sip-tcp5060",
        "junos-sip-tcp5060",
    ]
    default_service_groups["junos-sip"]["type"] = "group"

    default_service_groups["junos-smb"] = {}
    default_service_groups["junos-smb"]["description"] = ""
    default_service_groups["junos-smb"]["members"] = [
        "junos-smb-tcp139",
        "junos-smb-tcp445",
    ]
    default_service_groups["junos-smb"]["type"] = "group"

    default_service_groups["junos-talk"] = {}
    default_service_groups["junos-talk"]["description"] = ""
    default_service_groups["junos-talk"]["members"] = [
        "junos-talk-tcp517",
        "junos-talk-udp517",
    ]
    default_service_groups["junos-talk"]["type"] = "group"

    default_service_groups["junos-ntalk"] = {}
    default_service_groups["junos-ntalk"]["description"] = ""
    default_service_groups["junos-ntalk"]["members"] = [
        "junos-ntalk-tcp518",
        "junos-ntalk-udp518",
    ]
    default_service_groups["junos-ntalk"]["type"] = "group"

    default_service_groups["junos-vnc"] = {}
    default_service_groups["junos-vnc"]["description"] = ""
    default_service_groups["junos-vnc"]["members"] = [
        "junos-vnc-tcp5800",
        "junos-vnc-tcp5900",
    ]
    default_service_groups["junos-vnc"]["type"] = "group"

    default_service_groups["junos-ymsg"] = {}
    default_service_groups["junos-ymsg"]["description"] = ""
    default_service_groups["junos-ymsg"]["members"] = [
        "junos-ymsg-tcp5000-5010",
        "junos-ymsg-tcp5050",
        "junos-ymsg-udp5000-5010",
        "junos-ymsg-udp5050",
    ]
    default_service_groups["junos-ymsg"]["type"] = "group"

    default_service_groups["junos-stun"] = {}
    default_service_groups["junos-stun"]["description"] = ""
    default_service_groups["junos-stun"]["members"] = [
        "junos-stun-tcp3478-3479",
        "junos-stun-udp3478-3479",
    ]
    default_service_groups["junos-stun"]["type"] = "group"

    default_service_groups["junos-smtps"] = {}
    default_service_groups["junos-smtps"]["description"] = ""
    default_service_groups["junos-smtps"]["members"] = [
        "junos-smtps-tcp465",
        "junos-smtps-tcp587",
    ]
    default_service_groups["junos-smtps"]["type"] = "group"

    default_service_groups["junos-h323"] = {}
    default_service_groups["junos-h323"]["description"] = ""
    default_service_groups["junos-h323"]["members"] = [
        "junos-h323-tcp389",
        "junos-h323-tcp522",
        "junos-h323-tcp1503",
        "junos-h323-tcp1720",
        "junos-h323-tcp1731",
        "junos-h323-udp1719",
    ]
    default_service_groups["junos-h323"]["type"] = "group"

    default_service_groups["junos-routing-inbound"] = {}
    default_service_groups["junos-routing-inbound"]["description"] = ""
    default_service_groups["junos-routing-inbound"]["members"] = [
        "junos-bgp",
        "junos-rip",
        "junos-ldp-tcp",
        "junos-ldp-udp",
    ]
    default_service_groups["junos-routing-inbound"]["type"] = "group"

    default_service_groups["junos-cifs"] = {}
    default_service_groups["junos-cifs"]["description"] = ""
    default_service_groups["junos-cifs"]["members"] = [
        "junos-netbios-session",
        "junos-smb-session",
    ]
    default_service_groups["junos-cifs"]["type"] = "group"

    default_service_groups["junos-gprs-gtp"] = {}
    default_service_groups["junos-gprs-gtp"]["description"] = ""
    default_service_groups["junos-gprs-gtp"]["members"] = [
        "junos-gprs-gtp-c",
        "junos-gprs-gtp-u",
        "junos-gprs-gtp-v0",
    ]
    default_service_groups["junos-gprs-gtp"]["type"] = "group"

    default_service_groups["junos-mgcp"] = {}
    default_service_groups["junos-mgcp"]["description"] = ""
    default_service_groups["junos-mgcp"]["members"] = ["junos-mgcp-ua", "junos-mgcp-ca"]
    default_service_groups["junos-mgcp"]["type"] = "group"

    default_service_groups["junos-ms-rpc"] = {}
    default_service_groups["junos-ms-rpc"]["description"] = ""
    default_service_groups["junos-ms-rpc"]["members"] = [
        "junos-ms-rpc-tcp",
        "junos-ms-rpc-udp",
    ]
    default_service_groups["junos-ms-rpc"]["type"] = "group"

    default_service_groups["junos-ms-rpc-any"] = {}
    default_service_groups["junos-ms-rpc-any"]["description"] = ""
    default_service_groups["junos-ms-rpc-any"]["members"] = [
        "junos-ms-rpc-tcp",
        "junos-ms-rpc-udp",
    ]
    default_service_groups["junos-ms-rpc-any"]["type"] = "group"

    default_service_groups["junos-sun-rpc"] = {}
    default_service_groups["junos-sun-rpc"]["description"] = ""
    default_service_groups["junos-sun-rpc"]["members"] = [
        "junos-sun-rpc-tcp",
        "junos-sun-rpc-udp",
    ]
    default_service_groups["junos-sun-rpc"]["type"] = "group"

    default_service_groups["junos-sun-rpc-any"] = {}
    default_service_groups["junos-sun-rpc-any"]["description"] = ""
    default_service_groups["junos-sun-rpc-any"]["members"] = [
        "junos-sun-rpc-tcp",
        "junos-sun-rpc-udp",
    ]
    default_service_groups["junos-sun-rpc-any"]["type"] = "group"

    ## default_service_groups[""] = {}
    ## default_service_groups[""]["description"] = ""
    ## default_service_groups[""]["members"] = []
    ## default_service_groups[""]["type"] = "group"

    # Parse system

    logger.info(__name__ + ": parse system")

    re_match = re.search("set system host-name (.*?)\n", src_config)

    if re_match:
        data["system"]["hostname"] = re_match.group(1)

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces - not yet supported")

    ## physical interfaces and sub interfaces

    for re_match in re.finditer(
        "set interfaces ((?:pp|reth|ae|fe|ge|xe|xle|et)(?:-[0-9]{1,2}/[0-9]{1,2}/)?[0-9]{1,2}) unit ([0-9]{1,4}) family inet address ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ")\n",
        src_config,
    ):

        interface_phys_name = re_match.group(1)

        if interface_phys_name not in data["interfaces"]:
            data["interfaces"][interface_phys_name] = {}
            data["interfaces"][interface_phys_name]["enabled"] = ""
            data["interfaces"][interface_phys_name]["description"] = ""
            data["interfaces"][interface_phys_name]["ipv4_config"] = []
            data["interfaces"][interface_phys_name]["ipv6_config"] = []
            data["interfaces"][interface_phys_name]["physical_interfaces"] = []
            data["interfaces"][interface_phys_name]["type"] = "interface"
            data["interfaces"][interface_phys_name]["vlan_id"] = ""
            data["interfaces"][interface_phys_name]["vlan_name"] = ""

        interface_name = re_match.group(1) + "." + re_match.group(2)

        if interface_name in data["interfaces"]:

            interface_ip_member = {}
            interface_ip_member["ip_address"] = re_match.group(3)
            interface_ip_member["mask"] = ipv4_prefix_to_mask(re_match.group(4))
            interface_ip_member["type"] = "secondary"

            data["interfaces"][interface_name]["ipv4_config"].append(
                interface_ip_member
            )

        else:

            data["interfaces"][interface_name] = {}

            data["interfaces"][interface_name]["enabled"] = ""
            data["interfaces"][interface_name]["description"] = ""

            data["interfaces"][interface_name]["ipv4_config"] = []

            interface_ip_member = {}
            interface_ip_member["ip_address"] = re_match.group(3)
            interface_ip_member["mask"] = ipv4_prefix_to_mask(re_match.group(4))
            interface_ip_member["type"] = "primary"

            data["interfaces"][interface_name]["ipv4_config"].append(
                interface_ip_member
            )

            data["interfaces"][interface_name]["physical_interfaces"] = []
            data["interfaces"][interface_name]["physical_interfaces"].append(
                re_match.group(1)
            )

            data["interfaces"][interface_name]["type"] = "subinterface"
            data["interfaces"][interface_name]["vlan_id"] = ""
            data["interfaces"][interface_name]["vlan_name"] = ""

    ## find sub interface vlan tag

    for interface in data["interfaces"].keys():

        if "." in interface:
            interface_name = interface.replace(".", " unit ")
        else:
            interface_name = interface

        re_match = re.search(
            "set interfaces " + interface_name + " vlan-id ([0-9]{1,4})\n", src_config
        )

        if re_match:
            data["interfaces"][interface]["vlan_id"] = re_match.group(1)

        else:
            data["interfaces"][interface]["vlan_id"] = "0"

    ## vlan interfaces

    for re_match in re.finditer(
        "set interfaces vlan unit ([0-9]{1,4}) family inet address ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ")\n",
        src_config,
    ):

        interface_name = "vlan." + re_match.group(1)

        if interface_name in data["interfaces"]:

            interface_ip_member = {}
            interface_ip_member["ip_address"] = re_match.group(2)
            interface_ip_member["mask"] = ipv4_prefix_to_mask(re_match.group(3))
            interface_ip_member["type"] = "secondary"

            data["interfaces"][interface_name]["ipv4_config"].append(
                interface_ip_member
            )

        else:

            data["interfaces"][interface_name] = {}

            data["interfaces"][interface_name]["enabled"] = ""
            data["interfaces"][interface_name]["description"] = ""

            data["interfaces"][interface_name]["ipv4_config"] = []

            interface_ip_member = {}
            interface_ip_member["ip_address"] = re_match.group(2)
            interface_ip_member["mask"] = ipv4_prefix_to_mask(re_match.group(3))
            interface_ip_member["type"] = "primary"

            data["interfaces"][interface_name]["ipv4_config"].append(
                interface_ip_member
            )

            data["interfaces"][interface_name]["physical_interfaces"] = []

            data["interfaces"][interface_name]["type"] = "switch"
            data["interfaces"][interface_name]["vlan_id"] = ""
            data["interfaces"][interface_name]["vlan_name"] = ""

    ## find vlan interface vlan tag

    for re_match in re.finditer(
        "set vlans (.*?) l3-interface vlan.([0-9]{1,4})", src_config
    ):

        vlan_name = re_match.group(1)
        interface_name = "vlan." + re_match.group(2)

        if interface_name in data["interfaces"]:

            re_match = re.search(
                "set vlans " + vlan_name + " vlan-id ([0-9]{1,4})", src_config
            )

            data["interfaces"][interface_name]["vlan_id"] = re_match.group(1)
            data["interfaces"][interface_name]["vlan_name"] = vlan_name

    ## find vlan switch interface members

    for interface, attributes in data["interfaces"].items():

        if attributes["type"] == "switch":

            interface_name = interface

            for re_match in re.finditer(
                "set interfaces ((?:pp|reth|ae|fe|ge|xe|xle|et)(?:-[0-9]{1,2}/[0-9]{1,2}/)?[0-9]{1,2}) unit ([0-9]{1,4}) family ethernet-switching vlan members "
                + attributes["vlan_name"],
                src_config,
            ):

                data["interfaces"][interface_name]["physical_interfaces"].append(
                    re_match.group(1)
                )

    ## find disable

    for interface in data["interfaces"].keys():

        if "." in interface:
            interface_name = interface.replace(".", " unit ")
        else:
            interface_name = interface

        re_match = re.search(
            "set interfaces " + interface_name + " disable\n", src_config
        )

        if re_match:
            data["interfaces"][interface]["enabled"] = False

        else:
            data["interfaces"][interface]["enabled"] = True

    ## find description

    for interface in data["interfaces"].keys():

        if "." in interface:
            interface_name = interface.replace(".", " unit ")
        else:
            interface_name = interface

        re_match = re.search(
            "set interfaces " + interface_name + ' description "?(.*?)"?\n', src_config
        )

        if re_match:
            data["interfaces"][interface]["description"] = re_match.group(1)

        else:
            data["interfaces"][interface]["description"] = ""

    # Parse zones

    logger.info(__name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.info(__name__ + ": parse static routes")

    for route_match in re.finditer(
        "set routing-options static route ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ") next-hop ("
        + common.common_regex.ipv4_address
        + ")",
        src_config,
    ):

        route_network = route_match.group(1)
        route_prefix = route_match.group(2)
        route_gateway = route_match.group(3)

        route = {}

        route["network"] = route_network
        route["mask"] = ipv4_prefix_to_mask(route_prefix)
        route["gateway"] = route_gateway

        re_match = re.search(
            "set routing-options static route "
            + route_network
            + route_prefix
            + " preference ([0-9]{1,3})",
            src_config,
        )

        if re_match:
            route["distance"] = re_match.group(1)
        else:
            route["distance"] = "5"  ## default admin distance for static routes is 5

        route["type"] = "static"

        route["interface"] = interface_lookup(
            route_gateway, data["interfaces"], data["routes"]
        )

        data["routes"].append(route)

    # Parse IPv4 network objects

    logger.info(__name__ + ": parse IPv4 network objects")

    ## host and network objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_network = re_match.group(2)
        network_object_prefix = re_match.group(3)

        data["network_objects"][network_object_name] = {}

        if network_object_prefix == "/32":

            data["network_objects"][network_object_name]["type"] = "host"
            data["network_objects"][network_object_name][
                "host"
            ] = network_object_network

        else:

            data["network_objects"][network_object_name]["type"] = "network"
            data["network_objects"][network_object_name][
                "network"
            ] = network_object_network
            data["network_objects"][network_object_name]["mask"] = ipv4_prefix_to_mask(
                network_object_prefix
            )

    ## fqdn objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) dns-name ("
        + common.common_regex.fqdn
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_fqdn = re_match.group(2)

        data["network_objects"][network_object_name] = {}

        data["network_objects"][network_object_name]["type"] = "fqdn"
        data["network_objects"][network_object_name]["fqdn"] = network_object_fqdn

    ## range objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) range-address ("
        + common.common_regex.ipv4_address
        + ") to ("
        + common.common_regex.ipv4_address
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_address_first = re_match.group(2)
        network_object_address_last = re_match.group(3)

        data["network_objects"][network_object_name] = {}

        data["network_objects"][network_object_name]["type"] = "range"
        data["network_objects"][network_object_name][
            "address_first"
        ] = network_object_address_first
        data["network_objects"][network_object_name][
            "address_last"
        ] = network_object_address_last

    ## find description

    for network_object in data["network_objects"].keys():

        re_match = re.search(
            "address " + network_object + ' description "?(.*?)"?\n', src_config
        )

        if re_match:
            data["network_objects"][network_object]["description"] = re_match.group(1)

        else:
            data["network_objects"][network_object]["description"] = ""

    # Parse IPv6 network objects

    logger.info(__name__ + ": parse IPv6 network objects - not yet supported")

    """
    Parse IPv6 network objects
    """

    # Parse IPv4 network groups

    logger.info(__name__ + ": parse IPv4 network groups - not yet supported")

    ## address sets with address objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address-set (.*?) address (.*?)\n",
        src_config,
    ):

        network_group_name = re_match.group(1)
        network_group_member = re_match.group(2)

        if network_group_name in data["network_groups"]:

            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

        else:

            data["network_groups"][network_group_name] = {}
            data["network_groups"][network_group_name]["members"] = []
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

            data["network_groups"][network_group_name]["type"] = "group"

    ## address sets with nested address sets

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address-set (.*?) address-set (.*?)\n",
        src_config,
    ):

        network_group_name = re_match.group(1)
        network_group_member = re_match.group(2)

        if network_group_name in data["network_groups"]:

            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

        else:

            data["network_groups"][network_group_name] = {}
            data["network_groups"][network_group_name]["members"] = []
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

            data["network_groups"][network_group_name]["type"] = "group"

    ## find description

    for network_group in data["network_groups"].keys():

        re_match = re.search(
            "address-set " + network_group + ' description "?(.*?)"?\n', src_config
        )

        if re_match:
            data["network_groups"][network_group]["description"] = re_match.group(1)

        else:
            data["network_groups"][network_group]["description"] = ""

    # Parse IPv6 network groups

    logger.log(3, __name__ + ": parse IPv6 network groups - not yet supported")

    """
    Parse IPv6 network groups
    """

    # Parse service objects

    logger.log(3, __name__ + ": parse service objects - not yet supported")

    """
    Parse service objects
    """

    # Parse service groups

    logger.log(3, __name__ + ": parse service groups - not yet supported")

    """
    Parse service groups
    """

    # Parse firewall policies

    logger.log(3, __name__ + ": parse firewall policies - not yet supported")

    """
    Parse firewall policies
    """

    ## remember any, any-ipv4 and any-ipv6

    ## check if default service objects or groups are in use and add to data if so

    # Parse NAT

    logger.log(3, __name__ + ": parse NAT - not yet supported")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.info(__name__ + ": parser module finished")

    return data
