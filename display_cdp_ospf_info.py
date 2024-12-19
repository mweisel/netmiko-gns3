from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

import yaml
from netmiko import ConnectHandler


def get_cdp_and_ospf(device):
    commands = ["show cdp neighbors detail", "show ip ospf neighbor"]
    results = {}
    try:
        with ConnectHandler(**device) as conn:
            for cmd in commands:
                output = conn.send_command(cmd, use_textfsm=True)
                results[cmd] = output
        return results
    except ConnectionRefusedError as err:
        print(f"{device["host"]}: {err}\n")


if __name__ == "__main__":
    with open("devices.yaml", encoding="utf-8") as f:
        devices = yaml.safe_load(f)
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_cdp_and_ospf, devices)
        for result in results:
            if result is not None:
                pprint(result)
