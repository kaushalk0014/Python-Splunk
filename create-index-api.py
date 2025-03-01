import requests
import base64
import json
from urllib3.exceptions import InsecureRequestWarning

# ✅ Suppress SSL warnings (for local testing only)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ✅ Splunk API Details
SPLUNK_HOST = "https://127.0.0.1:8089"
USERNAME = "admin"
PASSWORD = "Admin"  # Replace with actual password

# ✅ Encode Credentials for Basic Auth
encoded_credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

# ✅ Headers with Authorization
headers = {
    "Authorization": f"Basic {encoded_credentials}"
}

# ✅ Check if Index Exists
INDEX_NAME = "custom_index_table"
CHECK_INDEX_URL = f"{SPLUNK_HOST}/servicesNS/admin/search/data/indexes?output_mode=json"

response = requests.get(CHECK_INDEX_URL, headers=headers, verify=False)

if response.status_code == 200:
    indexes = response.json().get("entry", [])
    index_names = [index["name"] for index in indexes]

    if INDEX_NAME in index_names:
        print(f"✅ Index '{INDEX_NAME}' already exists. No need to create.")
    else:
        # ✅ Create Index if it does not exist
        CREATE_INDEX_URL = f"{SPLUNK_HOST}/servicesNS/admin/search/data/indexes"
        index_data = f"name={INDEX_NAME}&datatype=event"

        create_response = requests.post(CREATE_INDEX_URL, headers=headers, data=index_data, verify=False)
        print("Index Creation Status Code:", create_response.status_code)
        print("Index Creation Response:", create_response.text)
else:
    print("Error checking indexes:", response.status_code, response.text)
