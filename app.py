from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector 
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from catalog import search_ebay
from datetime import date

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
global USER_ID

app = Flask(__name__, static_folder= "styles")
#FLASK_SECRET_KEY add in .env
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# THIS STOPS SOMEONE FROM LOGGIN BACK IN BY HITTING THE BACK BUTTON AFTER THEY HAVE LOGGED OUT
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get username and password values from the html form
        username = request.form.get("username")
        pwd = request.form.get("password")

        # connect to sql database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        try: 
            # get the password for the current username in the form
            cursor.execute("SELECT USER_ID, EMAIL, PASSWORD, ROLE FROM USER WHERE EMAIL = %s", (username,))
            user = cursor.fetchone()

            global USER_ID
            USER_ID= user["USER_ID"]

            # check if hashed password matches
            if (user and check_password_hash(user["PASSWORD"], pwd)) or (user and user["PASSWORD"] == pwd):
                role = user["ROLE"]
                session["user_id"] = user["USER_ID"]
                session["role"] = user["ROLE"]

                if role == "Driver":
                    return redirect(url_for("driverDash"))
                elif role == "Sponsor":
                    return redirect(url_for("sponDash"))
                elif role == "Admin":
                    return redirect(url_for("adminDash"))
                else:
                    return redirect(url_for("home"))

            # if password doesn't match stay on the page and give an error
            return render_template( "login.html", error="Invalid username or password" )
            
        finally:
            cursor.close()
            conn.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    print(session)
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # get user info to create an account
        first_name = request.form.get("first_name") 
        last_name = request.form.get("last_name") 
        email = request.form.get("email") 
        pwd = request.form.get("password")
        role = "Driver"

        # connect to sql database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        try:
            # check if email already exists 
            cursor.execute( "SELECT USER_ID FROM `USER` WHERE EMAIL = %s", (email,) )
            if cursor.fetchone(): 
                return render_template( 
                    "signup.html", 
                    error="An account with this email already exists." 
                )

            # hash the password
            hashed_password = generate_password_hash(pwd)

            cursor.execute(""" 
                INSERT INTO `USER` 
                (USER_FNAME, USER_LNAME, EMAIL, PASSWORD, ROLE) 
                VALUES (%s, %s, %s, %s, %s) """, 
                (first_name, last_name, email, hashed_password, "Driver")
            )

            conn.commit()

            return redirect(url_for("login"))

        except mysql.connector.Error: 
            conn.rollback() 
            app.logger.exception("Error creating user account") 
            return render_template( 
                "signup.html", 
                error="Unable to create your account. Please try again." 
            )
            
        finally:
            cursor.close()
            conn.close()
    return render_template("signup.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password= DB_PASSWORD,
    database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    #query gets newest row in about table
    cursor.execute("""select * from ABOUT where SPRINT_NUM 
                        = (select max(SPRINT_NUM) from ABOUT)""")
    
    data = cursor.fetchone()
    #check data in term
    #print(data)
    
    cursor.close()
    conn.close()
    return render_template("about.html", data = data)

@app.route("/driverDash")
def driverDash():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # A sponsor may view a selected driver's dashboard
    if session.get("role") in ("Sponsor","Admin"):
        driver_id = session.get("view_as_driver_id")

        if driver_id is None:
            if session.get("role") == "Sponsor":
                return redirect(url_for("sponDash"))
            else:
                return redirect(url_for("adminDash"))
        
        # Find the driver's USER_ID and confirm the sponsor owns them
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        try:
            if session.get("role") == "Sponsor":
                # Sponsors can only view drivers in their company.
                cursor.execute("""
                    SELECT d.DRIVER_ID, d.USER_ID
                    FROM DRIVER AS d
                    JOIN SPONSOR AS s
                        ON s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                    WHERE d.DRIVER_ID = %s
                      AND s.USER_ID = %s
                """, (driver_id, session["user_id"]))
            else:
                # Admins can view any existing driver.
                cursor.execute("""
                    SELECT DRIVER_ID, USER_ID
                    FROM DRIVER
                    WHERE DRIVER_ID = %s
                """, (driver_id,))

            driver = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
        if driver is None:
            session.pop("view_as_driver_id", None)
            return "Driver not found or not authorized", 403

        user_id = driver["USER_ID"]


    elif session.get("role") == "Driver":
        user_id = session["user_id"]

    else:
        return "Unauthorized", 403
    
    #new connection

    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
    cursor = conn.cursor(dictionary=True)
        #query gets driver info
    try:
        cursor.execute("""select
                        d.DRIVER_ID,
                        u.USER_ID,
                        u.USER_FNAME,
                        u.USER_LNAME,
                        u.ROLE,
                        u.EMAIL,
                        d.BALANCE
                    from DRIVER as d
                    join `USER` as u
                        on u.USER_ID = d.USER_ID
                    where d.USER_ID  = %s""", (user_id,))
        
        drive_info = cursor.fetchone()
        if drive_info is None:
            return "Driver account not found", 404
        
        #point history
        cursor.execute("""
            select
                pc.POINTCHANGE_ID,
                pc.POINTCHANGE_AMOUNT,
                pc.POINTCHANGE_REASON,
                pc.DTS
            from POINTCHANGES as pc
            where pc.USER_ID =  %s
            order by pc.DTS desc;
                """, (user_id,))

        history = cursor.fetchall()

        #order and status
        cursor.execute("""
            select 
                ORDER_ID,
                DRIVER_ID,
                POINT_TOTAL,
                ORDER_STATUS,
                ORDER_DTS
            from ORDERS
            WHERE DRIVER_ID = %s
            order by ORDER_DTS DESC;
                """, (drive_info["DRIVER_ID"],))

        order_stat = cursor.fetchall()

        cursor.close()
        conn.close()
        #print(drive_info)
        return render_template("driverDash.html", drive_info = drive_info,
                            history= history, order_stat = order_stat)
    finally: 
        cursor.close()
        conn.close()

@app.route("/catalog", methods=["GET", "POST"])
def catalog():

    items = []
    error = None
    query = ""

    if request.method == "POST":

        query = request.form.get("query", "").strip()

        if query:
            data, error = search_ebay(query)

            if data:
                items = data.get("itemSummaries", [])

    return render_template(
        "catalog.html",
        items=items,
        error=error,
        query=query
    )

@app.route("/userProfile")
def userProfile():
    user_id = USER_ID

    error = request.args.get("error")
    success = request.args.get("success")

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM USER WHERE USER_ID = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("userProfile.html", user=user,error=error,
        success=success)

@app.route("/updateFirstName", methods=["POST"])
def updateFirstName():

    user_id = session["user_id"]

    first_name = request.form["first_name"].strip()

    if not first_name:
        return redirect(url_for("userProfile", error="First name cannot be empty."))

    if not first_name.isalpha():
        return redirect(url_for("userProfile", error="First name can only contain letters."))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE USER
        SET USER_FNAME = %s
        WHERE USER_ID = %s
        """,
        (first_name, user_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("userProfile", success="First name updated successfully!"))

@app.route("/updateLastName", methods=["POST"])
def updateLastName():

    user_id = session["user_id"]

    last_name = request.form["last_name"].strip()

    if not last_name:
        return redirect(
            url_for("userProfile",error="Last name cannot be empty."))

    if not last_name.isalpha():
        return redirect(
            url_for("userProfile",error="Last name can only contain letters."))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE USER
        SET USER_LNAME = %s
        WHERE USER_ID = %s
        """,
        (last_name, user_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("userProfile",success="Last name updated successfully!"))

@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():

    user_id = USER_ID

    error = None
    success = None

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

    #get current user password hash
    cursor.execute(
        "SELECT USER_ID, PASSWORD FROM USER WHERE USER_ID = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.close()
        conn.close()
        return "User not found", 404

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        # check that all fields are entered
        if not current_password or not new_password or not confirm_password:
            error = "Please fill in all password fields."

        # verify current password against the stored hash    
        elif not check_password_hash(
            user["PASSWORD"],
            current_password
        ):
            error = "Current password is incorrect"

        # confirm the new password is a match
        elif new_password != confirm_password:
            error = "The new passwords do not match."

        # make sure the new password is different
        elif current_password == new_password:
            error = "Your new password must be different from your current password."

        else:

            #save old password hash before replacing
            old_password_hash = user["PASSWORD"]

            # generate new password hash
            new_password_hash = generate_password_hash(new_password)

            # update user table
            cursor.execute(
                "UPDATE USER SET PASSWORD = %s WHERE USER_ID = %s",
                (new_password_hash, user_id)
            )

            # record password change
            cursor.execute(
                """
                INSERT INTO PASSWORDCHANGES (
                    USER_ID,
                    PASSWORDCHANGE_REASON,
                    OLD_PASSWORD,
                    NEW_PASSWORD
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id, 
                    "User requested password change", 
                    old_password_hash, 
                    new_password_hash
                )
            )

            conn.commit()
            success = "Your password has been changed successfully."

    cursor.close()
    conn.close()
    return render_template("changePassword.html", error=error, success=success)
    
@app.route("/sponDash")
def sponDash():

    # dont allows the page to be accessed unless someone is logged in
    # if "user_id" not in session:
    #     return redirect(url_for("login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
        )
    cursor = conn.cursor(dictionary=True)

    role = session.get("role")

    # Determine which sponsor dashboard to display.
    if role == "Sponsor":
        sponsor_user_id = session["user_id"]

    elif role == "Admin":
        # Admins must select a sponsor first.
        sponsor_user_id = session.get("view_as_sponsor_id")

        if sponsor_user_id is None:
            return redirect(url_for("adminDash"))

    else:
        return "Unauthorized", 403

    if role == "Admin":
        # Find the sponsor's company and sponsor record.
        cursor.execute("""
            SELECT USER_ID, SPONSOR_ID, SPONSORCOMP_ID
            FROM SPONSOR
            WHERE SPONSOR_ID = %s
        """, (sponsor_user_id,))

        sponsor = cursor.fetchone()

        if sponsor is None:
            session.pop("view_as_sponsor_id", None)
            return "Sponsor account not found", 404
    
    # Driver information + point summary
    cursor.execute("""
        select 
            u.USER_ID,
            u.USER_FNAME,
            u.USER_LNAME,
            u.ROLE,
            u.EMAIL,

            d.DRIVER_ID,
            d.SPONSORCOMP_ID,
            d.BALANCE,

            coalesce(sum(
                case
                    when p.POINTCHANGE_AMOUNT > 0
                    then p.POINTCHANGE_AMOUNT
                    else 0
                end
            ), 0) as POINTS_GAINED,

            coalesce(sum(
                case
                    when p.POINTCHANGE_AMOUNT < 0
                    then ABS(p.POINTCHANGE_AMOUNT)
                    else 0
                end
            ), 0) as POINTS_LOST,

            coalesce(sum(p.POINTCHANGE_AMOUNT), 0) as NET_CHANGE

        from `USER` as u

        join DRIVER as d
            on u.USER_ID = d.USER_ID

        left join POINTCHANGES as p
            on p.USER_ID = d.USER_ID

        group by
            u.USER_ID,
            u.USER_FNAME,
            u.USER_LNAME,
            u.ROLE,
            u.EMAIL,
            d.DRIVER_ID,
            d.SPONSORCOMP_ID,
            d.BALANCE

        order by d.DRIVER_ID
    """)

    user_info = cursor.fetchall()
    
    # Individual point history
        # Individual point history
    # Get the selected history filter
    history_filter = request.args.get("history_filter", "all_time")

    today = date.today()
    month_start = today.replace(day=1)

    # Determine the previous calendar month's start date
    if month_start.month == 1:
        previous_month_start = date(month_start.year - 1, 12, 1)
    else:
        previous_month_start = date(
            month_start.year, month_start.month - 1, 1
        )

    # Base query: only show point changes for this sponsor's company
    history_query = """
        SELECT
            p.POINTCHANGE_ID,
            p.DRIVER_ID,
            u.USER_FNAME,
            u.USER_LNAME,
            p.POINTCHANGE_AMOUNT,
            p.POINTCHANGE_REASON,
            p.DTS
        FROM POINTCHANGES AS p
        JOIN DRIVER AS d
            ON p.DRIVER_ID = d.DRIVER_ID
        JOIN `USER` AS u
            ON d.USER_ID = u.USER_ID
        WHERE d.SPONSORCOMP_ID IN (
            SELECT s.SPONSORCOMP_ID
            FROM SPONSOR AS s
            WHERE s.USER_ID = %s
        )
    """

    params = [sponsor_user_id]

    # Apply the selected date range
    if history_filter == "current_month":
        history_query += " AND p.DTS >= %s AND p.DTS < %s"

        if month_start.month == 12:
            next_month_start = date(month_start.year + 1, 1, 1)
        else:
            next_month_start = date(
                month_start.year, month_start.month + 1, 1
            )

        params.extend([month_start, next_month_start])

    elif history_filter == "past_month":
        history_query += " AND p.DTS >= %s AND p.DTS < %s"
        params.extend([previous_month_start, month_start])

    elif history_filter != "all_time":
        history_filter = "all_time"

    history_query += " ORDER BY p.DTS DESC, p.POINTCHANGE_ID DESC"

    cursor.execute(history_query, tuple(params))
    point_history = cursor.fetchall()

    # Count pending applications for this sponsor
    cursor.execute("""
        SELECT COUNT(*) AS PENDING_APPLICATIONS
        FROM APPLICATIONS AS a
        JOIN SPONSOR AS s
            ON a.SPONSOR_ID = s.SPONSOR_ID
        WHERE s.USER_ID = %s
            AND a.STATUS = 'PENDING'
    """, (sponsor_user_id,))

    pending_applications = cursor.fetchone()["PENDING_APPLICATIONS"]

    # Points given to all drivers this month
    cursor.execute("""
        SELECT COALESCE(SUM(p.POINTCHANGE_AMOUNT), 0) AS POINTS_THIS_MONTH
        FROM SPONSOR AS s
        JOIN DRIVER AS d
            ON s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
        JOIN POINTCHANGES AS p
            ON p.USER_ID = d.USER_ID
        WHERE s.USER_ID = %s
            AND p.POINTCHANGE_AMOUNT > 0
            AND p.DTS >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
            AND p.DTS < DATE_ADD(
                DATE_FORMAT(CURDATE(), '%Y-%m-01'),
                INTERVAL 1 MONTH
            )
    """, (sponsor_user_id,))

    points_this_month = cursor.fetchone()["POINTS_THIS_MONTH"]


    cursor.close()
    conn.close()
    return render_template(
        "sponsorDash.html",
        user_info=user_info,
        point_history=point_history, 
        history_filter=history_filter,
        pending_applications=pending_applications,
        points_this_month=points_this_month
    )

@app.route("/assignPoints", methods=["GET", "POST"])
def assignPoints():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if session.get("role") != "Sponsor":
        return "Unauthorized", 403

    sponsor_user_id = session["user_id"]
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":

            # handle the bulk changes for all drivers
            bulk_action = request.form.get("bulk_action")

            if bulk_action in ("add_all", "subtract_all"):
                try:
                    bulk_amount = int(request.form.get("bulk_amount", ""))
                except (TypeError, ValueError):
                    flash("Enter a valid whole-number point amount.", "error")
                    return redirect(url_for("assignPoints"))

                bulk_reason = request.form.get("bulk_reason", "").strip()

                if bulk_amount <= 0:
                    flash("The point amount must be greater than zero.", "error")
                    return redirect(url_for("assignPoints"))

                if not bulk_reason:
                    flash("Please enter a reason for the point change.", "error")
                    return redirect(url_for("assignPoints"))

                # negative amount means points are being subtracted
                signed_amount = (
                    bulk_amount if bulk_action == "add_all" 
                    else -bulk_amount
                )

                # lock sponsor company's driver balances before checking
                cursor.execute("""
                    SELECT d.DRIVER_ID, d.BALANCE
                    FROM DRIVER AS d
                    WHERE EXISTS (
                        SELECT 1
                        FROM SPONSOR AS s
                        WHERE s.USER_ID = %s
                            AND s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                    )
                    FOR UPDATE
                    """, 
                    (sponsor_user_id,)
                )
                company_drivers = cursor.fetchall()

                if not company_drivers:
                    conn.rollback()
                    flash("There are no drivers to update.", "error")
                    return redirect(url_for("assignPoints"))

                # reject the whole subtraction is any driver would go negative
                if bulk_action == "subtract_all":
                    drivers_without_enough_points = [
                        driver for driver in company_drivers
                        if float(driver["BALANCE"] or 0) < bulk_amount
                    ]

                    if drivers_without_enough_points:
                        conn.rollback()
                        flash("Bulk subtraction cancelled: at least one driver does not have enough points. No balances were changes.", "error")
                        return redirect(url_for("assignPoints"))

                # update all drivers belonging to the sponsor's company
                cursor.execute("""
                    UPDATE DRIVER AS d
                    SET BALANCE = BALANCE + %s
                    WHERE EXISTS (
                        SELECT 1
                        FROM SPONSOR AS s
                        WHERE s.USER_ID = %s
                            AND s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                    )
                    """,
                    (signed_amount, sponsor_user_id)
                )

                # record the change separately for each affected driver
                cursor.execute("""
                    INSERT INTO POINTCHANGES
                        (DRIVER_ID, POINTCHANGE_AMOUNT, POINTCHANGE_REASON, USER_ID)
                    SELECT 
                        d.DRIVER_ID, %s, %s, s.USER_ID
                    FROM DRIVER AS d
                    JOIN SPONSOR AS s
                        ON s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                    WHERE s.USER_ID = %s
                    """,
                    (signed_amount, bulk_reason, sponsor_user_id)
                )

                conn.commit()

                operation = (
                    "added to" if bulk_action == "add_all" 
                    else "subtracted from"
                )
                flash(
                    f"{bulk_amount} points successfully {operation} "
                    f"all {len(company_drivers)} drivers.",
                    "success"
                )
                return redirect(url_for("assignPoints"))

            driver_id_raw = request.form.get("driver_id", "")
            action = request.form.get("action", "")
            amount_raw = request.form.get("amount", "")
            reason = request.form.get("reason", "").strip()

            # validate the form before making database changes
            try:
                driver_id = int(driver_id_raw)
                amount = int(amount_raw)
            except (TypeError, ValueError):
                flash("Enter a valid driver and a whole-number point amount.", "error")
                return redirect(url_for("assignPoints"))

            if amount <= 0:
                flash("The point amount must be greater than zero.", "error")
                return redirect(url_for("assignPoints"))
            
            if action not in ("add", "subtract"):
                flash("Choose whether to add or subtract points.", "error")
                return redirect(url_for("assignPoints"))

            if not reason:
                flash("Please enter a reason for the point change.", "error")
                return redirect(url_for("assignPoints"))

            # lock the driver's balance while checking and updating it
            # condition to ensure the sponsor owns the driver
            cursor.execute("""
                SELECT d.DRIVER_ID, d.BALANCE
                FROM DRIVER AS d
                WHERE d.DRIVER_ID = %s
                    AND EXISTS (
                        SELECT 1
                        FROM SPONSOR AS s
                        WHERE s.USER_ID = %s
                            AND s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                    )
                FOR UPDATE
                """, 
                (driver_id, sponsor_user_id),
            )
            driver = cursor.fetchone()

            if driver is None:
                conn.rollback()
                flash("That driver was not found or is not assigned to your company.", "error")
                return redirect(url_for("assignPoints"))

            current_balance = float(driver["BALANCE"] or 0)
            signed_amount = amount if action == "add" else -amount
            new_balance = current_balance + signed_amount

            if new_balance < 0:
                conn.rollback()
                flash(f"This driver only has {current_balance:g} points. You cannot subtract {amount} points.", "error")
                return redirect(url_for("assignPoints"))

            cursor.execute(
                "UPDATE DRIVER SET BALANCE = %s WHERE DRIVER_ID = %s",
                (new_balance, driver_id),
            )
            cursor.execute("""
                INSERT INTO POINTCHANGES
                (DRIVER_ID, POINTCHANGE_AMOUNT, POINTCHANGE_REASON, USER_ID)
                VALUES (%s, %s, %s, %s)
                """,
                (driver_id, signed_amount, reason, sponsor_user_id),
            )
            conn.commit()
            flash(
                f"Successfully {'added' if action == 'add' else 'subtracted'} {amount} points.",
                "success",
            )
            return redirect(url_for("assignPoints"))

        # list only drivers belonging to one of the logged-in sponsor's companies
        cursor.execute("""
            SELECT
                d.DRIVER_ID,
                d.USER_ID,
                d.BALANCE,
                d.SPONSORCOMP_ID,
                u.USER_FNAME,
                u.USER_LNAME,
                u.EMAIL,
                latest.POINTCHANGE_AMOUNT AS LAST_CHANGE_AMOUNT,
                latest.POINTCHANGE_REASON AS LAST_CHANGE_REASON,
                latest.DTS AS LAST_CHANGE_DTS
            FROM DRIVER AS d
            JOIN `USER` AS u ON u.USER_ID = d.USER_ID
            LEFT JOIN POINTCHANGES AS latest
                ON latest.POINTCHANGE_ID = (
                    SELECT p.POINTCHANGE_ID
                    FROM POINTCHANGES AS p
                    WHERE p.DRIVER_ID = d.DRIVER_ID
                    ORDER BY p.DTS DESC, p.POINTCHANGE_ID DESC
                    LIMIT 1
                )
            WHERE EXISTS (
                SELECT 1
                FROM SPONSOR AS s
                WHERE s.USER_ID = %s
                    AND s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
            )
            ORDER BY u.USER_LNAME, u.USER_FNAME, d.DRIVER_ID
            """,
            (sponsor_user_id,),
        )
        drivers = cursor.fetchall()

        cursor.execute("""
            SELECT
                p.POINTCHANGE_ID,
                p.DRIVER_ID,
                p.POINTCHANGE_AMOUNT,
                p.POINTCHANGE_REASON,
                p.DTS
            FROM POINTCHANGES AS p
            JOIN DRIVER AS d ON d.DRIVER_ID = p.DRIVER_ID
            WHERE EXISTS (
                SELECT 1
                FROM SPONSOR AS s
                WHERE s.USER_ID = %s
                    AND s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
            )
            ORDER BY p.DTS DESC, p.POINTCHANGE_ID DESC
            """,
            (sponsor_user_id,),
        )
        history_rows = cursor.fetchall()

        history_by_driver = {}
        for change in history_rows:
            history_by_driver.setdefault(change["DRIVER_ID"], []).append(change)

        return render_template(
            "assignPoints.html",
            drivers=drivers,
            history_by_driver=history_by_driver,
        )
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

@app.route("/adminDash")
def adminDash():

    # dont allows the page to be accessed unless someone is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

    user_id = session["user_id"]
    cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (user_id,)
        )
        
    user = cursor.fetchone()
    
    if not user or user['ROLE'] != 'Admin':
        return redirect(url_for('login'))

    # Get sponsor comps
    cursor.execute("""
        SELECT *
        FROM SPONSORCOMP
        ORDER BY SPONSORCOMP_NAME
    """)

    sponsor_companies = cursor.fetchall()

    # Get drivers
    cursor.execute("""
        SELECT
            D.DRIVER_ID,
            U.USER_ID,
            U.USER_FNAME,
            U.USER_LNAME,
            U.EMAIL,
            U.ROLE,
            D.BALANCE,
            SC.SPONSORCOMP_ID,
            SC.SPONSORCOMP_NAME
        FROM DRIVER D
        INNER JOIN USER U
            ON D.USER_ID = U.USER_ID
        INNER JOIN SPONSORCOMP SC
            ON D.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
        ORDER BY U.USER_LNAME, U.USER_FNAME
    """)

    drivers = cursor.fetchall()

    # Get sponsors
    cursor.execute("""
        SELECT
            S.SPONSOR_ID,
            U.USER_ID,
            U.USER_FNAME,
            U.USER_LNAME,
            U.EMAIL,
            U.ROLE,
            SC.SPONSORCOMP_ID,
            SC.SPONSORCOMP_NAME,
            COALESCE(PC.POINTS_AWARDED, 0) AS POINTS_AWARDED
        FROM SPONSOR S
        INNER JOIN USER U
            ON S.USER_ID = U.USER_ID
        INNER JOIN SPONSORCOMP SC
            ON S.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
        LEFT JOIN ( 
            SELECT
                USER_ID, 
                SUM( 
                    CASE 
                        WHEN POINTCHANGE_AMOUNT > 0 
                        THEN POINTCHANGE_AMOUNT 
                        ELSE 0 
                    END 
                ) AS POINTS_AWARDED 
            FROM POINTCHANGES 
            GROUP BY USER_ID 
        ) PC ON PC.USER_ID = U.USER_ID
        ORDER BY U.USER_LNAME, U.USER_FNAME
    """)

    sponsors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "adminDash.html",
        drivers=drivers,
        sponsors=sponsors,
        sponsor_companies=sponsor_companies
    )

@app.route("/adminDash/sponsors")
def adminSponsors():
    if "user_id" not in session:
            return redirect(url_for("login"))
    
    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = conn.cursor(dictionary=True)

    user_id = session["user_id"]
    cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (user_id,)
        )
    
    user = cursor.fetchone()

    if not user or user['ROLE'] != 'Admin':
        return redirect(url_for('login'))

    cursor.execute("""
            SELECT
                S.SPONSOR_ID,
                U.USER_ID,
                U.USER_FNAME,
                U.USER_LNAME,
                U.EMAIL,
                SC.SPONSORCOMP_ID,
                SC.SPONSORCOMP_NAME,
                COALESCE(PC.POINTS_AWARDED, 0) AS POINTS_AWARDED
            FROM SPONSOR S
            JOIN USER U
                ON S.USER_ID = U.USER_ID
            JOIN SPONSORCOMP SC
                ON S.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
            LEFT JOIN (
                SELECT
                    USER_ID,
                    SUM(
                        CASE
                            WHEN POINTCHANGE_AMOUNT > 0
                            THEN POINTCHANGE_AMOUNT
                            ELSE 0
                        END
                    ) AS POINTS_AWARDED
                FROM POINTCHANGES
                GROUP BY USER_ID
            ) PC
                ON PC.USER_ID = U.USER_ID
            ORDER BY U.USER_LNAME, U.USER_FNAME
        """)
    sponsors = cursor.fetchall()
    
    cursor.execute("""
            SELECT *
            FROM SPONSORCOMP
            ORDER BY SPONSORCOMP_NAME
        """)
    sponsor_companies = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
            "adminSponsors.html",
            sponsors=sponsors,
            sponsor_companies=sponsor_companies
        )


@app.route("/adminDash/drivers")
def adminDrivers():

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
        )
    cursor = conn.cursor(dictionary=True)

    user_id = session["user_id"]
    cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (user_id,)
        )
        
    user = cursor.fetchone()
    
    if not user or user['ROLE'] != 'Admin':
        return redirect(url_for('login'))
    
    # Get sponsor comps
    cursor.execute("""
        SELECT *
            FROM SPONSORCOMP
            ORDER BY SPONSORCOMP_NAME
        """)
    sponsor_companies = cursor.fetchall()
    
    # Get drivers
    cursor.execute("""
            SELECT
                D.DRIVER_ID,
                U.USER_ID,
                U.USER_FNAME,
                U.USER_LNAME,
                U.EMAIL,
                U.ROLE,
                D.BALANCE,
                SC.SPONSORCOMP_ID,
                SC.SPONSORCOMP_NAME
            FROM DRIVER D
            INNER JOIN USER U
                ON D.USER_ID = U.USER_ID
            INNER JOIN SPONSORCOMP SC
                ON D.SPONSORCOMP_ID = SC.SPONSORCOMP_ID
            ORDER BY U.USER_LNAME, U.USER_FNAME
        """)
    
    drivers = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template(
        'adminDrivers.html',
        drivers=drivers,
        sponsor_companies=sponsor_companies
    )


@app.route("/adminDash/reports")
def adminReports():

    if "user_id" not in session:
            return redirect(url_for("login"))

    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
    cursor = conn.cursor(dictionary=True)
    
    
    user_id = session["user_id"]
    cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (user_id,)
        )
        
    user = cursor.fetchone()

    if not user or user['ROLE'] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template("adminReports.html")

@app.route("/adminDash/audit")
def adminAudit():

    if "user_id" not in session:
            return redirect(url_for("login"))

    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
    cursor = conn.cursor(dictionary=True)
    
    
    user_id = session["user_id"]
    cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (user_id,)
        )
        
    user = cursor.fetchone()

    if not user or user['ROLE'] != 'Admin':
        return redirect(url_for('login'))
    
    return render_template("adminAudit.html")

@app.route("/viewAsDriver/<int:driver_id>", methods=["POST"])
def viewAsDriver(driver_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") not in ("Sponsor", "Admin"):
        return "Unauthorized", 403

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        if session.get("role") == "Sponsor":
            # Sponsors can only view drivers in their company.
            cursor.execute("""
                SELECT d.DRIVER_ID
                FROM DRIVER AS d
                JOIN SPONSOR AS s
                    ON s.SPONSORCOMP_ID = d.SPONSORCOMP_ID
                WHERE d.DRIVER_ID = %s
                  AND s.USER_ID = %s
            """, (driver_id, session["user_id"]))
        else:
            # Admins can view any existing driver.
            cursor.execute("""
                SELECT DRIVER_ID
                FROM DRIVER
                WHERE DRIVER_ID = %s
            """, (driver_id,))

        driver = cursor.fetchone()

        if driver is None:
            return "Driver not found or not authorized", 403

        # save the driver being viewed without changing sponsor login
        session["view_as_driver_id"] = driver_id

        return redirect(url_for("driverDash"))

    finally:
        cursor.close()
        conn.close()


@app.route("/stopViewingAsDriver", methods=["POST"])
def stopViewingAsDriver():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") not in ("Sponsor", "Admin"):
        return "Unauthorized", 403

    # Return the sponsor view
    session.pop("view_as_driver_id", None)

    if session.get("role") == "Admin":
        return redirect(url_for("adminDash"))

    return redirect(url_for("sponDash"))

@app.route("/viewAsSponsor/<int:sponsor_id>", methods=["POST"])
def viewAsSponsor(sponsor_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") not in ("Admin"):
        return "Unauthorized", 403

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT SPONSOR_ID
            FROM SPONSOR
            WHERE SPONSOR_ID = %s
            """, (sponsor_id,))

        sponsor = cursor.fetchone()

        if sponsor is None:
            return "Sponsor not found or not authorized", 403

        # save the sponsor being viewed without changing sponsor login
        session["view_as_sponsor_id"] = sponsor_id

        return redirect(url_for("sponDash"))

    finally:
        cursor.close()
        conn.close()


@app.route("/stopViewingAsSponsor", methods=["POST"])
def stopViewingAsSponsor():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") not in ("Admin"):
        return "Unauthorized", 403

    # Return the sponsor view
    session.pop("view_as_sponsor_id", None)

    if session.get("role") == "Admin":
        return redirect(url_for("adminDash"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)