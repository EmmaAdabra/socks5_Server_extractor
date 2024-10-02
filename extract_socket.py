from PIL import Image
import os
import sys
import pytesseract
import re
import csv
from multiprocessing import Pool

# Set the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# the dir that contains the images should be in the same directory with script file and should be name images
current_dir = os.path.dirname(os.path.abspath(__file__))
socks_images_dir = os.path.join(current_dir, "images")
csv_dir = os.path.join(current_dir, "csv")
data = []


def get_socks_images(image_dir):
    socks_images = [
        os.path.join(socks_images_dir, img_name)
        for img_name in os.listdir(socks_images_dir)
        if (img_name[0] != ".")
        and (
            img_name.endswith(".png")
            or img_name.endswith(".jpeg")
            or img_name.endswith(".jpg")
        )
    ]

    return socks_images


def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return None


def extract_ips_and_ports(text):
    # Updated regex pattern to capture IPs with optional spaces
    pattern = r"(\d{1,3}(?:\.\s*\d{1,3}){3}):(\d+)"
    matches = re.findall(pattern, text)

    data = []
    ip_and_port = {}

    if matches:
        for ip, port in matches:
            ip_and_port["ip"] = ip.replace(" ", "")
            ip_and_port["port"] = port
            data.append(ip_and_port)
            ip_and_port = {}

    return data


def add_ip_port_to_list(socks_images):
    try:
        # using subprocesses
        with Pool(processes=4) as pool:
            extracted_texts = pool.map(extract_text_from_image, socks_images)
        for text in extracted_texts:
            ip_and_port = extract_ips_and_ports(text)
            data.extend(ip_and_port)
    except Exception as e:
        print(f"An error occurred: {e}")


def save_to_csv(data):
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    save_path = os.path.join(csv_dir, "socks_server.csv")
    with open(save_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ip", "port"])
        writer.writeheader()  # Write the header
        writer.writerows(data)  # Write the data rows

    print("Success !!!")
    print(
        f"{len(data)} servers extracted from {len(get_socks_images(socks_images_dir))} images and save to {csv_dir}"
    )


def main():
    """controls program flow and logic"""
    # check if source directory exist
    if not os.path.exists(socks_images_dir):
        print("Directory does not exist")
        sys.exit(1)

    # check if source directory is empty
    if len(os.listdir(socks_images_dir)) == 0:
        print("Image directory is empty")
        sys.exit(1)

    socks_images = get_socks_images(socks_images_dir)
    add_ip_port_to_list(socks_images)
    save_to_csv(data)


if __name__ == "__main__":
    main()
