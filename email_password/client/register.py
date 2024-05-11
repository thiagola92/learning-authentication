import sys
import httpx

# Get username and password from command line
email = sys.argv[1]
password = sys.argv[2]

# Setup body string
body = f"email={email}&password={password}"

# Register user
response = httpx.post(
    "http://127.0.0.1:8000/register",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    content=body,
)
print(response.content)
