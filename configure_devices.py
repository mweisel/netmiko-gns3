from concurrent.futures import ThreadPoolExecutor
from difflib import unified_diff
from pathlib import Path

import yaml
from netmiko import ConnectHandler


def set_configuration(device):
    try:
        with ConnectHandler(**device) as conn:
            before_config = conn.send_command("show running-config")
            conn.send_config_from_file(
                f"{Path("configs").resolve()}/{device["host"]}.txt"
            )
            after_config = conn.send_command("show running-config")
            diff = unified_diff(
                before_config.splitlines(),  # type: ignore
                after_config.splitlines(),  # type: ignore
                fromfile=f"{device["host"]}-> before",
                tofile=f"{device["host"]}-> after",
                lineterm="",
            )
        return "\n".join(list(diff))
    except ConnectionRefusedError as err:
        print(f"{device["host"]}: {err}\n")


if __name__ == "__main__":
    with open("devices.yaml", encoding="utf-8") as f:
        devices = yaml.safe_load(f)
    with ThreadPoolExecutor() as executor:
        results = executor.map(set_configuration, devices)
        for result in results:
            if result is not None:
                print(result)
