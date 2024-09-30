import socket
import requests

def check_socks5_server(ip, port):
    try:
        # Try to establish a socket connection to the SOCKS5 server on the specified port
        sock = socket.create_connection((ip, port), timeout=5)
        sock.close()
        return True  # Server is live
    except socket.error:
        return False  # Server is offline

def get_server_location(ip):
    try:
        # Use the ipinfo API to get the location details
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            country = data.get('country', 'Unknown')
            region = data.get('region', 'Unknown')
            city = data.get('city', 'Unknown')
            return country, region, city
        else:
            return "Unknown", "Unknown", "Unknown"
    except requests.RequestException:
        return "Unknown", "Unknown", "Unknown"

def check_socks5_server_and_location(ip, port):
    # Check if the SOCKS5 server is live
    if check_socks5_server(ip, port):
        print(f"SOCKS5 server at {ip}:{port} is live.")
        
        # Get the server location
        country, region, city = get_server_location(ip)
        print(f"Server is located in {city}, {region}, {country}.")
    else:
        print(f"SOCKS5 server at {ip}:{port} is offline.")

# Example usage
check_socks5_server_and_location('173.255.223.18', 3128)  # Replace with your SOCKS5 server IP and port