import os
import json
from EndDevice import EndDevice
from netmiko import ConnectHandler
from jinja2 import Template

# Qemu IOSv in GNS3/EVE-ng

switch = {
    'device_type':'cisco_ios',
    'ip':'192.168.1.254',
    'username':'test',
    'password':'test',
    'secret':'test'
    }
# Hold List of end devices
list_enddevice = []

# Hold full port config for a Switch
port_configs = ''

# Change the default Dir
os.chdir(r'c:/Users/user/Documents')

# Connection to the switch
net_connect = ConnectHandler(**switch)
net_connect.enable()

# Collect information from the switch
arp_output = net_connect.send_command('show ip arp', use_textfsm=True)
cam_output = net_connect.send_command('show mac address-table', use_textfsm=True)

# Mapping for each end device the ip , mac and the port. 
for cam_entry in cam_output:
    for arp_entry in arp_output:
        if cam_entry['destination_address'] in arp_entry.values():
            device = EndDevice(ip = arp_entry['address'], mac = arp_entry['mac'])
            device.get_hostname()
            device.port = cam_entry['destination_port']
            # Add instance in the list of end devices
            list_enddevice.append(device)

# Read the template
with open("template_description.j2", 'r') as f :
    template_description = Template(f.read(), keep_trailing_newline=True)

# Populating the template and generate and str of the full config
for device in list_enddevice:
    port_config = template_description.render(
        port = device.port,
        hostname = device.hostname)
    port_configs += port_config

# Write the full config previously generate into a .txt 
with open("port_configs.txt", "w") as f:
    f.write(port_configs)

# Push the .txt previously create

push_config = net_connect.send_config_from_file("port_configs.txt")
print(push_config)