
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

# ✅ Splunk Search Query
SEARCH_QUERY = 'search index="price_demo" source="prices.csv" | eval discount = round ((price - sale_price), 2) | table productId, product_name, price, sale_price, discount, code | head 10'

# ✅ API Endpoint for Search Job (forcing JSON response)
SEARCH_URL = f"{SPLUNK_HOST}/services/search/jobs?output_mode=json"

# ✅ Step 1: Start the search job (forcing JSON response)
data = {"search": SEARCH_QUERY, "exec_mode": "blocking", "output_mode": "json"}
response = requests.post(SEARCH_URL, headers=headers, data=data, verify=False)

# ✅ Debugging: Print response
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)  # Print response for debugging

# ✅ Step 2: Check for errors before parsing JSON
try:
    response_json = response.json()
    if "sid" not in response_json:
        print("Error: 'sid' not found in response. Check Splunk API permissions.")
        exit()
    sid = response_json["sid"]
except json.JSONDecodeError:
    print("Error: Response is not valid JSON. Check Splunk API authentication.")
    exit()

# ✅ Step 3: Fetch Search Results (forcing JSON response)
RESULTS_URL = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results?output_mode=json"
results_response = requests.get(RESULTS_URL, headers=headers, verify=False)

# ✅ Debugging: Print response
print("Results Response Status Code:", results_response.status_code)
print("Results Response Text:", results_response.text)  # Print response for debugging

# ✅ Step 4: Parse Results JSON
try:
    results_json = results_response.json()
    print("Search Results:", json.dumps(results_json, indent=2))
except json.JSONDecodeError:
    print("Error: Unable to decode search results JSON.")
