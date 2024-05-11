import sys
import httpx
import base64

# Get username and password from command line
username = sys.argv[1]
password = sys.argv[2]

# Setup credentials string
credentials = f"{username}:{password}"
credentials = credentials.encode()
credentials = base64.b64encode(credentials)
credentials = credentials.decode()

# Get content
response = httpx.get("http://127.0.0.1:8000/", headers={"Authorization": f"Basic {credentials}"})
print(response.content)