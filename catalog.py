from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash, current_app, abort, g
from dotenv import load_dotenv
import requests, base64, os, mysql.connector, math, time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import re
from html import unescape

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

SORT_OPTIONS = {"low": "price", "high": "-price"}   # "default" = no sort param

cat = Blueprint("cat", __name__)

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")


# Short-lived cache so browsing approved items doesn't use up eBay API calls.
# (Per process; it resets when the app restarts. Cart and checkout never use it.)
_ITEM_CACHE = {}
ITEM_CACHE_SECONDS = 300

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
def search_ebay(query, limit=10, offset=0, max_price=None, sort=None, enrich=True):
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

    if sort:
        params["sort"] = sort

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

    if enrich:
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
        WHERE d.USER_ID = %s AND b.SPONSORCOMP_ID = %s AND b.IS_ACTIVE = 1
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
        WHERE d.USER_ID = %s AND b.IS_ACTIVE = 1
        ORDER BY sc.SPONSORCOMP_NAME
        """,
        (user_id,)
    )
    companies = cursor.fetchall()

    _, comp_limit, _ = acting_context()
    if comp_limit is not None:
        companies = [c for c in companies if c["SPONSORCOMP_ID"] == comp_limit]

    return companies


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
        WHERE d.USER_ID = %s AND b.SPONSORCOMP_ID = %s AND b.IS_ACTIVE = 1
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


def get_driver_id(user_id):
    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password= DB_PASSWORD,
                database= DB_NAME
        )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DRIVER_ID FROM DRIVER WHERE USER_ID = %s", (user_id,))
    row = cursor.fetchone()
    return row["DRIVER_ID"] if row else None


def get_cart_item_ids(driver_id, comp_id):
    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ITEM_ID FROM CART_ITEM
        WHERE DRIVER_ID = %s AND SPONSORCOMP_ID = %s
        ORDER BY ADDED_AT
        """,
        (driver_id, comp_id)
    )
    return [row["ITEM_ID"] for row in cursor.fetchall()]


def get_points_per_dollar(comp_id):
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT SPONSORCOMP_DOLLAR, SPONSORCOMP_POINT
            FROM SPONSORCOMP
            WHERE SPONSORCOMP_ID = %s
            """,
            (comp_id,)
        )
        row = cursor.fetchone()
        if row and row["SPONSORCOMP_DOLLAR"] and row["SPONSORCOMP_POINT"]:
            return float(row["SPONSORCOMP_POINT"]) / float(row["SPONSORCOMP_DOLLAR"])
        return 1.0      # fall back to 1 point per dollar if the rate isn't set
    finally:
        conn.close()


def acting_context():
    """
    Returns (driver_user_id, sponsor_comp_id, is_acting).
    - Driver:                 (own user_id, None, False)
    - Sponsor in control:     (driver's user_id, sponsor's company id, True)
    - Admin in control:       (driver's user_id, None, True)   # admins aren't limited to one company
    Cached per request so it only hits the database once.
    """
    if hasattr(g, "acting_ctx"):
        return g.acting_ctx

    user_id = session.get("user_id")
    role = session.get("role")
    controlled = session.get("view_as_driver_id")
    ctx = (user_id, None, False)

    if user_id is not None and controlled is not None and role in ("Sponsor", "Admin"):
        conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password= DB_PASSWORD,
                database= DB_NAME
        )
        try:
            cursor = conn.cursor(dictionary=True)
            if role == "Sponsor":
                cursor.execute("""
                    SELECT d.USER_ID, s.SPONSORCOMP_ID
                    FROM DRIVER d
                    JOIN BALANCE b ON b.DRIVER_ID = d.DRIVER_ID
                    JOIN SPONSOR s ON s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                    WHERE d.DRIVER_ID = %s AND s.USER_ID = %s AND b.IS_ACTIVE = 1
                    LIMIT 1
                    """,
                    (controlled, user_id)
                )
            else:
                cursor.execute(
                    "SELECT USER_ID, NULL AS SPONSORCOMP_ID FROM DRIVER WHERE DRIVER_ID = %s",
                    (controlled,)
                )
            row = cursor.fetchone()
        finally:
            conn.close()
        if row:
            ctx = (row["USER_ID"], row["SPONSORCOMP_ID"], True)

    g.acting_ctx = ctx
    return ctx

def acting_driver_user_id():
    return acting_context()[0]


def get_catalog_mode(comp_id):
    conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT CATALOG_MODE FROM SPONSORCOMP WHERE SPONSORCOMP_ID = %s", (comp_id,)
        )
        row = cursor.fetchone()
        return "selection" if row and row["CATALOG_MODE"] == "selection" else "query"
    finally:
        conn.close()


def get_approved_item_ids(comp_id):
    conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ITEM_ID FROM SPONSOR_APPROVED_ITEM
            WHERE SPONSORCOMP_ID = %s
            ORDER BY ADDED_AT, APPROVED_ID
            """,
            (comp_id,)
        )
        return [row["ITEM_ID"] for row in cursor.fetchall()]
    finally:
        conn.close()


