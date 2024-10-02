import socket
import requests
import csv
import os
import sys
from concurrent.futures import ThreadPoolExecutor

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(current_dir, "csv")
servers_file_path = os.path.join(csv_dir, "socks_server.csv")
live_server = []


def csv_to_dict_list(file_path):
  if not os.path.exists(file_path):
     print(f"can't find {file_path} directory")
     sys.exit(1)
  
  if not os.path.exists(file_path):
     print(f"socks_server.csv do not exist in {file_path}")
     sys.exit(1)
  
  data = []

  # open csv file
  with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file, fieldnames=['ip', 'port'])

    next(csv_reader)
    
    for row in csv_reader:
      data.append({'ip': row['ip'], 'port': row['port']})
  
  return data

def check_socks5_server(ip, port):
    try:
        sock = socket.create_connection((ip, port), timeout=5)
        sock.close()
        return True
    except socket.error:
        return False


def get_server_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json") #location API
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
        add_to_live_server(ip, port, country, region, city)
        print(f"Server is located in {city}, {region}, {country}.")
    else:
        print(f"SOCKS5 server at {ip}:{port} is offline.")


def add_to_live_server(ip, port, county, region, city):
   data = {"IP":ip, "PORT": port, "SOCKET": ip + ":" + port, "COUNTRY": county, "REGION": region, "CITY": city}
   live_server.append(data)


def save_to_csv(file_path, data):
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  file_path = os.path.join(file_path, "live_servers.csv")
  with open(file_path, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=['IP', 'PORT', 'SOCKET', 'COUNTRY', 'REGION', 'CITY'])
    writer.writeheader()  # Write the header
    writer.writerows(data)


def main():
  data = csv_to_dict_list(servers_file_path)

  # using multithreaded approach since it is I/O bond
  with ThreadPoolExecutor(max_workers=10) as executor:
    for server in data:
      ip = server['ip']
      port = server['port']
      executor.submit(check_socks5_server_and_location, ip, port)

  save_to_csv(csv_dir, live_server)
  print(f"{len(live_server)} live server was found out of {len(data)} servers")
  print(f"open {csv_dir} to view them")


if __name__ == "__main__":
   main()