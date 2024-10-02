# SOCKS5 Server Extractor & Validator

This project contains two scripts that work together to extract SOCKS5 server IP addresses and ports from images and then validate which of those servers are live. The project includes OCR for text extraction and server validation with geolocation lookups.

## Project Structure

```bash
├── extract_socket.py   # Extracts IPs and ports from images and saves them to a CSV file.
├── is_live.py          # Validates extracted SOCKS5 servers and checks their geographic location.
├── images/             # Folder to store images containing SOCKS5 server data.
├── csv/                # Folder where CSV files with extracted and live server data are stored.
```

## Scripts Overview

### 1. `extract_socket.py`

This script performs the following tasks:

- Extracts text from images in the `images/` directory using `pytesseract` (OCR).
- Uses a regular expression to find IP addresses and ports from the extracted text.
- Saves the IP and port data to a CSV file (`socks_server.csv`) in the `csv/` directory.  

### 2. `is_live.py`

This script reads the extracted server information from the CSV file (`socks_server.csv`) and:

- Validates if each server is live by attempting a connection.
- Fetches the geographic location (country, region, city) of each live server.
- Saves live servers' details to a CSV file (`live_servers.csv`) in the `csv/` directory.

## Usage

1. Place your image files containing SOCKS5 server information in the `images/` folder.

2. Run `extract_socket.py` to extract the IP addresses and ports from the images and save them in a CSV file.

    ```bash
    python extract_socket.py
    ```

3. Run `is_live.py` to validate the servers and retrieve their geographic locations.

    ```bash
    python is_live.py
    ```

## Requirements

- Python 3.x
- Required libraries: `Pillow`, `pytesseract`, `requests`, `multiprocessing`, `concurrent.futures`

You can install the dependencies with:

- For Linux or macOS:

    ```bash
    pip install Pillow pytesseract requests
    ```

- For Windows:

    ```bash
    py -m pip install Pillow pytesseract requests
    ```

Make sure to have Tesseract OCR installed and update the path in `extract_socket.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Notes

- The extracted server details will be stored in the `csv/socks_server.csv` file.
- The live and validated servers will be stored in the `csv/live_servers.csv` file.  