def get_item_details_cached(item_id, access_token):
    now = time.time()
    hit = _ITEM_CACHE.get(item_id)
    if hit and now - hit[0] < ITEM_CACHE_SECONDS:
        return hit[1]
    details = get_item_details(item_id, access_token)
    if details:
        _ITEM_CACHE[item_id] = (now, details)
    return details


def load_selection_items(comp_id, balance, rate, sort, page, per_page):
    """Approved items the driver can afford, sorted and paginated. Returns (items, total, error)."""
    item_ids = get_approved_item_ids(comp_id)
    if not item_ids:
        return [], 0, None

    token = get_access_token()
    if not token:
        return [], 0, "Could not reach eBay. Please try again shortly."

    with ThreadPoolExecutor(max_workers=10) as pool:
        details_list = list(pool.map(lambda i: get_item_details_cached(i, token), item_ids))

    items = []
    for d in details_list:
        price = (d or {}).get("price")
        if not price or price.get("currency") != "USD":
            continue                                   # listing ended or unusable

        points = math.ceil(float(price["value"]) * rate)
        if points > balance:
            continue                                   # driver can't afford it

        avail = (d.get("estimatedAvailabilities") or [None])[0]
        item = dict(d)                                 # same shape the template already uses
        item["points"] = points
        item["availability"] = availability_text(avail)
        item["description"] = clean_description(d)
        items.append(item)

    if sort == "low":
        items.sort(key=lambda i: i["points"])
    elif sort == "high":
        items.sort(key=lambda i: i["points"], reverse=True)

    start = (page - 1) * per_page
    return items[start:start + per_page], len(items), None


