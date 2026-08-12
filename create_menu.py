import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("Missing LINE_CHANNEL_ACCESS_TOKEN secret")

# 1) Create the Rich Menu
url = "https://api.line.me/v2/bot/richmenu"
payload = {
    "size": {"width": 2500, "height": 1686},
    "selected": False,
    "name": "TinyTangyuan Menu A",
    "chatBarText": "選單",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": 1250, "height": 1686},
            "action": {"type": "message", "label": "首頁", "text": "首頁"}
        },
        {
            "bounds": {"x": 1250, "y": 0, "width": 1250, "height": 1686},
            "action": {"type": "message", "label": "下一頁", "text": "下一頁"}
        }
    ]
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    url,
    data=data,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")
        print("CREATE HTTP", response.status)
        print(body)
        rich_menu_id = json.loads(body)["richMenuId"]
except urllib.error.HTTPError as e:
    print("CREATE HTTP", e.code)
    print(e.read().decode("utf-8"))
    raise

# 2) Upload the compressed JPEG produced by the workflow.
image_path = "bu.jpg"
if not os.path.exists(image_path):
    raise SystemExit(f"Missing image: {image_path}")

with open(image_path, "rb") as f:
    image_data = f.read()

print("IMAGE BYTES", len(image_data))
if len(image_data) >= 1000000:
    raise SystemExit("Compressed image is still too large for LINE (< 1,000,000 bytes required)")

upload_url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
upload_req = urllib.request.Request(
    upload_url,
    data=image_data,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "image/jpeg"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(upload_req) as response:
        print("UPLOAD HTTP", response.status)
        print(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("UPLOAD HTTP", e.code)
    print(e.read().decode("utf-8"))
    raise

# 3) Set this Rich Menu as the default for all users.
default_url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
default_req = urllib.request.Request(
    default_url,
    data=b"",
    headers={"Authorization": f"Bearer {TOKEN}"},
    method="POST"
)

try:
    with urllib.request.urlopen(default_req) as response:
        print("DEFAULT HTTP", response.status)
        print(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("DEFAULT HTTP", e.code)
    print(e.read().decode("utf-8"))
    raise

print("SUCCESS: TinyTangyuan Menu A created, image uploaded, and set as default.")
print("Rich Menu ID:", rich_menu_id)
