import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    start_port, end_port = port_range
    
    # Resolve hostname to IP address
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        # Check if it's an IP address
        try:
            socket.inet_aton(target)
            ip_address = target
        except socket.error:
            return "Error: Invalid IP address" if target.replace('.', '').isdigit() else "Error: Invalid hostname"
    
    # Scan the specified range of ports
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    if verbose:
        # Format the output for verbose mode
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            hostname = target
        
        if hostname == target:
            output = f"Open ports for {target}\nPORT     SERVICE\n"
        else:
            output = f"Open ports for {hostname} ({ip_address})\nPORT     SERVICE\n"
            
        for port in open_ports:
            service = ports_and_services.get(port, "unknown")
            output += f"{port:<8} {service}\n"
        return output.strip()
    
    return open_ports