@cat.route("/catalog", methods=["GET", "POST"])
def catalog():
    items, error, total = [], None, 0

    user_id = acting_driver_user_id()

    source = request.form if request.method == "POST" else request.args
    page = 1 if request.method == "POST" else source.get("page", 1)
    query = source.get("query", "").strip()

    sort = source.get("sort", "default")
    if sort not in ("default", "low", "high"):
        sort = "default"

    try:
        per_page = int(source.get("per_page", 10))
    except ValueError:
        per_page = 10
    if per_page not in (10, 25, 50):
        per_page = 10

    try:
        page = max(1, int(page))
    except ValueError:
        page = 1

    companies = get_driver_companies(user_id)
    valid_ids = {c["SPONSORCOMP_ID"] for c in companies}

    comp_id = None
    allowed_terms, balance, rate = [], 0.0, 1.0
    mode = "query"

    if not companies:
        error = "You aren't assigned to any sponsor company yet."
        query = ""
    else:
        try:
            comp_id = int(source.get("comp_id", ""))
        except ValueError:
            comp_id = None
        if comp_id not in valid_ids:
            comp_id = companies[0]["SPONSORCOMP_ID"]

        mode = get_catalog_mode(comp_id)
        balance = get_user_balance(user_id, comp_id)
        rate = get_points_per_dollar(comp_id)

        if mode == "query":
            allowed_terms = get_allowed_terms(user_id, comp_id)
            if query and query.lower() not in allowed_terms:
                error = "That search isn't approved by this sponsor."
                query = ""
        else:
            query = ""          # no searching in selection mode
            items, total, error = load_selection_items(
                comp_id, balance, rate, sort, page, per_page
            )

    # Query mode only: search eBay
    if query:
        offset = (page - 1) * per_page
        data, error = search_ebay(
            query,
            limit=per_page,
            offset=offset,
            max_price=balance / rate,
            sort=SORT_OPTIONS.get(sort)
        )
        if data:
            items = data.get("itemSummaries", [])
            total = int(data.get("total", 0))
            for item in items:
                price = item.get("price")
                if price:
                    item["points"] = math.ceil(float(price["value"]) * rate)

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        "catalog.html",
        items=items, error=error, query=query,
        per_page=per_page, page=page, total=total, total_pages=total_pages,
        companies=companies, comp_id=comp_id,
        allowed_terms=allowed_terms, balance=balance,
        sort=sort, mode=mode
    )

SPONSOR_SEARCH_PER_PAGE = 12
@cat.route("/catalog-items", methods=["GET", "POST"])
def sponsor_catalog_items():
    user_id = session.get("user_id")
    sponsor_id, comp_id = get_sponsor_info(user_id)
    if not sponsor_id:
        abort(403)                    # only users with a SPONSOR row get past here

    mode = get_catalog_mode(comp_id)

    # ---------- changes (POST) ----------
    if request.method == "POST":
        action = request.form.get("action", "")
        q = request.form.get("q", "").strip()
        page = request.form.get("page", "1")

        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        try:
            cursor = conn.cursor()

            if action == "set_mode":
                new_mode = request.form.get("mode")
                if new_mode in ("query", "selection"):
                    cursor.execute(
                        "UPDATE SPONSORCOMP SET CATALOG_MODE = %s WHERE SPONSORCOMP_ID = %s",
                        (new_mode, comp_id)
                    )
                    conn.commit()
                    flash(f"Catalog mode changed to {new_mode} mode.", "success")
                else:
                    flash("Choose a valid catalog mode.", "error")

            elif action == "add" and mode == "query":
                term = request.form.get("term", "").strip().lower()
                if not term or len(term) > 100:
                    flash("Enter a term up to 100 characters.", "error")
                else:
                    cursor.execute("""
                        INSERT IGNORE INTO SPONSORORDERS
                            (`QUERY`, SPONSORCOMP_ID, USER_ID, SPONSOR_ID)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (term, comp_id, user_id, sponsor_id)
                    )
                    conn.commit()

            elif action == "delete" and mode == "query":
                term = request.form.get("term", "").strip().lower()
                cursor.execute(
                    "DELETE FROM SPONSORORDERS WHERE SPONSORCOMP_ID = %s AND `QUERY` = %s",
                    (comp_id, term)
                )
                conn.commit()

            elif action in ("approve", "unapprove") and mode == "selection":
                item_id = request.form.get("item_id", "").strip()
                if not re.fullmatch(r"v1\|\d+\|\d+", item_id):
                    flash("That isn't a valid item.", "error")
                elif action == "approve":
                    cursor.execute("""
                        INSERT IGNORE INTO SPONSOR_APPROVED_ITEM
                            (SPONSORCOMP_ID, ITEM_ID, USER_ID, SPONSOR_ID)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (comp_id, item_id, user_id, sponsor_id)
                    )
                    conn.commit()
                else:
                    cursor.execute(
                        "DELETE FROM SPONSOR_APPROVED_ITEM WHERE SPONSORCOMP_ID = %s AND ITEM_ID = %s",
                        (comp_id, item_id)
                    )
                    conn.commit()

            else:
                flash("That action isn't available in the current catalog mode.", "error")

        finally:
            conn.close()

        # Redirect so a refresh doesn't resubmit, and keep the sponsor on the same search page
        return redirect(url_for("cat.sponsor_catalog_items", q=q, page=page))

    # ---------- display (GET) ----------
    q = request.args.get("q", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1

    error, terms, approved_items, search_items, total = None, [], [], [], 0

    if mode == "query":
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT `QUERY` FROM SPONSORORDERS WHERE SPONSORCOMP_ID = %s ORDER BY `QUERY`",
                (comp_id,)
            )
            terms = [row["QUERY"] for row in cursor.fetchall()]
        finally:
            conn.close()

    else:
        rate = get_points_per_dollar(comp_id)
        approved_ids = get_approved_item_ids(comp_id)
        approved_set = set(approved_ids)
        token = get_access_token()

        # The items drivers can currently buy
        if approved_ids and token:
            with ThreadPoolExecutor(max_workers=10) as pool:
                details = list(pool.map(lambda i: get_item_details_cached(i, token), approved_ids))
        else:
            details = [None] * len(approved_ids)

        for item_id, d in zip(approved_ids, details):
            d = d or {}
            price = d.get("price")
            approved_items.append({
                "item_id": item_id,
                "title": d.get("title", "Listing no longer available"),
                "image": (d.get("image") or {}).get("imageUrl"),
                "url": d.get("itemWebUrl"),
                "points": math.ceil(float(price["value"]) * rate) if price else None,
            })

        # The sponsor's eBay search
        if q:
            data, error = search_ebay(
                q,
                limit=SPONSOR_SEARCH_PER_PAGE,
                offset=(page - 1) * SPONSOR_SEARCH_PER_PAGE,
                enrich=False
            )
            if data:
                search_items = data.get("itemSummaries", [])
                total = int(data.get("total", 0))
                for it in search_items:
                    price = it.get("price")
                    if price:
                        it["points"] = math.ceil(float(price["value"]) * rate)
                    it["approved"] = it["itemId"] in approved_set

    total_pages = max(1, math.ceil(total / SPONSOR_SEARCH_PER_PAGE))

    return render_template(
        "sponsor_catalog_terms.html",
        mode=mode, terms=terms, approved_items=approved_items,
        search_items=search_items, q=q, page=page,
        total=total, total_pages=total_pages, error=error
    )

