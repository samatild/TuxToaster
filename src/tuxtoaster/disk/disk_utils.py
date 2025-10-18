import subprocess
import json
import os


def create_dummy_file(directory):
    temp_file_path = os.path.join(directory, "temp_file")
    print(f"Warming up: Creating dummy file at {temp_file_path}")
    subprocess.run(["dd", "if=/dev/zero", f"of={temp_file_path}", "bs=10M", "count=10", "oflag=direct"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return temp_file_path


def create_dummy_file_multi(directory, file_name):
    temp_file_path = os.path.join(directory, file_name)
    print(f"Warming up: Creating dummy file at {temp_file_path}")
    subprocess.run(["dd", "if=/dev/zero", f"of={temp_file_path}", "bs=10M", "count=10", "oflag=direct"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return temp_file_path


def get_unique_mount_points():
    mount_points = {}
    output = subprocess.check_output(["lsblk", "-o", "NAME,MOUNTPOINT", "-J"], universal_newlines=True)
    lsblk_json = json.loads(output)
    for device in lsblk_json['blockdevices']:
        parent_device_name = f"/dev/{device['name']}"
        if parent_device_name.startswith("/dev/loop"):
            continue
        if 'children' in device:
            for child in device['children']:
                mount_point = child.get('mountpoint')
                device_name = f"/dev/{child['name']}"
                if not mount_point or mount_point.startswith('/boot'):
                    continue
                if mount_point not in mount_points:
                    mount_points[mount_point] = {'device_name': device_name, 'parent_device': parent_device_name}
                else:
                    mount_points[mount_point]['parent_device'] += f", {parent_device_name}"
    return mount_points


