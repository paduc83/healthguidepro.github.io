import nmap

def scan_devices(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac = nm[host]['addresses']['mac']
        else:
            mac = "Unknown"
        devices.append({'ip': host, 'mac': mac, 'hostname': nm[host].hostname()})

    return devices

def save_to_txt(devices, filename):
    with open(filename, 'w') as file:
        for device in devices:
            file.write(f"IP: {device['ip']}\tMAC: {device['mac']}\tHostname: {device['hostname']}\n")

ip_range = "192.168.1.1/24"

devices = scan_devices(ip_range)

save_to_txt(devices, "network_devices.txt")

print("Network scan completed and saved to network_devices.txt")