@cat.route("/cart/add", methods=["POST"])
def cart_add():
    user_id = acting_driver_user_id()

    driver_id = get_driver_id(user_id)
    item_id = request.form.get("item_id", "").strip()

    comp_id = int(request.form.get("comp_id", ""))

    valid_ids = {c["SPONSORCOMP_ID"] for c in get_driver_companies(user_id)}
    if not driver_id or comp_id not in valid_ids or not item_id or len(item_id) > 100:
        abort(400)

    if get_catalog_mode(comp_id) == "selection" and item_id not in get_approved_item_ids(comp_id):
        flash("That item isn't available from this sponsor.", "error")
        return redirect(url_for("cat.catalog", comp_id=comp_id))

    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO CART_ITEM (USER_ID, DRIVER_ID, SPONSORCOMP_ID, ITEM_ID)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, driver_id, comp_id, item_id)
    )
    conn.commit()

    # not sure if flash is working
    flash("Added to cart.")
    # send them back to the same search results page
    return redirect(url_for(
        "cat.catalog",
        query=request.form.get("query", ""),
        per_page=request.form.get("per_page", 10),
        page=request.form.get("page", 1),
        comp_id=comp_id,
        sort=request.form.get("sort", "default")
    ))


@cat.route("/cart/remove", methods=["POST"])
def cart_remove():
    user_id = acting_driver_user_id()

    driver_id = get_driver_id(user_id)
    item_id = request.form.get("item_id", "").strip()

    comp_id = int(request.form.get("comp_id", ""))

    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
    )
        
    cursor = conn.cursor()
    # scoped to this driver, so nobody can delete someone else's cart rows
    cursor.execute("""
        DELETE FROM CART_ITEM
        WHERE DRIVER_ID = %s AND SPONSORCOMP_ID = %s AND ITEM_ID = %s
        """,
        (driver_id, comp_id, item_id)
    )
    conn.commit()

    return redirect(url_for("cat.cart", comp_id=comp_id))


