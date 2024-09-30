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
  extract_text_from_image(socks_images[0])


if __name__ == "__main__":
  main()