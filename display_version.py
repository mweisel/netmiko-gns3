from concurrent.futures import ThreadPoolExecutor

import yaml
from netmiko import ConnectHandler


def get_version(device):
    try:
        with ConnectHandler(**device) as conn:
            output = conn.send_command("show version")
        return output
    except ConnectionRefusedError as err:
        print(f"{device["host"]}: {err}\n")


if __name__ == "__main__":
    with open("devices.yaml", encoding="utf-8") as f:
        devices = yaml.safe_load(f)
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_version, devices)
        for i, result in enumerate(results, start=1):
            if result is not None:
                print("//", i)
                print(result)
