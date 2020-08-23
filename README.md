# anti-arp

Undos arp spoofing from popular parental controls devices

## HOWTO:

1. Prerequisites: Install Python 3 (not 2) on any machine. You need admin access on the machine, and it must be on the same network as the device that is doing the ARP spoofing.
1. Install modules: `python3 -m pip install -r requirements.txt`. Preferably under a [venv](https://docs.python.org/3/library/venv.html).
1. Create configuration file. This can be called anything, but `config.txt` works well. The first line MUST be the router. The format is "IP MAC" with IP being the IP address of the device you want to undo the ARP spoofing on, and MAC is the hardware address. Google "How to find mac address on xyz" if you don't know how to get it
1. This program must be run as admin / root. Run the file with `python3 anti-arp.py config.txt`. If you want more details about what is going on, add a `--verbose` after it, like so: `python3 anti-arp.py config.txt --verbose`.
1. Let it run in the background. It may hog some CPU.

## Sample config file
```
192.168.1.1 52:54:00:11:68:c1
192.168.2.10 52:54:00:b7:d7:a5
```
