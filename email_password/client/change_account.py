import sys
import httpx
from urllib.parse import urlencode

# Get email, code and new password from command line
email = sys.argv[1]
code = sys.argv[2]
password = sys.argv[3]

# Setup body string
body = urlencode({"email": email, "code": code, "password": password})

# Change account password
response = httpx.post("http://127.0.0.1:8000/change_account", content=body)
print(response.content)