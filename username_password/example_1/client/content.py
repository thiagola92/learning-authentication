import sys
import httpx
from urllib.parse import urlencode

# Get username and password from command line
username = sys.argv[1]
password = sys.argv[2]

# Setup body string
body = urlencode({"username": username, "password": password})

# Login
response = httpx.post(
    "http://127.0.0.1:8000/login",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    content=body,
)

# Get content
response = httpx.get("http://127.0.0.1:8000/", cookies=response.cookies)
print(response.content)