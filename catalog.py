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
def get_user_balance(user_id, comp_id):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.BALANCE
        FROM DRIVER d
        JOIN BALANCE b ON d.DRIVER_ID = b.DRIVER_ID
        WHERE d.USER_ID = %s AND b.SPONSORCOMP_ID = %s
        """,
        (user_id, comp_id)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(row["BALANCE"]) if row else 0.0


# Helper function to get the companies a driver belongs to
def get_driver_companies(user_id):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT sc.SPONSORCOMP_ID, sc.SPONSORCOMP_NAME
        FROM DRIVER d
        JOIN BALANCE b ON b.DRIVER_ID = d.DRIVER_ID
        JOIN SPONSORCOMP sc ON sc.SPONSORCOMP_ID = b.SPONSORCOMP_ID
        WHERE d.USER_ID = %s
        ORDER BY sc.SPONSORCOMP_NAME
        """,
        (user_id,)
    )
    return cursor.fetchall()


# helper function to get the allowed search queries for a driver based on the comany they belong to
def get_allowed_terms(user_id, comp_id):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT so.`QUERY`
        FROM DRIVER d
        JOIN BALANCE b ON b.DRIVER_ID = d.DRIVER_ID
        JOIN SPONSORORDERS so ON so.SPONSORCOMP_ID = b.SPONSORCOMP_ID
        WHERE d.USER_ID = %s AND b.SPONSORCOMP_ID = %s
        ORDER BY so.`QUERY`
        """,
        (user_id, comp_id)
    )
    return [row["QUERY"].lower() for row in cursor.fetchall()]


# helper function to get sponsor and sponsor company ids
def get_sponsor_info(user_id):
    """Returns (sponsor_id, sponsorcomp_id) for a sponsor user, or (None, None)."""
    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT SPONSOR_ID, SPONSORCOMP_ID FROM SPONSOR WHERE USER_ID = %s",
        (user_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return (row["SPONSOR_ID"], row["SPONSORCOMP_ID"]) if row else (None, None)


@cat.route("/catalog", methods=["GET", "POST"])
def catalog():
    items = []
    error = None
    total = 0

    user_id = session.get("user_id")
    # balance = get_user_balance(user_id)

    source = request.form if request.method == "POST" else request.args
    page = 1 if request.method == "POST" else source.get("page", 1)

    query = source.get("query", "").strip()

    try:
        per_page = int(source.get("per_page", 10))
    except ValueError:
        per_page = 10
    if per_page not in (10, 25, 50):
        per_page = 10

    page = max(1, int(page))

    # Companies this driver can choose from
    companies = get_driver_companies(user_id)
    valid_ids = {c["SPONSORCOMP_ID"] for c in companies}

    comp_id = None
    allowed_terms = []
    balance = 0.0

    if not companies:
        error = "You aren't assigned to any sponsor company yet."
        query = ""
    else:
        try:
            comp_id = int(source.get("comp_id", ""))
        except ValueError:
            comp_id = None
        if comp_id not in valid_ids:
            comp_id = companies[0]["SPONSORCOMP_ID"]   # default to the first company

        allowed_terms = get_allowed_terms(user_id, comp_id)
        balance = get_user_balance(user_id, comp_id)

        if query and query.lower() not in allowed_terms:
            error = "That search isn't approved by this sponsor."
            query = ""

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
        total_pages=total_pages,
        companies=companies,
        comp_id=comp_id,
        allowed_terms=allowed_terms,
        balance=balance
    )


@cat.route("/catalog-items", methods=["GET", "POST"])
def sponsor_catalog_items():
    user_id = session.get("user_id")
    sponsor_id, comp_id = get_sponsor_info(user_id)

    message = None
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        action = request.form.get("action")
        term = request.form.get("term", "").strip().lower()

        if action == "add":
            if not term or len(term) > 100:
                message = "Enter a term up to 100 characters."
            else:
                cursor.execute("""
                    INSERT IGNORE INTO SPONSORORDERS
                        (`QUERY`, SPONSORCOMP_ID, USER_ID, SPONSOR_ID)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (term, comp_id, user_id, sponsor_id)
                )
                conn.commit()

        elif action == "delete":
            cursor.execute(
                "DELETE FROM SPONSORORDERS WHERE SPONSORCOMP_ID = %s AND `QUERY` = %s",
                (comp_id, term)
            )
            conn.commit()

    cursor.execute(
        "SELECT `QUERY` FROM SPONSORORDERS WHERE SPONSORCOMP_ID = %s ORDER BY `QUERY`",
        (comp_id,)
    )
    terms = [row["QUERY"] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return render_template(
        "sponsor_catalog_terms.html", 
        terms=terms, 
        message=message
    )