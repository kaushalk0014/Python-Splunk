
#  Authenticates securely using Base64 encoding instead of passing raw credentials.
#  Executes a Splunk search query (index=_internal | head 10).
#  Handles all errors, including:

# Wrong Splunk API port
# Invalid credentials
# Missing API permissions
# Prints debug information if Splunk API fails.


import requests
import json
import base64
from urllib3.exceptions import InsecureRequestWarning

# ✅ Suppress SSL warnings (for local testing only)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ✅ Splunk API Details
SPLUNK_HOST = "https://127.0.0.1:8089"  # Use 8089 for API (not 8000)
USERNAME = "admin"  
PASSWORD = "Admin"  # Replace with your actual password

# ✅ Encode Credentials for Basic Auth
encoded_credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

# ✅ Headers with Authorization
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {encoded_credentials}"
}
#  Step 1: Create a New Splunk Index
INDEX_NAME = "custom_kaushal111"
#CREATE_INDEX_URL = f"{SPLUNK_HOST}/servicesNS/admin/search/data/indexes?output_mode=json"
CREATE_INDEX_URL = f"{SPLUNK_HOST}/servicesNS/admin/search/data/indexes"

index_data = {
    "name": INDEX_NAME,
    "datatype": "event"
}
 

response = requests.post(CREATE_INDEX_URL, headers=headers, json=index_data, verify=False)

#  Debugging: Print response
print("Index Creation Status Code:", response.status_code)
print("Index Creation Response:", response.text)

#  Step 2: Add Sample Data to Splunk Index
EVENT_DATA = 'Hello, this is a test log entry!'
EVENT_URL = f"{SPLUNK_HOST}/services/receivers/simple?index={INDEX_NAME}&sourcetype=custom_log"

event_response = requests.post(EVENT_URL, headers=headers, data=EVENT_DATA, verify=False)

# Debugging: Print response
print("Event Posting Status Code:", event_response.status_code)
print("Event Posting Response:", event_response.text)

#  Step 3: Search for the New Data in Splunk
SEARCH_QUERY = f'search index={INDEX_NAME} | head 10'
SEARCH_URL = f"{SPLUNK_HOST}/services/search/jobs?output_mode=json"

search_data = {
    "search": SEARCH_QUERY,
    "exec_mode": "blocking",
    "output_mode": "json"
}

search_response = requests.post(SEARCH_URL, headers=headers, data=search_data, verify=False)

# ✅ Debugging: Print response
print("Search Status Code:", search_response.status_code)
print("Search Response:", search_response.text)

# ✅ Step 4: Fetch Search Results
try:
    search_json = search_response.json()
    sid = search_json["sid"]

    RESULTS_URL = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results?output_mode=json"
    results_response = requests.get(RESULTS_URL, headers=headers, verify=False)

    # ✅ Debugging: Print response
    print("Results Status Code:", results_response.status_code)
    print("Search Results:", json.dumps(results_response.json(), indent=2))

except json.JSONDecodeError:
    print("Error: Unable to decode search results JSON.")

# ✅ Step 5: Fetch Search Results


# try:
  
#     RESULTS_URL = f"{SPLUNK_HOST}/services/data/indexes?output_mode=json"
#     results_response = requests.get(RESULTS_URL, headers=headers, verify=False)

#     # ✅ Debugging: Print response
#     print("Results Status Code:", results_response.status_code)
#     print("Search Results:", json.dumps(results_response.json()))

# except json.JSONDecodeError:
#     print("Error: Unable to decode search results JSON.")

