from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from dotenv import load_dotenv
import requests, base64, os, mysql.connector 
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import re
from html import unescape

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

cat = Blueprint("cat", __name__)

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

# This is used to get an access token for ebay's API in order to query for items
# Access tokens are based on your client id and client secret
def get_access_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"

    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        print("Token error:")
        print(response.status_code)
        print(response.text)

        return None

    return response.json()["access_token"]


def get_item_details(item_id, access_token):
    """Call getItem for one item and return the full JSON response."""
    url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    return response.json()


def clean_description(details, max_length=200):
    if not details:
        return ""

    text = details.get("shortDescription")

    if not text:
        html = details.get("description", "")
        # drop script/style blocks
        html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", html)
        # drop tags
        text = re.sub(r"<[^>]+>", " ", html)

    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_length:
        text = text[:max_length].rsplit(" ", 1)[0] + "…"

    return text


# helper for search_ebay's availability
# make availability object readable
def availability_text(avail):
    if not avail:
        return "Availability unknown"

    status = avail.get("estimatedAvailabilityStatus")
    if status == "OUT_OF_STOCK":
        return "Out of stock"

    # exact count (eBay only gives for low stock)
    qty = avail.get("estimatedAvailableQuantity")
    if qty is not None:
        return f"{qty} left"

    # otherwise threshold is more than 10 items
    threshold = avail.get("availabilityThreshold")
    if threshold is not None:
        if avail.get("availabilityThresholdType") == "MORE_THAN":
            return f"More than {threshold} available"
        return f"{threshold} available"

    return "In stock" if status == "IN_STOCK" else "Availability unknown"


# This is used to actually query for ebay items/data
# It will return items in form of json
def search_ebay(query, limit=10, offset=0, max_price=None):
    access_token = get_access_token()

    if not access_token:
        return None, "Could not get eBay access token."

    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    params = {
        "q": query,
        "limit": limit,
        "offset": offset
    }

    if max_price is not None:
        params["filter"] = f"price:[..{max_price:.2f}],priceCurrency:USD"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    data = response.json()
    items = data.get("itemSummaries", [])

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(
            lambda item: get_item_details(item["itemId"], access_token),
            items
        )
        for item, details in zip(items, results):
            avail = None
            if details:
                avail_list = details.get("estimatedAvailabilities", [])
                avail = avail_list[0] if avail_list else None

            item["availability"] = availability_text(avail)
            item["description"] = clean_description(details)

    return data, None


# Helper func to get a user's balance based off of their user_id
def get_user_balance(user_id):
    # connect to sql database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT BALANCE
        FROM DRIVER as d
        JOIN BALANCE as b ON d.DRIVER_ID = b.DRIVER_ID
        WHERE USER_ID = %s
        """,
        (user_id,)
    )
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return float(row["BALANCE"]) if row else 0.0


@cat.route("/catalog", methods=["GET", "POST"])
def catalog():
    items = []
    error = None
    total = 0

    user_id = session.get("user_id")
    balance = get_user_balance(user_id)

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        per_page = int(request.form.get("per_page", 10))
        page = 1
    else:
        query = request.args.get("query", "").strip()
        per_page = request.args.get("per_page", 10)
        page = request.args.get("page", 1)

    per_page = int(per_page)
    if per_page not in (10, 25, 50):
        per_page = 10

    page = max(1, int(page))

    # search for both POST and GET requests
    if query:
        offset = (page - 1) * per_page
        data, error = search_ebay(
            query,
            limit=per_page,
            offset=offset,
            max_price=balance
        )

        if data:
            items = data.get("itemSummaries", [])
            total = int(data.get("total", 0))

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        "catalog.html",
        items=items,
        error=error,
        query=query,
        per_page=per_page,
        page=page,
        total=total,
        total_pages=total_pages
    )