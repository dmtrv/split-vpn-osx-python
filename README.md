# Split VPN Routing script for OS X

This script modifying routing table for split tunneling.

## Installation

```Terminal
$ git clone https://github.com/davochka/split-vpn-osx-python.git
$ cd split-vpn-osx-python
$ sudo install -c -m 0755 ip-up.py /etc/ppp/ip-up
$ sudo install -c -m 0666 ip-up.json /etc/ppp/ip-up.json
$ touch /tmp/ip-up-vpn.log
```
## Configuration

Uncheck "Send all traffic over VPN connection" checkbox  in the OS X VPN settings!

Open and edit /etc/ip-up.json with your favorite editor.  You need to find out the subnet of the IPs in your VPN you need access to and a local IP.

ip-up.json config example which has two sections for two different VPNs:

``` 
{ "VPN": {
    "192.168.3.3": [
        "192.168.3",
        "10.248.0"
    ],
    "192.168.10.3": [
        "192.168.7",
        "10.248.1"
    ] }
}
```

Other traffic will be routed through default gateway.

To reset the routing table back disconnect from the VPN.

## Troubleshooting

Check the log ```/tmp/ip-up-vpn.log```