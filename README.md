# werkzeug pin generator

A werkzeug pin generator for python 3.10 (not tested on other versions) and for lazy people like me.

All you need to do is to provide the informations evoqued in section ### What do you need.

### Usage

```bash
pip install -r requirements.txt
./werkzeug_pin_generator.py
```

### What do you need ?

You need to leak some infos from the target machine. Usually it is done via LFI .

- machine_id : /etc/machine-id
- boot_id if machine_id does'nt exist : /proc/sys/kernel/random/boot_id
- cgroup : /proc/self/cgroup
- username of the user who started the flask app : /proc/self/environ
- the flask path of app.py of the flask application
- the device's mac address used : Leak /proc/net/arp then, leak /sys/class/net/<device>/address. Enter the mac address.

Enter all these informations inside the .env file and the script will generate some pins you'll can enter if werkzeug debug is enabled on the the website.

No test has been done on this script, ie, use it for hack the box or try hack me or whatever.
