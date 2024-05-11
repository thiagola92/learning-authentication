import sys
import httpx

# Get email from command line
email = sys.argv[1]
content = f"{email}"

# Request recovery code
response = httpx.post("http://127.0.0.1:8000/recover_account", content=content)
print(response.content)