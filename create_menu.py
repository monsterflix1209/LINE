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

# 2) Upload the actual 2500x1686 image from this repository
image_path = "bu.png"
if not os.path.exists(image_path):
    raise SystemExit(f"Missing image: {image_path}")

with open(image_path, "rb") as f:
    image_data = f.read()

upload_url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
upload_req = urllib.request.Request(
    upload_url,
    data=image_data,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "image/png"
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

print("SUCCESS: TinyTangyuan Menu A created and bu.png uploaded.")
print("Rich Menu ID:", rich_menu_id)
