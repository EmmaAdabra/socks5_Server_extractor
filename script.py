from PIL import Image
import os
import sys
import pytesseract
import re
import csv

# Set the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# the dir that contains the images should be in the same directory with script file and should be name images
current_dir = os.path.dirname(os.path.abspath(__file__))
socks_images_dir = os.path.join(current_dir, "socks_images")
csv_dir = os.path.join(current_dir, "csv")

def get_socks_images(image_dir):
  socks_images = [
    os.path.join(socks_images_dir, img_name)
        for img_name in os.listdir(socks_images_dir)
        if (img_name[0] != ".") and (img_name.endswith(".png") or img_name.endswith(".jpeg") or img_name.endswith(".jpg"))
  ]

  return socks_images


def extract_text_from_image(image_path):
  image = Image.open(image_path)
  return pytesseract.image_to_string(image)


# Use regex to extract the IP addresses and ports
def extract_sockets(text):
    # Regex to match IP:Port (e.g., 162.19.7.47:27828)
    socket_pattern = r'(\d{1,3}(?:\.\d{1,3}){3}:\d+)'
    sockets = re.findall(socket_pattern, text)
    return sockets


def extract_text(extracted_text):
    # Use regex to find the relevant sections
    country_region = re.search(r'COUNTRY(.*?)REGION', extracted_text, re.DOTALL)
    region_city = re.search(r'REGION(.*?)CITY', extracted_text, re.DOTALL)
    city_end = re.search(r'CITY(.*)', extracted_text, re.DOTALL)

    # Extract the matched groups and clean them up
    country_to_region = country_region.group(1).strip() if country_region else ''
    region_to_city = region_city.group(1).strip() if region_city else ''
    city_to_end = city_end.group(1).strip() if city_end else ''

    # Return the results
    return {
        "country": [country.strip() for country in country_to_region.splitlines() if country.strip()],
        "region": [region.strip() for region in region_to_city.splitlines() if region != ""],
        "city": [city.strip() for city in city_to_end.splitlines() if city != ""],
    }
    

def main():
  """controls program flow and logic"""
  # check if source directory exist
  if not os.path.exists(socks_images_dir):
     print("Directory does not exist")
     sys.exit(1)

  # check if source directory is empty
  if len(os.listdir(socks_images_dir)) == 0:
    print("Directory is empty")
    sys.exit(1)

  socks_images = get_socks_images(socks_images_dir)
  image_text_content = extract_text_from_image(socks_images[0])
  sockets = extract_sockets(image_text_content)
  cities = extract_text(image_text_content)
  print(cities["country"])
  print(sockets)
  print()
  # print(image_text_content)


if __name__ == "__main__":
  main()