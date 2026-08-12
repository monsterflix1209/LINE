import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("Missing LINE_CHANNEL_ACCESS_TOKEN secret")

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
        print("HTTP", response.status)
        print(body)
except urllib.error.HTTPError as e:
    print("HTTP", e.code)
    print(e.read().decode("utf-8"))
    raise