@cat.route("/cart")
def cart():
    user_id = acting_driver_user_id()

    driver_id = get_driver_id(user_id)
    companies = get_driver_companies(user_id)
    valid_ids = {c["SPONSORCOMP_ID"] for c in companies}

    cart_items, total, balance, rate = [], 0.0, 0.0, 1.0
    comp_id, error = None, None

    if not driver_id or not companies:
        error = "You aren't assigned to any sponsor company yet."
    else:
        try:
            comp_id = int(request.args.get("comp_id", ""))
        except ValueError:
            comp_id = None
        if comp_id not in valid_ids:
            comp_id = companies[0]["SPONSORCOMP_ID"]

        balance = get_user_balance(user_id, comp_id)
        rate = get_points_per_dollar(comp_id)
        item_ids = get_cart_item_ids(driver_id, comp_id)

        token = get_access_token() if item_ids else None
        if item_ids and not token:
            error = "Couldn't reach eBay to load prices. Please try again shortly."

        # one getItem call per cart item, in parallel
        with ThreadPoolExecutor(max_workers=10) as pool:
            details_list = list(pool.map(
                lambda i: get_item_details(i, token) if token else None,
                item_ids
            ))

        for item_id, d in zip(item_ids, details_list):
            d = d or {}
            price = d.get("price")
            cart_items.append({
                "item_id": item_id,
                "title": d.get("title", "Item unavailable"),
                "image": (d.get("image") or {}).get("imageUrl"),
                "url": d.get("itemWebUrl"),
                "points": math.ceil(float(price["value"]) * rate) if price else None,
            })

        total = sum(i["points"] for i in cart_items if i["points"] is not None)

    has_unavailable = any(i["points"] is None for i in cart_items)

    return render_template(
        "cart.html",
        cart_items=cart_items, 
        total=total, 
        balance=balance,
        remaining=balance - total, 
        over_budget=total > balance,
        companies=companies, 
        comp_id=comp_id, 
        error=error,
        has_unavailable=has_unavailable
    )


