from concurrent.futures import ThreadPoolExecutor

import yaml
from netmiko import ConnectHandler


def get_version_and_interfaces(device):
    commands = ["show version", "show interfaces"]
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
        results = executor.map(get_version_and_interfaces, devices)
        for result in results:
            if result is not None:
                # from pprint import pprint
                # pprint(result)
                ver = result["show version"][0]  # type: ignore
                print(
                    f"{ver["hostname"]} is version {ver["version"]} using the {ver["software_image"]} image."
                )
                first_intf = next(iter(result["show interfaces"]))  # type: ignore
                print(
                    f"The first interface of {ver["hostname"]} is {first_intf["interface"]} ({first_intf["mac_address"]}).\n"
                )
