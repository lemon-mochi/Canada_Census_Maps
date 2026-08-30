import requests

# Table 98100001 is the 2021 Census Profile data
product_id = 98100001
language = "en"

# Parameters are passed right in the URL string
url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{product_id}/{language}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    print(f"Requesting download link from: {url}")
    response = requests.get(url, headers=headers)
    
    # This will trigger an error if the URL is broken
    response.raise_for_status() 
    
    # Parse the successful JSON response
    data = response.json()
    
    if data.get("status") == "SUCCESS":
        print("\n[+] Success! Copy and paste this link into your browser to download the zip:")
        print(data.get("object"))
    else:
        print(f"\n[-] StatCan API Error: {data.get('message')}")

except requests.exceptions.HTTPError as http_err:
    print(f"\n[-] HTTP Error: {http_err}")
except Exception as err:
    print(f"\n[-] Error parsing JSON: {err}")
    print("Raw Response text was:", response.text[:200])