@cat.route("/cart/checkout", methods=["POST"])
def cart_checkout():
    user_id = acting_driver_user_id()
    actor_id = session.get("user_id")

    if not user_id:
        abort(403)

    driver_id = get_driver_id(user_id)
    try:
        comp_id = int(request.form.get("comp_id", ""))
    except ValueError:
        abort(400)

    valid_ids = {c["SPONSORCOMP_ID"] for c in get_driver_companies(user_id)}
    if not driver_id or comp_id not in valid_ids:
        abort(400)

    cart_url = url_for("cat.cart", comp_id=comp_id)

    # Price everything from live eBay data (before taking the DB lock)
    item_ids = get_cart_item_ids(driver_id, comp_id)
    if not item_ids:
        flash("Your cart is empty.", "error")
        return redirect(cart_url)

    token = get_access_token()
    if not token:
        flash("Couldn't reach eBay to confirm prices. Please try again shortly.", "error")
        return redirect(cart_url)

    with ThreadPoolExecutor(max_workers=10) as pool:
        details_list = list(pool.map(lambda i: get_item_details(i, token), item_ids))

    rate = get_points_per_dollar(comp_id)
    lines = []
    for item_id, d in zip(item_ids, details_list):
        d = d or {}
        price = d.get("price")
        avail = (d.get("estimatedAvailabilities") or [{}])[0]

        if (not price or price.get("currency") != "USD"
                or avail.get("estimatedAvailabilityStatus") == "OUT_OF_STOCK"):
            flash("One or more items in your cart are no longer available. "
                  "Remove them and try again.", "error")
            return redirect(cart_url)

        lines.append({
            "item_id": item_id,                                   # used only to clear the cart
            "title": d.get("title", "")[:255],                    # -> ITEM_NAME
            "desc": clean_description(d, max_length=250),         # -> ITEM_DESC
            "points": math.ceil(float(price["value"]) * rate),    # -> ITEM_PRICE
        })

    total = sum(l["points"] for l in lines)

    # Reject if the price changed since the driver last looked at the cart
    try:
        expected = int(float(request.form.get("expected_total", "")))
    except ValueError:
        expected = None
    if expected != total:
        flash("Prices changed since you last viewed your cart. "
              "Please review the new total.", "error")
        return redirect(cart_url)

    # Do the purchase as one transaction 
    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password= DB_PASSWORD,
                database= DB_NAME
        )
    cursor = conn.cursor(dictionary=True)
    try:
        # Lock this driver's balance row so two purchases can't spend the same points
        cursor.execute("""
            SELECT BALANCE_ID, BALANCE
            FROM BALANCE
            WHERE DRIVER_ID = %s AND SPONSORCOMP_ID = %s AND IS_ACTIVE = 1
            FOR UPDATE
            """,
            (driver_id, comp_id)
        )
        bal = cursor.fetchone()

        if not bal:
            conn.rollback()
            flash("No active balance was found for this sponsor.", "error")
            return redirect(cart_url)

        balance = float(bal["BALANCE"] or 0)
        if total > balance:
            conn.rollback()
            flash(f"Not enough points: your cart costs {total} and you have {balance:g}.", "error")
            return redirect(cart_url)

        # Remove from cart first. If a duplicate request already bought these,
        # nothing gets deleted and we stop instead of charging twice.
        for l in lines:
            cursor.execute("""
                DELETE FROM CART_ITEM
                WHERE DRIVER_ID = %s AND SPONSORCOMP_ID = %s AND ITEM_ID = %s
                """,
                (driver_id, comp_id, l["item_id"])
            )
            if cursor.rowcount != 1:
                conn.rollback()
                flash("Your cart changed while checking out. Please review it and try again.", "error")
                return redirect(cart_url)

        # Order header
        cursor.execute("""
            INSERT INTO ORDERS
                (USER_ID, DRIVER_ID, SPONSORCOMP_ID, ORDER_DTS, POINT_TOTAL, ORDER_STATUS)
            VALUES (%s, %s, %s, NOW(), %s, 'Active')
            """,
            (user_id, driver_id, comp_id, total)
        )
        order_id = cursor.lastrowid

        # Order lines (quantity is always 1 per cart item)
        cursor.executemany("""
            INSERT INTO ITEMIZEDORDER
                (ORDER_ID, ITEM_NAME, ITEM_DESC, ITEM_AMOUNT, ITEM_PRICE)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [(order_id, l["title"], l["desc"], 1, l["points"]) for l in lines]
        )

        # Deduct the points
        cursor.execute(
            "UPDATE BALANCE SET BALANCE = BALANCE - %s WHERE BALANCE_ID = %s",
            (total, bal["BALANCE_ID"])
        )

        # Log it like any other point change so history and audits stay complete
        reason = f"Purchase (order #{order_id})"
        if actor_id != user_id:
            reason += " placed by sponsor"

        cursor.execute("""
            INSERT INTO POINTCHANGES
                (BALANCE_ID, DRIVER_ID, POINTCHANGE_AMOUNT, POINTCHANGE_REASON, USER_ID)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (bal["BALANCE_ID"], driver_id, -total, reason, actor_id)
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    flash(f"Order #{order_id} placed! {total} points were deducted.", "success")
    return redirect(cart_url)