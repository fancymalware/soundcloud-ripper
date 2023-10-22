import os
import asyncio
import requests
import re
import warnings
from colorama import Fore
from urllib.parse import urlparse, urlunparse
import random
import string
import xml.etree.ElementTree as ET

# Ignore RuntimeWarning notification
warnings.simplefilter('ignore', RuntimeWarning)

# Function to check a single URL
async def check_single_url(short_url, existing_urls, xml_root, new_urls):
    # Perform an HTTP request to get the response
    response = await asyncio.to_thread(requests.get, short_url, allow_redirects=False)

    # Check if the response is a redirection (status code 302)
    if response.status_code == 302:
        full_url = response.headers.get('Location', '')
        parsed_url = urlparse(full_url)
        url_final = urlunparse(parsed_url._replace(query=''))

        # Search for a pattern in the final URL
        match = re.search(r's-[a-zA-Z0-9]{11}', url_final)

        if match:
            # Check if the URL already exists
            if short_url not in existing_urls:
                # Check if the URL is new
                if short_url not in new_urls:
                    new_urls.add(short_url)
                    # Add the URL to the XML file
                    entry = ET.SubElement(xml_root, "track")
                    entry.text = short_url + "\n"
                    print(Fore.GREEN + "[+] Valid URL: ", short_url)
            else:
                print(Fore.YELLOW + "[*] URL already recorded: ", short_url)
        else:
            print(Fore.RED + "[-] Invalid URL: ", short_url)

# Main function to check a certain number of URLs
async def check(num_urls_to_generate):
    folder_name = "Hits"
    file_name = "hits.xml"
    full_file_path = os.path.join(folder_name, file_name)

    # Check if the "Hits" folder exists, create it if necessary
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Check if the "hits.xml" file exists
    if os.path.exists(full_file_path):
        existing_tree = ET.parse(full_file_path)
        existing_root = existing_tree.getroot()
        existing_urls = set()
        for track in existing_root:
            url = track.text.strip()
            existing_urls.add(url)
    else:
        existing_root = ET.Element("tracks")
        existing_urls = set()

    new_urls = set()

    xml_root = ET.Element("new_tracks")

    tasks = []

    print("\n\n< Checking... >\n")

    # Generate and check a certain number of URLs
    for _ in range(num_urls_to_generate):
        characters = string.ascii_letters + string.digits
        rand = ''.join(random.choice(characters) for _ in range(5))
        short_url = "https://on.soundcloud.com/" + rand

        task = check_single_url(short_url, existing_urls, xml_root, new_urls)
        tasks.append(task)

    # Execute all tasks asynchronously
    await asyncio.gather(*tasks)

    # Add the new URLs to the existing XML file
    existing_root.extend(xml_root)

    # Save the changes to the XML file
    with open(full_file_path, "wb") as xml_file:
        xml_tree = ET.ElementTree(existing_root)
        xml_tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    print(Fore.YELLOW + f"\n[!] Finished ! {len(new_urls)} new private tracks found on {num_urls_to_generate} generated URL <3\n")

# Entry point of the program
if __name__ == "__main__":
    num_urls = int(input("\nNumber of Short URL: "))
    asyncio.run(check(num_urls))
