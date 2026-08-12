import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("Missing LINE_CHANNEL_ACCESS_TOKEN secret")

API = "https://api.line.me/v2/bot"
DATA_API = "https://api-data.line.me/v2/bot"


def request_json(method, url, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            print(f"{method} HTTP", response.status)
            print(body)
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"{method} HTTP", e.code)
        print(body)
        raise


def create_rich_menu(name, areas):
    payload = {
        "size": {"width": 2500, "height": 1686},
        "selected": False,
        "name": name,
        "chatBarText": "選單",
        "areas": areas,
    }
    result = request_json("POST", f"{API}/richmenu", payload)
    return result["richMenuId"]


def upload_image(rich_menu_id):
    image_path = "bu.jpg"
    if not os.path.exists(image_path):
        raise SystemExit(f"Missing image: {image_path}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    print("IMAGE BYTES", len(image_data))
    if len(image_data) >= 1000000:
        raise SystemExit("Compressed image is still too large for LINE (< 1,000,000 bytes required)")

    upload_url = f"{DATA_API}/richmenu/{rich_menu_id}/content"
    req = urllib.request.Request(
        upload_url,
        data=image_data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "image/jpeg",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            print("UPLOAD HTTP", response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("UPLOAD HTTP", e.code)
        print(e.read().decode("utf-8"))
        raise


def delete_alias_if_exists(alias_id):
    url = f"{API}/richmenu/alias/{alias_id}"
    req = urllib.request.Request(
        url,
        data=None,
        headers={"Authorization": f"Bearer {TOKEN}"},
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(req) as response:
            print("DELETE ALIAS HTTP", response.status, alias_id)
    except urllib.error.HTTPError as e:
        # 404 means the alias does not exist yet, which is fine.
        if e.code == 404:
            print("ALIAS NOT FOUND", alias_id)
            return
        print("DELETE ALIAS HTTP", e.code, alias_id)
        print(e.read().decode("utf-8"))
        raise


def create_alias(alias_id, rich_menu_id):
    payload = {"richMenuAliasId": alias_id, "richMenuId": rich_menu_id}
    request_json("POST", f"{API}/richmenu/alias", payload)


def set_default(rich_menu_id):
    url = f"{API}/user/all/richmenu/{rich_menu_id}"
    req = urllib.request.Request(
        url,
        data=b"",
        headers={"Authorization": f"Bearer {TOKEN}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            print("DEFAULT HTTP", response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("DEFAULT HTTP", e.code)
        print(e.read().decode("utf-8"))
        raise


# Two Rich Menus = two pages.
# Page A -> Page B via the right button.
# Page B -> Page A via the left button.
# The same uploaded image is used for both until a separate Page B artwork is provided.
A_ALIAS = "tinytangyuan-menu-a"
B_ALIAS = "tinytangyuan-menu-b"

A_AREAS = [
    {
        "bounds": {"x": 0, "y": 0, "width": 1250, "height": 1686},
        "action": {"type": "message", "label": "首頁", "text": "首頁"},
    },
    {
        "bounds": {"x": 1250, "y": 0, "width": 1250, "height": 1686},
        "action": {
            "type": "richmenuswitch",
            "richMenuAliasId": B_ALIAS,
            "data": "page=B",
            "label": "下一頁",
        },
    },
]

B_AREAS = [
    {
        "bounds": {"x": 0, "y": 0, "width": 1250, "height": 1686},
        "action": {
            "type": "richmenuswitch",
            "richMenuAliasId": A_ALIAS,
            "data": "page=A",
            "label": "上一頁",
        },
    },
    {
        "bounds": {"x": 1250, "y": 0, "width": 1250, "height": 1686},
        "action": {"type": "message", "label": "功能", "text": "功能"},
    },
]

print("Creating Rich Menu A...")
menu_a = create_rich_menu("TinyTangyuan Menu A", A_AREAS)
print("Rich Menu A ID:", menu_a)

print("Creating Rich Menu B...")
menu_b = create_rich_menu("TinyTangyuan Menu B", B_AREAS)
print("Rich Menu B ID:", menu_b)

print("Uploading image to Page A...")
upload_image(menu_a)
print("Uploading image to Page B...")
upload_image(menu_b)

print("Refreshing Rich Menu aliases...")
delete_alias_if_exists(A_ALIAS)
delete_alias_if_exists(B_ALIAS)
create_alias(A_ALIAS, menu_a)
create_alias(B_ALIAS, menu_b)

print("Setting Page A as the default Rich Menu...")
set_default(menu_a)

print("SUCCESS: TinyTangyuan Pages A + B created, images uploaded, aliases configured, and Page A set as default.")
print("Page A Rich Menu ID:", menu_a)
print("Page B Rich Menu ID:", menu_b)
print("Page A alias:", A_ALIAS)
print("Page B alias:", B_ALIAS)
