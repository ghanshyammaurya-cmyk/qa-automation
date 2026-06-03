import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Step 1: Load the form page
url = "https://builders-qa.onsumaye.com/ecosystem-engagement/solution-hub/contact-us"
r = session.get(url)

# Optional: Extract CSRF token (if present)
soup = BeautifulSoup(r.text, "html.parser")
token_input = soup.find("input", {"name": "csrf_token"})
csrf_token = token_input["value"] if token_input else None

# Step 2: Prepare data payload (update with real field names)
data = {
    "fullName": "Test User",
    "email": "testuser@example.com",
    "company": "Test Company",
    "role": "QA Tester",
    "phone": "1234567890",
    "inquiryType": "General Inquiry",
    "messageConsent": "on",
}

if csrf_token:
    data["csrf_token"] = csrf_token

# Step 3: Post data
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = session.post(url, data=data, headers=headers)

# Step 4: Validate
if response.status_code == 200:
    print("Form submitted successfully!")
else:
    print(f"Failed to submit form. Status code: {response.status_code}")
    print(response.text[:1000])
