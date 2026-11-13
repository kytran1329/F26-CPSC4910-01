from flask import (
    Flask,
    render_template,
    request, 
    redirect, 
    url_for, 
    session, 
    flash,
    current_app)
import mysql.connector 
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from decimal import Decimal, InvalidOperation

from export import export, parseOrderReportFilters, getOrderReportRows
from catalog import cat
from auth import auth
from notifications import create_notification, NOTIFICATION_TYPES, ROLE_NOTIFICATION_TYPES
from bulk_upload import validate_bulk_upload

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
global USER_ID

app = Flask(__name__, static_folder= "styles")
#FLASK_SECRET_KEY add in .env
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(auth)
app.register_blueprint(cat)
app.register_blueprint(export)

# THIS STOPS SOMEONE FROM LOGGIN BACK IN BY HITTING THE BACK BUTTON AFTER THEY HAVE LOGGED OUT
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/backToDash")
def backToDash():
    if session.get("role") == "Driver":
        return redirect(url_for("driverDash"))
    elif session.get("role") == "Sponsor":
        return redirect(url_for("sponDash"))
    elif session.get("role") == "Admin":
        return redirect(url_for("adminDash"))
    else:
        return redirect(url_for("home"))

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
                    JOIN BALANCE as b
                        on b.DRIVER_ID = d.DRIVER_ID
                    JOIN SPONSOR AS s
                        ON s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                    WHERE d.DRIVER_ID = %s
                      AND s.USER_ID = %s
                      AND b.IS_ACTIVE = 1
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
                        b.BALANCE
                    from BALANCE as b
                    join DRIVER as d
                        on d.DRIVER_ID = b.DRIVER_ID 
                    join `USER` as u
                        on u.USER_ID = d.USER_ID
                    where d.USER_ID  = %s
                    and b.IS_ACTIVE = 1""", (user_id,))
        
        drive_info = cursor.fetchone()
        if drive_info is None:
            return driverApplications()
        
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
                ORDER_DTS,
                (ORDER_STATUS = 'Active'
                AND NOW() < DATE_ADD(
                    ORDER_DTS, INTERVAL 5 MINUTE)
            ) AS CAN_CANCEL
            from ORDERS
            WHERE DRIVER_ID = %s
            order by ORDER_DTS DESC;
                """, (drive_info["DRIVER_ID"],))

        order_stat = cursor.fetchall()

        cursor.execute("""
            select
                io.ITEMIZED_ID,
                io.ORDER_ID,
                io.ITEM_NAME,
                io.ITEM_DESC,
                io.ITEM_AMOUNT,
                io.ITEM_PRICE,
                o.ORDER_DTS,
                o.ORDER_STATUS
            from ITEMIZEDORDER as io
            join ORDERS as o
                on io.ORDER_ID = o.ORDER_ID
            where o.DRIVER_ID = %s
            order by o.ORDER_DTS desc, io.ITEMIZED_ID asc
        """, (drive_info["DRIVER_ID"],))

        itemized_orders = cursor.fetchall()

        cursor.close()
        conn.close()
        #print(drive_info)
        return render_template("driverDash.html", drive_info = drive_info,
                            history= history, order_stat = order_stat,
                            itemized_orders = itemized_orders)
    finally: 
        cursor.close()
        conn.close()


@app.route("/cancelOrder/<int:order_id>", methods=["POST"])
def cancelOrder(order_id):

    # Only logged-in Drivers can cancel their own orders.
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Driver":
        return "Unauthorized", 403

    user_id = session["user_id"]

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

    try:
        # Lock the order to prevent two cancellation
        # requests from refunding the same purchase.
        cursor.execute("""
            SELECT
                o.ORDER_ID,
                o.DRIVER_ID,
                o.SPONSORCOMP_ID,
                o.POINT_TOTAL,
                o.ORDER_STATUS,
                o.ORDER_DTS,
                (NOW() < DATE_ADD(
                    o.ORDER_DTS, INTERVAL 5 MINUTE
                )) AS CAN_CANCEL
            FROM ORDERS AS o
            JOIN DRIVER AS d
                ON d.DRIVER_ID = o.DRIVER_ID
            WHERE o.ORDER_ID = %s
              AND o.USER_ID = %s
              AND d.USER_ID = %s
            FOR UPDATE
        """, (order_id, user_id, user_id))

        order = cursor.fetchone()

        if order is None:
            conn.rollback()
            flash("Order not found.", "error")
            return redirect(url_for("driverDash"))

        if order["ORDER_STATUS"] != "Active":
            conn.rollback()
            flash("This order can no longer be cancelled.", "error")
            return redirect(url_for("driverDash"))

        if not order["CAN_CANCEL"]:
            conn.rollback()
            flash("The 5-minute cancellation window has expired.", "error")
            return redirect(url_for("driverDash"))

        # Find the original sponsor balance, including
        # balances that are no longer active.
        cursor.execute("""
            SELECT BALANCE_ID
            FROM BALANCE
            WHERE DRIVER_ID = %s
              AND SPONSORCOMP_ID = %s
            FOR UPDATE
        """, (
            order["DRIVER_ID"],
            order["SPONSORCOMP_ID"]
        ))

        balance = cursor.fetchone()

        if balance is None:
            raise ValueError("The original order balance was not found.")

        # Recheck the deadline at the time of the status
        # update, not just when the request first arrived.
        cursor.execute("""
            UPDATE ORDERS
            SET ORDER_STATUS = 'Cancelled'
            WHERE ORDER_ID = %s
              AND ORDER_STATUS = 'Active'
              AND NOW() < DATE_ADD(
                  ORDER_DTS, INTERVAL 5 MINUTE
              )
        """, (order_id,))

        if cursor.rowcount != 1:
            conn.rollback()
            flash("The cancellation window has expired.", "error")
            return redirect(url_for("driverDash"))

        # Refund the original amount of points.
        cursor.execute("""
            UPDATE BALANCE
            SET BALANCE = BALANCE + %s
            WHERE BALANCE_ID = %s
        """, (
            order["POINT_TOTAL"],
            balance["BALANCE_ID"]
        ))

        if cursor.rowcount != 1:
            raise ValueError("The points could not be refunded.")

        # Record the refund in point history.
        cursor.execute("""
            INSERT INTO POINTCHANGES (
                BALANCE_ID,
                DRIVER_ID,
                POINTCHANGE_AMOUNT,
                POINTCHANGE_REASON,
                USER_ID
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            balance["BALANCE_ID"],
            order["DRIVER_ID"],
            order["POINT_TOTAL"],
            f"Refund for cancelled order #{order_id}",
            user_id
        ))

        # Save the cancellation and refund together.
        conn.commit()

        flash(
            f"Order #{order_id} was cancelled. "
            f"{order['POINT_TOTAL']} points were refunded.",
            "success"
        )

    except (mysql.connector.Error, ValueError):
        conn.rollback()
        current_app.logger.exception(
            "Failed to cancel order %s", order_id
        )
        flash(
            "Unable to cancel the order. No refund was completed.",
            "error"
        )

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("driverDash"))

@app.route("/sponDash/applications")
def applications():

    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    # Validate the selected dates
    try:
        if start_date:
            date.fromisoformat(start_date)

        if end_date:
            date.fromisoformat(end_date)

        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must not be after end date.")

    except ValueError:
        return render_template(
            "applications.html",
            applications=[],
            start_date=start_date,
            end_date=end_date,
            error="Please enter a valid date range."
        )
    # Get pending driver applications
    # from the database

    # connect to sql database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    # grab correct data about each applicant
    # Get pending applications for the logged-in sponsor's company
    query = """
            SELECT
                a.APPLICATION_ID,
                u.USER_FNAME,
                u.USER_LNAME,
                u.EMAIL,
                a.CREATED_DTS,
                a.STATUS,
                u.USER_ID
            FROM APPLICATIONS AS a
            JOIN USER AS u
                ON u.USER_ID = a.USER_ID
            JOIN SPONSOR AS s
                ON s.SPONSORCOMP_ID = a.SPONSORCOMP_ID
            WHERE a.STATUS = 'Pending'
              AND s.USER_ID = %s
        """

    params = [session["user_id"]]

    if start_date:
        query += " AND a.CREATED_DTS >= %s"
        params.append(start_date)

    if end_date:
        query += " AND a.CREATED_DTS < DATE_ADD(%s, INTERVAL 1 DAY)"
        params.append(end_date)

    query += " ORDER BY a.CREATED_DTS DESC"

    cursor.execute(query, params)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "applications.html",
        applications=applications
    )


@app.route("/sponDash/applications/bulk_update_applications", methods=["POST"])
def bulk_update_applications():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Sponsor":
        return redirect(url_for("home"))

    # connect to sql database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
    )

    action = request.form.get("action")
    application_ids = request.form.getlist("application_ids")
    reason = request.form.get("reason", "").strip()

    start_date = request.form.get("start_date", "")
    end_date = request.form.get("end_date", "")

    # Only allow these two status changes
    if action not in ("Accepted", "Rejected"):
        return redirect(url_for(
            "applications",
            start_date=start_date,
            end_date=end_date
        ))

    # Require at least one selected application
    if not application_ids:
        return redirect(url_for(
            "applications",
            start_date=start_date,
            end_date=end_date
        ))

    # Validate that all IDs are integers
    try:
        application_ids = [int(app_id) for app_id in application_ids]
    except ValueError:
        return "Invalid application ID", 400

    placeholders = ", ".join(["%s"] * len(application_ids))

    cursor = conn.cursor(dictionary=True)

    # Get the logged-in sponsor's information
    cursor.execute("""
        SELECT SPONSOR_ID, SPONSORCOMP_ID
        FROM SPONSOR
        WHERE USER_ID = %s
    """, (session["user_id"],))

    sponsor = cursor.fetchone()

    cursor.execute(f"""
        SELECT APPLICATION_ID, USER_ID, SPONSORCOMP_ID
        FROM APPLICATIONS
        WHERE APPLICATION_ID IN ({placeholders})
            AND SPONSORCOMP_ID = %s
            AND STATUS = 'Pending'
        FOR UPDATE
    """, tuple(application_ids) + (sponsor["SPONSORCOMP_ID"],))

    applications = cursor.fetchall()

    if not applications:
        return redirect(url_for(
            "applications",
            start_date=start_date,
            end_date=end_date
        ))

    # Update the selected applications
    valid_ids = [app["APPLICATION_ID"] for app in applications]
    valid_placeholders = ", ".join(["%s"] * len(valid_ids))
    try:
        if action == "Accepted":
            # Update the selected applications
            cursor.execute(f"""
                UPDATE APPLICATIONS
                SET STATUS = 'Accepted',
                    SPONSOR_ID = %s,
                    REASON = CASE
                        WHEN %s = '' THEN REASON
                        WHEN REASON IS NULL OR REASON = '' THEN %s
                        ELSE CONCAT(REASON, '\n', %s)
                    END,
                    UPDATED_DTS = NOW()
                WHERE APPLICATION_ID IN ({valid_placeholders})
                AND STATUS = 'Pending'
                AND SPONSORCOMP_ID = %s
            """, (
                sponsor["SPONSOR_ID"],
                reason,
                reason,
                reason,
                *valid_ids,
                sponsor["SPONSORCOMP_ID"]
            ))

            # Create driver and balance records as needed
            for application in applications:
                user_id = application["USER_ID"]
                sponsorcomp_id = application["SPONSORCOMP_ID"]

                # Check whether this user already has a DRIVER record
                cursor.execute("""
                    SELECT DRIVER_ID
                    FROM DRIVER
                    WHERE USER_ID = %s
                """, (user_id,))

                driver = cursor.fetchone()

                # Create the DRIVER record only if one doesn't exist
                if driver:
                    driver_id = driver["DRIVER_ID"]
                else:
                    cursor.execute("""
                        INSERT INTO DRIVER (USER_ID)
                        VALUES (%s)
                    """, (user_id,))

                    driver_id = cursor.lastrowid

                # Check whether this driver already has a balance
                # for this sponsor company
                cursor.execute("""
                    SELECT DRIVER_ID, IS_ACTIVE
                    FROM BALANCE
                    WHERE DRIVER_ID = %s
                    AND SPONSORCOMP_ID = %s
                """, (driver_id, sponsorcomp_id))

                balance_record = cursor.fetchone()

                # Create an initial zero balance only if needed
                if balance_record:
                    # reactivate the existing affiliation
                    if not balance_record["IS_ACTIVE"]:
                        cursor.execute("""
                            UPDATE BALANCE
                            SET IS_ACTIVE = 1
                            WHERE DRIVER_ID = %s
                              AND SPONSORCOMP_ID = %s
                        """, (driver_id, sponsorcomp_id))
                else:
                    # create new affiliation
                    cursor.execute("""
                        INSERT INTO BALANCE
                            (DRIVER_ID, SPONSORCOMP_ID, BALANCE, IS_ACTIVE)
                        VALUES (%s, %s, %s, %s)
                    """, (driver_id, sponsorcomp_id, 0, 1))

        else:
            # Reject applications without creating driver records
            cursor.execute(f"""
                UPDATE APPLICATIONS
                SET STATUS = 'Rejected',
                    SPONSOR_ID = %s,
                    REASON = CASE
                        WHEN %s = '' THEN REASON
                        WHEN REASON IS NULL OR REASON = '' THEN %s
                        ELSE CONCAT(REASON, '\n', %s)
                    END,
                    UPDATED_DTS = NOW()
                WHERE APPLICATION_ID IN ({valid_placeholders})
                  AND STATUS = 'Pending'
                  AND SPONSORCOMP_ID = %s
            """, (
                sponsor["SPONSOR_ID"],
                reason,
                reason,
                reason,
                *valid_ids,
                sponsor["SPONSORCOMP_ID"]
            ))

        # notify the driver about the application decision
        for application in applications:
            driver_user_id = application["USER_ID"]
            sponsorcomp_id = application["SPONSORCOMP_ID"]
            application_id = application["APPLICATION_ID"]

            # get the sponsor company's name for the notification
            cursor.execute("""
                SELECT SPONSORCOMP_NAME
                FROM SPONSORCOMP
                WHERE SPONSORCOMP_ID = %s
            """, (sponsorcomp_id,))

            company = cursor.fetchone()
            company_name = (
                company["SPONSORCOMP_NAME"]
                if company
                else "the sponsor company"
            )

            # get driver's name
            cursor.execute("""
                SELECT USER_FNAME, USER_LNAME
                FROM USER
                WHERE USER_ID = %s
            """, (driver_user_id,))

            driver_info = cursor.fetchone()
            driver_name = (
                f"{driver_info['USER_FNAME']} {driver_info['USER_LNAME']}"
                if driver_info
                else f"Driver user ID {driver_user_id}"
            )

            if action == "Accepted":
                create_notification(
                    cursor,
                    driver_user_id,
                    "APPLICATION_ACCEPTED",
                    "Application accepted!",
                    f"Your application to join {company_name} "
                    f"has been accepted.",
                    application_id=application_id
                )

                # notify driver that relationship created
                create_notification(
                    cursor,
                    driver_user_id,
                    "DRIVER_SPONSOR_ADDED",
                    "Sponsor added",
                    f"You are now connected with {company_name}. "
                    f"You can begin earning points through this company.",
                    application_id=application_id
                )

                # notify sponsor that driver was added
                cursor.execute("""
                    SELECT USER_ID
                    FROM SPONSOR
                    WHERE SPONSORCOMP_ID = %s
                """, (sponsorcomp_id,))

                sponsor_users = cursor.fetchall()
                
                for sponsor_user in sponsor_users:
                    create_notification(
                        cursor,
                        sponsor_user["USER_ID"],
                        "SPONSOR_DRIVER_ADDED",
                        "Driver added",
                        f"A driver's application to join {company_name} "
                        f"was accepted. The driver is now connected "
                        f"with your company.",
                        application_id=application_id
                    )

                # notify admin of application acceptance
                cursor.execute("""
                    SELECT USER_ID
                    FROM USER
                    WHERE ROLE = 'Admin'
                """)

                admin_users = cursor.fetchall()
                
                for admin_user in admin_users:
                    create_notification(
                        cursor,
                        admin_user["USER_ID"],
                        "ADMIN_APPLICATION_ACCEPTED",
                        "Driver application accepted",
                        f"{driver_name} was accepted by {company_name}. "
                        f"The driver is now connected with this sponsor.",
                        application_id=application_id
                    )

            else:
                create_notification(
                    cursor,
                    driver_user_id,
                    "APPLICATION_REJECTED",
                    "Application update",
                    f"Your application to join {company_name} "
                    f"was not accepted.",
                    application_id=application_id
                )

        conn.commit()

    except mysql.connector.Error:
        conn.rollback()
        current_app.logger.exception(
            "Error processing sponsor applications"
        )

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for(
        "applications",
        start_date=start_date,
        end_date=end_date
    ))

@app.route("/driverDash/applications", methods=["GET", "POST"])
def driverApplications():
    # Connect to database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    cursor = conn.cursor(dictionary=True)
    
    error = None
    success = None
    user_id = session["user_id"]

    if request.method == "POST":

        sponsorcomp_id = request.form.get("sponsor_id")

        if not sponsorcomp_id:
            error = "Please select a sponsor company."

        else:
            try:
                sponsorcomp_id = int(sponsorcomp_id)

                # Select user for user information
                cursor.execute(
                        "SELECT * FROM USER WHERE USER_ID = %s",
                        (user_id,)
                )
                            
                user = cursor.fetchone()

                first_name = user["USER_FNAME"]
                last_name = user["USER_LNAME"]

                # Check if the driver already applied to this company
                # Allow apply again if previously rejected
                cursor.execute("""
                    SELECT APPLICATION_ID
                    FROM APPLICATIONS
                    WHERE USER_ID = %s
                    AND SPONSORCOMP_ID = %s
                    AND STATUS != 'Rejected'
                """, (user_id, sponsorcomp_id))

                existing_application = cursor.fetchone()

                if existing_application:
                    error = "You have already submitted an application to this sponsor company."

                else:
                    # Get the sponsor company's name
                    cursor.execute("""
                        SELECT SPONSORCOMP_NAME
                        FROM SPONSORCOMP
                        WHERE SPONSORCOMP_ID = %s
                    """, (sponsorcomp_id,))

                    company = cursor.fetchone()

                    if not company:
                        error = "The selected sponsor company could not be found."

                    else:
                        company_name = company["SPONSORCOMP_NAME"]

                        # Insert the new sponsor application
                        cursor.execute("""
                            INSERT INTO APPLICATIONS
                                (USER_ID, SPONSORCOMP_ID, SPONSOR_ID)
                            VALUES (%s, %s, NULL)
                        """, (user_id, sponsorcomp_id))

                        application_id = cursor.lastrowid

                        # Notify all sponsors in the company
                        cursor.execute("""
                            SELECT USER_ID
                            FROM SPONSOR
                            WHERE SPONSORCOMP_ID = %s
                        """, (sponsorcomp_id,))

                        sponsor_users = cursor.fetchall()

                        for sponsor_user in sponsor_users:
                            create_notification(
                                cursor,
                                sponsor_user["USER_ID"],
                                "SPONSOR_NEW_APPLICATION",
                                "New driver application",
                                f"{first_name} {last_name} has applied to join "
                                f"{company_name}.",
                                application_id=application_id
                            )

                        # Notify all admins
                        cursor.execute("""
                            SELECT USER_ID
                            FROM USER
                            WHERE ROLE = 'Admin'
                        """)

                        admin_users = cursor.fetchall()

                        for admin_user in admin_users:
                            create_notification(
                                cursor,
                                admin_user["USER_ID"],
                                "ADMIN_NEW_APPLICATION",
                                "New driver application",
                                f"{first_name} {last_name} has applied to join "
                                f"{company_name}.",
                                application_id=application_id
                            )

                        # Commit the application and notifications
                        conn.commit()

                        success = f"Your application to {company_name} was submitted successfully!"

            except ValueError:
                error = "Invalid sponsor company selection."

            except Exception as e:
                conn.rollback()
                print(f"Error submitting application: {e}")
                error = "Something went wrong while submitting your application. Please try again."

    # Validate selected dates
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    try:
        if start_date:
            date.fromisoformat(start_date)

        if end_date:
            date.fromisoformat(end_date)

        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must not be after end date.")

    except ValueError:
        return render_template(
            "driverApplications.html",
            applications=[],
            sponsors=[],
            start_date=start_date,
            end_date=end_date,
            error="Please enter a valid date range.",
            success=success
        )

    # Get the logged-in driver's applications
    query = """
        SELECT
            a.APPLICATION_ID,
            a.CREATED_DTS,
            a.STATUS,
            a.REASON,
            s.SPONSORCOMP_NAME
        FROM APPLICATIONS AS a
        JOIN SPONSORCOMP AS s
            ON s.SPONSORCOMP_ID = a.SPONSORCOMP_ID
        WHERE a.USER_ID = %s
    """

    params = [session["user_id"]]

    if start_date:
        query += " AND a.CREATED_DTS >= %s"
        params.append(start_date)

    if end_date:
        query += " AND a.CREATED_DTS < DATE_ADD(%s, INTERVAL 1 DAY)"
        params.append(end_date)

    query += " ORDER BY a.CREATED_DTS DESC"

    cursor.execute(query, params)

    applications = cursor.fetchall()

    # Get available sponsor companies for dropdown
    cursor.execute("""
        SELECT
            SPONSORCOMP_ID,
            SPONSORCOMP_NAME
        FROM SPONSORCOMP
        ORDER BY SPONSORCOMP_NAME
    """)

    sponsors = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "driverApplications.html",
        applications=applications,
        sponsors=sponsors,
        start_date=start_date,
        end_date=end_date,
        error=error,
        success=success
    )

@app.route("/userProfile/<int:user_id>")
def userProfile(user_id):
    # user_id = USER_ID

    current_user_id = session.get("user_id")

    if current_user_id is None:
        user_id = USER_ID
        # return redirect(url_for("login"))

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

    return render_template(
        "userProfile.html", 
        user_id=user_id, 
        user=user,
        error=error,
        success=success)

@app.route("/updateFirstName/<int:user_id>", methods=["POST"])
def updateFirstName(user_id):
    first_name = request.form["first_name"].strip()

    if not first_name:
        return redirect(url_for(
            "userProfile", 
            user_id=user_id, 
            error="First name cannot be empty."
            ))

    if not first_name.isalpha():
        return redirect(url_for(
            "userProfile", 
            user_id=user_id, 
            error="First name can only contain letters."
        ))

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

    return redirect(url_for(
        "userProfile", 
        user_id=user_id, 
        success="First name updated successfully!"))

@app.route("/updateLastName/<int:user_id>", methods=["POST"])
def updateLastName(user_id):
    last_name = request.form["last_name"].strip()

    if not last_name:
        return redirect(url_for(
                "userProfile",
                user_id=user_id, 
                error="Last name cannot be empty."
            ))

    if not last_name.isalpha():
        return redirect(url_for(
            "userProfile",
            user_id=user_id,
            error="Last name can only contain letters."))

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

    return redirect(url_for(
        "userProfile", 
        user_id=user_id, 
        success="Last name updated successfully!"
    ))

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
            b.SPONSORCOMP_ID,
            b.BALANCE,

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

        join BALANCE as b
            on b.DRIVER_ID = d.DRIVER_ID

        left join POINTCHANGES as p
            on p.USER_ID = d.USER_ID

        where b.is_active = 1
            and b.SPONSORCOMP_ID in (
                select s.SPONSORCOMP_ID
                from SPONSOR as s
                where s.USER_ID = %s
            )

        group by
            u.USER_ID,
            u.USER_FNAME,
            u.USER_LNAME,
            u.ROLE,
            u.EMAIL,
            d.DRIVER_ID,
            b.SPONSORCOMP_ID,
            b.BALANCE

        order by d.DRIVER_ID
    """, (sponsor_user_id,))

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
        join BALANCE as b
            on b.DRIVER_ID = d.DRIVER_ID
        JOIN `USER` AS u
            ON d.USER_ID = u.USER_ID
        WHERE b.SPONSORCOMP_ID IN (
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
        SELECT COALESCE(
            SUM(p.POINTCHANGE_AMOUNT), 0) AS POINTS_THIS_MONTH

        FROM SPONSOR AS s
        JOIN BALANCE as b
            ON s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
        JOIN DRIVER AS d
            ON b.DRIVER_ID = d.DRIVER_ID
        JOIN POINTCHANGES AS p
            ON p.DRIVER_ID = d.DRIVER_ID

        WHERE s.USER_ID = %s
            AND p.POINTCHANGE_AMOUNT > 0
            AND p.DTS >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
            AND p.DTS < DATE_ADD(
                DATE_FORMAT(CURDATE(), '%Y-%m-01'),
                INTERVAL 1 MONTH
            );
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

@app.route("/sponDash/drivers")
def driverView():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    if role == "Sponsor":
        sponsor_id = session["user_id"]
        sponsor_lookup = "USER_ID"
    elif role == "Admin":
        sponsor_id = session.get("view_as_sponsor_id")
        if sponsor_id is None:
            return redirect(url_for("adminDash"))
        sponsor_lookup = "SPONSOR_ID"
    else:
        return "Unauthorized", 403

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(f"""
            SELECT SPONSORCOMP_ID
            FROM SPONSOR
            WHERE {sponsor_lookup} = %s
        """, (sponsor_id,))
        sponsor = cursor.fetchone()

        if sponsor is None:
            return "Sponsor account not found", 404

        cursor.execute("""
            SELECT DISTINCT
                d.DRIVER_ID,
                u.USER_ID,
                u.USER_FNAME,
                u.USER_LNAME,
                u.EMAIL,
                b.BALANCE
            FROM BALANCE AS b
            JOIN DRIVER AS d
                ON d.DRIVER_ID = b.DRIVER_ID
            JOIN `USER` AS u
                ON u.USER_ID = d.USER_ID
            WHERE b.SPONSORCOMP_ID = %s
                AND b.IS_ACTIVE = 1
            ORDER BY u.USER_LNAME, u.USER_FNAME, d.DRIVER_ID
        """, (sponsor["SPONSORCOMP_ID"],))
        drivers = cursor.fetchall()

        return render_template("driverView.html", drivers=drivers)
    finally:
        cursor.close()
        conn.close()

@app.route("/sponDash/drivers/<int:driver_id>/fire", methods=["POST"])
def fireDriver(driver_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    if role == "Sponsor":
        cursor_sponsor_id = session["user_id"]
        sponsor_query = """
            SELECT s.SPONSORCOMP_ID, sc.SPONSORCOMP_NAME
            FROM SPONSOR AS s
            JOIN SPONSORCOMP AS sc
                ON sc.SPONSORCOMP_ID = s.SPONSORCOMP_ID
            WHERE s.USER_ID = %s
        """
    elif role == "Admin":
        cursor_sponsor_id = session.get("view_as_sponsor_id")
        if cursor_sponsor_id is None:
            return redirect(url_for("adminDash"))
        sponsor_query = """
            SELECT s.SPONSORCOMP_ID, sc.SPONSORCOMP_NAME
            FROM SPONSOR AS s
            JOIN SPONSORCOMP AS sc
                ON sc.SPONSORCOMP_ID = s.SPONSORCOMP_ID
            WHERE s.SPONSOR_ID = %s
        """
    else:
        return "Unauthorized", 403

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(sponsor_query, (cursor_sponsor_id,))
        sponsor = cursor.fetchone()
        if sponsor is None:
            return "Sponsor account not found", 404

        sponsorcomp_id = sponsor["SPONSORCOMP_ID"]
        company_name = sponsor["SPONSORCOMP_NAME"]

        cursor.execute("""
            SELECT d.USER_ID, u.USER_FNAME, u.USER_LNAME
            FROM BALANCE AS b
            JOIN DRIVER AS d
                ON d.DRIVER_ID = b.DRIVER_ID
            JOIN `USER` AS u
                ON u.USER_ID = d.USER_ID
            WHERE b.DRIVER_ID = %s
              AND b.SPONSORCOMP_ID = %s
              AND b.IS_ACTIVE = 1
        """, (driver_id, sponsorcomp_id))
        driver = cursor.fetchone()
        if driver is None:
            flash("That driver is not affiliated with your company.", "error")
            return redirect(url_for("driverView"))

        cursor.execute("""
            UPDATE BALANCE
            SET IS_ACTIVE = 0
            WHERE DRIVER_ID = %s
              AND SPONSORCOMP_ID = %s
              AND IS_ACTIVE = 1
        """, (driver_id, sponsorcomp_id))
        if cursor.rowcount != 1:
            conn.rollback()
            flash("The driver affiliation could not be removed.", "error")
            return redirect(url_for("driverView"))

        driver_name = (
            f"{driver['USER_FNAME']} {driver['USER_LNAME']}"
        )
        create_notification(
            cursor,
            driver["USER_ID"],
            "DRIVER_SPONSOR_REMOVED",
            "Sponsor connection ended",
            f"You are no longer connected with {company_name}."
        )

        cursor.execute("""
            SELECT USER_ID
            FROM SPONSOR
            WHERE SPONSORCOMP_ID = %s
        """, (sponsorcomp_id,))
        for sponsor_user in cursor.fetchall():
            create_notification(
                cursor,
                sponsor_user["USER_ID"],
                "SPONSOR_DRIVER_REMOVED",
                "Driver removed",
                f"{driver_name} was removed from {company_name}."
            )

        # notify admin of driver removal
        cursor.execute("""
            SELECT USER_ID
            FROM USER
            WHERE ROLE = 'Admin'
        """)
        for admin_user in cursor.fetchall():
            create_notification(
                cursor,
                admin_user["USER_ID"],
                "ADMIN_DRIVER_REMOVED",
                "Driver removed from sponsor company",
                f"{driver_name} was removed from {company_name}."
            )

        conn.commit()
        flash(f"{driver_name} was removed from {company_name}.", "success")
    except mysql.connector.Error:
        conn.rollback()
        current_app.logger.exception("Error removing driver from sponsor company")
        flash("The driver could not be removed due to a database error.", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("driverView"))

@app.route("/assignPoints", methods=["GET", "POST"])
def assignPoints():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("role")
    if role not in ("Sponsor", "Admin"):
        return "Unauthorized", 403

    is_admin = role == "Admin"
    actor_user_id = session["user_id"]

    # Admins may choose one company or all companies.
    # Sponsors' company is determined from their logged-in account.
    selected_company_raw = request.values.get("sponsorcomp_id", "all")
    selected_company_id = None

    if is_admin and selected_company_raw != "all":
        try:
            selected_company_id = int(selected_company_raw)
            if selected_company_id <= 0:
                raise ValueError
        except (TypeError, ValueError):
            flash("Please select a valid sponsor company.", "error")
            return redirect(url_for("assignPoints"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == "POST":

            # Save the point-to-dollar conversion rate (sponsors only)
            if request.form.get("rate_action") == "save_rate":
                if is_admin:
                    flash("Only sponsors can change the conversion rate.", "error")
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                try:
                    rate_dollars = Decimal(request.form.get("rate_dollars", "").strip())
                    rate_points = int(request.form.get("rate_points", "").strip())

                    if (not rate_dollars.is_finite()
                            or rate_dollars <= 0 or rate_dollars > 1000000
                            or rate_points <= 0 or rate_points > 1000000):
                        raise ValueError

                    rate_dollars = rate_dollars.quantize(Decimal("0.01"))
                    if rate_dollars <= 0:      # e.g. 0.001 rounds down to 0
                        raise ValueError

                except (InvalidOperation, ValueError):
                    flash(
                        "Enter a dollar amount and a whole number of points, "
                        "both greater than zero.",
                        "error"
                    )
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                # The company comes from the logged-in account, never from the form.
                cursor.execute(
                    "SELECT SPONSORCOMP_ID FROM SPONSOR WHERE USER_ID = %s",
                    (actor_user_id,)
                )
                sponsor_row = cursor.fetchone()

                if not sponsor_row:
                    flash("Your account isn't linked to a sponsor company.", "error")
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                cursor.execute("""
                    UPDATE SPONSORCOMP
                    SET SPONSORCOMP_DOLLAR = %s,
                        SPONSORCOMP_POINT = %s
                    WHERE SPONSORCOMP_ID = %s
                """, (rate_dollars, rate_points, sponsor_row["SPONSORCOMP_ID"]))
                conn.commit()

                flash(
                    f"Conversion rate saved: ${rate_dollars} = {rate_points} points.",
                    "success"
                )
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            # Bulk Add or Subtract
            bulk_action = request.form.get("bulk_action")

            if bulk_action in ("add_all", "subtract_all"):
                try:
                    bulk_amount = int(request.form.get("bulk_amount", ""))
                except (TypeError, ValueError):
                    flash("Enter a valid whole-number point amount.","error")
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                bulk_reason = request.form.get("bulk_reason", "").strip()

                if bulk_amount <= 0:
                    flash("The point amount must be greater than zero.","error")
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                if not bulk_reason:
                    flash("Please enter a reason for the point change.","error")
                    return redirect(url_for(
                        "assignPoints",
                        sponsorcomp_id=selected_company_raw
                    ))

                signed_amount = (bulk_amount
                    if bulk_action == "add_all"
                    else -bulk_amount
                )

                # Apply the same company restriction when selecting
                # balances and when updating them.
                company_condition = ""
                company_params = []

                if is_admin:
                    # A selected company; otherwise, all companies.
                    if selected_company_id is not None:
                        company_condition = """
                            AND b.SPONSORCOMP_ID = %s
                        """
                        company_params.append(selected_company_id)
                else:
                    # Sponsors can only affect their own company.
                    company_condition = """
                        AND EXISTS (
                            SELECT 1
                            FROM SPONSOR AS s
                            WHERE s.USER_ID = %s
                              AND s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                        )
                    """
                    company_params.append(actor_user_id)

                try:
                    # Lock the balances before validating them.
                    cursor.execute("""
                        SELECT
                            b.BALANCE_ID,
                            b.DRIVER_ID,
                            b.SPONSORCOMP_ID,
                            b.BALANCE
                        FROM BALANCE AS b
                        WHERE b.IS_ACTIVE = 1
                    """ + company_condition + """
                        FOR UPDATE
                    """, tuple(company_params))

                    balances = cursor.fetchall()

                    if not balances:
                        conn.rollback()
                        flash("There are no balances to update.","error")
                        return redirect(url_for(
                            "assignPoints",
                            sponsorcomp_id=selected_company_raw
                        ))

                    # Prevent a bulk subtraction if one balance goes negative.
                    if bulk_action == "subtract_all":
                        insufficient = any(
                            float(balance["BALANCE"] or 0) < bulk_amount
                            for balance in balances
                        )

                        if insufficient:
                            conn.rollback()
                            flash(
                                "Bulk subtraction cancelled: at least "
                                "one balance does not have enough points. "
                                "No balances were changed.",
                                "error"
                            )
                            return redirect(url_for(
                                "assignPoints",
                                sponsorcomp_id=selected_company_raw
                            ))

                    # Update only the balances selected above.
                    cursor.execute("""
                        UPDATE BALANCE AS b
                        SET BALANCE = BALANCE + %s
                        WHERE b.IS_ACTIVE = 1
                    """ + company_condition,
                    tuple([signed_amount] + company_params))

                    for balance in balances:
                        # record point change
                        cursor.execute("""
                            INSERT INTO POINTCHANGES (
                                BALANCE_ID,
                                DRIVER_ID,
                                POINTCHANGE_AMOUNT,
                                POINTCHANGE_REASON,
                                USER_ID
                            )
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            balance["BALANCE_ID"],
                            balance["DRIVER_ID"],
                            signed_amount,
                            bulk_reason,
                            actor_user_id
                        ))

                        pointchange_id = cursor.lastrowid

                        # get driver user account and sponsor company name
                        cursor.execute("""
                            SELECT d.USER_ID AS DRIVER_USER_ID,
                                sc.SPONSORCOMP_NAME
                            FROM DRIVER AS d
                            JOIN SPONSORCOMP AS sc
                                ON sc.SPONSORCOMP_ID = %s
                            WHERE d.DRIVER_ID = %s
                        """, (
                            balance["SPONSORCOMP_ID"],
                            balance["DRIVER_ID"]
                        ))

                        driver_info = cursor.fetchone()

                        if driver_info:
                            driver_user_id = driver_info["DRIVER_USER_ID"]
                            company_name = driver_info["SPONSORCOMP_NAME"]

                            # calculate the driver's updated balance
                            new_balance = (float(balance["BALANCE"] or 0) + signed_amount)

                            #notify driver
                            if signed_amount > 0:
                                driver_type = "POINTS_GAINED"
                                driver_title = "You earned points!"
                                driver_message = (
                                    f"You received {signed_amount} points from "
                                    f"{company_name}. Reason: {bulk_reason}. "
                                    f"Your new balance is {new_balance:g} points."
                                )
                            else:
                                driver_type = "POINTS_LOST"
                                driver_title = "Your points changed"
                                driver_message = (
                                    f"{abs(signed_amount)} points were deducted by "
                                    f"{company_name}. Reason: {bulk_reason}. "
                                    f"Your new balance is {new_balance:g} points."
                                )
                            
                            create_notification(
                                cursor,
                                driver_user_id,
                                driver_type,
                                driver_title,
                                driver_message,
                                pointchange_id=pointchange_id
                            )

                            # notify sponsor associated with company
                            cursor.execute("""
                                SELECT USER_ID
                                FROM SPONSOR
                                WHERE SPONSORCOMP_ID = %s
                            """, (balance["SPONSORCOMP_ID"],))

                            sponsor_users = cursor.fetchall()

                            for sponsor_user in sponsor_users:
                                create_notification(
                                    cursor,
                                    sponsor_user["USER_ID"],
                                    "SPONSOR_POINT_CHANGE",
                                    "Driver points Updated",
                                    f"{abs(signed_amount)} points were "
                                    f"{'added to' if signed_amount > 0 else 'deducted from'} "
                                    f"a driver's balance at {company_name}. "
                                    f"Reason: {bulk_reason}. "
                                    f"New balance: {new_balance:g} points.",
                                    pointchange_id=pointchange_id
                                )

                            # notify admin
                            cursor.execute("""
                                SELECT USER_ID
                                FROM USER
                                WHERE ROLE = 'Admin'
                            """)

                            admin_users = cursor.fetchall()

                            for admin_user in admin_users:
                                create_notification(
                                    cursor,
                                    admin_user["USER_ID"],
                                    "ADMIN_POINT_CHANGE",
                                    "Driver points Updated",
                                    f"{abs(signed_amount)} points were "
                                    f"{'added to' if signed_amount > 0 else 'deducted from'} "
                                    f"a driver's balance at {company_name}. "
                                    f"Reason: {bulk_reason}. "
                                    f"New balance: {new_balance:g} points.",
                                    pointchange_id=pointchange_id
                                )

                    conn.commit()

                    operation = (
                        "added to"
                        if bulk_action == "add_all"
                        else "subtracted from"
                    )

                    flash(
                        f"{bulk_amount} points successfully {operation} "
                        f"{len(balances)} balances.",
                        "success"
                    )

                except Exception:
                    conn.rollback()
                    raise

                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            # Add or Subtract Individually
            driver_id_raw = request.form.get("driver_id", "")
            balance_company_raw = request.form.get("sponsorcomp_id", "")
            action = request.form.get("action", "")
            amount_raw = request.form.get("amount", "")
            reason = request.form.get("reason", "").strip()

            try:
                driver_id = int(driver_id_raw)
                balance_company_id = int(balance_company_raw)
                amount = int(amount_raw)

                if driver_id <= 0 or balance_company_id <= 0:
                    raise ValueError

            except (TypeError, ValueError):
                flash(
                    "Select a valid driver and enter a whole-number point amount.",
                    "error"
                )
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            if amount <= 0:
                flash("The point amount must be greater than zero.","error")
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            if action not in ("add", "subtract"):
                flash("Choose whether to add or subtract points.","error")
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            if not reason:
                flash(
                    "Please enter a reason for the point change.","error")
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            # Look up and lock exactly one driver/company balance.
            # EXISTS Prevents sponsors from changing another company's balance
            cursor.execute("""
                SELECT
                    b.BALANCE_ID,
                    b.DRIVER_ID,
                    b.SPONSORCOMP_ID,
                    b.BALANCE
                FROM BALANCE AS b
                WHERE b.DRIVER_ID = %s
                  AND b.SPONSORCOMP_ID = %s
                  AND b.IS_ACTIVE = 1
                  AND (
                      %s = 1
                      OR EXISTS (
                          SELECT 1
                          FROM SPONSOR AS s
                          WHERE s.USER_ID = %s
                            AND s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                      )
                  )
                FOR UPDATE
            """, (
                driver_id,
                balance_company_id,
                1 if is_admin else 0,
                actor_user_id
            ))

            balance = cursor.fetchone()

            if balance is None:
                conn.rollback()
                flash("That driver/company balance was not found or you "
                    "are not authorized to change it.",
                    "error"
                )
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            current_balance = float(balance["BALANCE"] or 0)
            signed_amount = (
                amount if action == "add" else -amount
            )
            new_balance = current_balance + signed_amount

            if new_balance < 0:
                conn.rollback()
                flash(
                    f"This balance has {current_balance:g} points. "
                    f"You cannot subtract {amount} points.",
                    "error"
                )
                return redirect(url_for(
                    "assignPoints",
                    sponsorcomp_id=selected_company_raw
                ))

            cursor.execute("""
                UPDATE BALANCE
                SET BALANCE = %s
                WHERE DRIVER_ID = %s
                  AND SPONSORCOMP_ID = %s
                  AND IS_ACTIVE = 1
            """, (
                new_balance,
                driver_id,
                balance_company_id
            ))

            cursor.execute("""
                INSERT INTO POINTCHANGES (
                    BALANCE_ID,
                    DRIVER_ID,
                    POINTCHANGE_AMOUNT,
                    POINTCHANGE_REASON,
                    USER_ID
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                balance["BALANCE_ID"],
                balance["DRIVER_ID"],
                signed_amount,
                reason,
                actor_user_id
            ))

            pointchange_id = cursor.lastrowid

            # look up driver user account by sponsor company name
            cursor.execute("""
                SELECT d.USER_ID AS DRIVER_USER_ID,
                    sc.SPONSORCOMP_NAME
                FROM DRIVER AS d
                JOIN SPONSORCOMP AS sc
                    ON sc.SPONSORCOMP_ID = %s
                WHERE d.DRIVER_ID = %s
            """, (
                balance["SPONSORCOMP_ID"],
                balance["DRIVER_ID"]
            ))

            driver_info = cursor.fetchone()

            if driver_info:
                driver_user_id = driver_info["DRIVER_USER_ID"]
                company_name = driver_info["SPONSORCOMP_NAME"]

                #notify driver
                if signed_amount > 0:
                    driver_type = "POINTS_GAINED"
                    driver_title = "You earned points!"
                    driver_message = (
                        f"You received {signed_amount} points from "
                        f"{company_name}. Reason: {reason}. "
                        f"Your new balance is {new_balance:g} points."
                    )
                else:
                    driver_type = "POINTS_LOST"
                    driver_title = "Your points changed"
                    driver_message = (
                        f"{abs(signed_amount)} points were deducted by "
                        f"{company_name}. Reason: {reason}. "
                        f"Your new balance is {new_balance:g} points."
                    )
                            
                create_notification(
                    cursor,
                    driver_user_id,
                    driver_type,
                    driver_title,
                    driver_message,
                    pointchange_id=pointchange_id
                )

                # notify sponsor associated with company
                cursor.execute("""
                    SELECT USER_ID
                    FROM SPONSOR
                    WHERE SPONSORCOMP_ID = %s
                """, (balance["SPONSORCOMP_ID"],))

                sponsor_users = cursor.fetchall()

                for sponsor_user in sponsor_users:
                    create_notification(
                        cursor,
                        sponsor_user["USER_ID"],
                        "SPONSOR_POINT_CHANGE",
                        "Driver points Updated",
                        f"{abs(signed_amount)} points were "
                        f"{'added to' if signed_amount > 0 else 'deducted from'} "
                        f"a driver's balance at {company_name}. "
                        f"Reason: {reason}. "
                        f"New balance: {new_balance:g} points.",
                        pointchange_id=pointchange_id
                    )

                # notify admin
                cursor.execute("""
                    SELECT USER_ID
                    FROM USER
                    WHERE ROLE = 'Admin'
                """)

                admin_users = cursor.fetchall()

                for admin_user in admin_users:
                    create_notification(
                        cursor,
                        admin_user["USER_ID"],
                        "ADMIN_POINT_CHANGE",
                        "Driver points Updated",
                        f"{abs(signed_amount)} points were "
                        f"{'added to' if signed_amount > 0 else 'deducted from'} "
                        f"a driver's balance at {company_name}. "
                        f"Reason: {reason}. "
                        f"New balance: {new_balance:g} points.",
                        pointchange_id=pointchange_id
                    )

            conn.commit()

            flash(
                f"Successfully "
                f"{'added' if action == 'add' else 'subtracted'} "
                f"{amount} points.",
                "success"
            )

            return redirect(url_for(
                "assignPoints",
                sponsorcomp_id=selected_company_raw
            ))

        # Load driver balances
        driver_query = """
            SELECT
                d.DRIVER_ID,
                d.USER_ID,
                b.BALANCE,
                b.SPONSORCOMP_ID,
                sc.SPONSORCOMP_NAME,
                u.USER_FNAME,
                u.USER_LNAME,
                u.EMAIL,
                latest.POINTCHANGE_AMOUNT AS LAST_CHANGE_AMOUNT,
                latest.POINTCHANGE_REASON AS LAST_CHANGE_REASON,
                latest.DTS AS LAST_CHANGE_DTS
            FROM DRIVER AS d
            JOIN BALANCE AS b
                ON b.DRIVER_ID = d.DRIVER_ID
            JOIN SPONSORCOMP AS sc
                ON sc.SPONSORCOMP_ID = b.SPONSORCOMP_ID
            JOIN `USER` AS u
                ON u.USER_ID = d.USER_ID
            LEFT JOIN POINTCHANGES AS latest
                ON latest.POINTCHANGE_ID = (
                    SELECT p.POINTCHANGE_ID
                    FROM POINTCHANGES AS p
                    WHERE p.DRIVER_ID = d.DRIVER_ID
                    ORDER BY p.DTS DESC, p.POINTCHANGE_ID DESC
                    LIMIT 1
                )
            WHERE b.IS_ACTIVE = 1
        """

        if is_admin:
            if selected_company_id is not None:
                cursor.execute(
                    driver_query + """
                        AND b.SPONSORCOMP_ID = %s
                        ORDER BY u.USER_LNAME, u.USER_FNAME, d.DRIVER_ID
                    """,
                    (selected_company_id,)
                )
            else:
                cursor.execute(
                    driver_query + """
                        ORDER BY u.USER_LNAME, u.USER_FNAME, d.DRIVER_ID
                    """
                )
        else:
            cursor.execute(
                driver_query + """
                    AND EXISTS (
                        SELECT 1
                        FROM SPONSOR AS s
                        WHERE s.USER_ID = %s
                          AND s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                    )
                    ORDER BY u.USER_LNAME, u.USER_FNAME, d.DRIVER_ID
                """,
                (actor_user_id,)
            )

        drivers = cursor.fetchall()

        # Load point change history
        history_query = """
            SELECT
                p.POINTCHANGE_ID,
                p.DRIVER_ID,
                p.POINTCHANGE_AMOUNT,
                p.POINTCHANGE_REASON,
                p.DTS
            FROM POINTCHANGES AS p
            WHERE EXISTS (
                SELECT 1
                FROM BALANCE AS b
                WHERE b.DRIVER_ID = p.DRIVER_ID
        """

        history_params = []

        if is_admin and selected_company_id is not None:
            history_query += """
                  AND b.SPONSORCOMP_ID = %s
            """
            history_params.append(selected_company_id)

        elif not is_admin:
            history_query += """
                  AND EXISTS (
                      SELECT 1
                      FROM SPONSOR AS s
                      WHERE s.USER_ID = %s
                        AND s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                  )
            """
            history_params.append(actor_user_id)

        history_query += """
            )
            ORDER BY p.DTS DESC, p.POINTCHANGE_ID DESC
        """

        cursor.execute(history_query, tuple(history_params))
        history_rows = cursor.fetchall()

        history_by_driver = {}
        for change in history_rows:
            history_by_driver.setdefault(
                change["DRIVER_ID"], []
            ).append(change)

        # Load the company dropdown/filter
        if is_admin:
            cursor.execute("""
                SELECT SPONSORCOMP_ID, SPONSORCOMP_NAME
                FROM SPONSORCOMP
                ORDER BY SPONSORCOMP_NAME
            """)
        else:
            cursor.execute("""
                SELECT DISTINCT sc.SPONSORCOMP_ID, sc.SPONSORCOMP_NAME
                FROM SPONSOR AS s
                JOIN SPONSORCOMP AS sc
                    ON sc.SPONSORCOMP_ID = s.SPONSORCOMP_ID
                WHERE s.USER_ID = %s
                ORDER BY sc.SPONSORCOMP_NAME
            """, (actor_user_id,))

        sponsor_companies = cursor.fetchall()

        # Current conversion rate (sponsors only)
        rate_dollars, rate_points = 1, 1
        if not is_admin:
            cursor.execute("""
                SELECT sc.SPONSORCOMP_DOLLAR, sc.SPONSORCOMP_POINT
                FROM SPONSOR AS s
                JOIN SPONSORCOMP AS sc ON sc.SPONSORCOMP_ID = s.SPONSORCOMP_ID
                WHERE s.USER_ID = %s
                LIMIT 1
            """, (actor_user_id,))
            rate_row = cursor.fetchone()
            if rate_row and rate_row["SPONSORCOMP_DOLLAR"] and rate_row["SPONSORCOMP_POINT"]:
                rate_dollars = float(rate_row["SPONSORCOMP_DOLLAR"])
                rate_points = float(rate_row["SPONSORCOMP_POINT"])

        return render_template(
            "assignPoints.html",
            drivers=drivers,
            history_by_driver=history_by_driver,
            is_admin=is_admin,
            sponsor_companies=sponsor_companies,
            selected_company_id=selected_company_id,
            rate_dollars=rate_dollars,
            rate_points=rate_points
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
        return redirect(url_for('auth.login'))

    # Get sponsor comps
    cursor.execute("""
        SELECT *
        FROM SPONSORCOMP
        ORDER BY SPONSORCOMP_NAME
    """)

    sponsor_companies = cursor.fetchall()

    # Get drivers
    cursor.execute("""CALL ADMIN_GET_DRIVERS()""")
    drivers = cursor.fetchall()
    # Pass cursor to next set because stored procedure returns results 
    # and status of stored proecure
    while cursor.nextset():
        pass

    # Get sponsors
    cursor.execute("""CALL ADMIN_GET_SPONSORS()""")
    sponsors = cursor.fetchall()
    # Pass cursor to next set because stored procedure returns results 
    # and status of stored proecure
    while cursor.nextset():
        pass

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
        return redirect(url_for('auth.login'))

    # Get sponsors
    cursor.execute("""CALL ADMIN_GET_SPONSORS()""")
    sponsors = cursor.fetchall()
    # Pass cursor to next set because stored procedure returns results 
    # and status of stored proecure
    while cursor.nextset():
        pass
    
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
        return redirect(url_for('auth.login'))
    
    # Get sponsor comps
    cursor.execute("""
        SELECT *
            FROM SPONSORCOMP
            ORDER BY SPONSORCOMP_NAME
        """)
    sponsor_companies = cursor.fetchall()
    
    # Get drivers
    cursor.execute("""CALL ADMIN_GET_DRIVERS()""")
    drivers = cursor.fetchall()
    # Pass cursor to next set because stored procedure returns results 
    # and status of stored proecure
    while cursor.nextset():
        pass

    cursor.close()
    conn.close()
    
    return render_template(
        'adminDrivers.html',
        drivers=drivers,
        sponsor_companies=sponsor_companies
    )


@app.route("/adminDash/reports", methods=["GET", "POST"])
def adminReports():

    # required login
    if "user_id" not in session:
            return redirect(url_for("login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    
    try:
        # verify the loggin in user is admin
        cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (session["user_id"],)
        )
        user = cursor.fetchone()

        if not user or user["ROLE"] != "Admin":
            return "Unauthorized", 403

        if request.method == "POST":
            sponsorcomp_id = request.form.get("sponsorcomp_id", "")
            start_text = request.form.get("start_date", "")
            end_text = request.form.get("end_date", "")

            # validate submitted form
            try:
                sponsorcomp_id = int(sponsorcomp_id)
                start_date = date.fromisoformat(start_text)
                end_date = date.fromisoformat(end_text)
            except (ValueError, TypeError):
                flash("Please select a sponsor and valid dates.", "error")
                return redirect(url_for("adminReports") + "#invoice")
            
            if start_date > end_date:
                flash("The end date must be on or after the start date.", "error")
                return redirect(url_for("adminReports") + "#invoice")

            cursor.execute(
                """
                SELECT SPONSORCOMP_ID
                FROM SPONSORCOMP
                WHERE SPONSORCOMP_ID = %s
                """,
                (sponsorcomp_id,)
            )

            if cursor.fetchone() is None:
                flash("The selected sponsor company was not found.", "error")
                return redirect(url_for("adminReports") + "#invoice")

            # get itemized purchases for this sponsor and date range
            # only completed orders count as purchases
            cursor.execute(
                """
                SELECT
                    o.ORDER_ID,
                    o.DRIVER_ID,
                    o.ORDER_DTS,
                    io.ITEM_NAME,
                    io.ITEM_AMOUNT,
                    io.ITEM_PRICE,
                    (io.ITEM_AMOUNT * io.ITEM_PRICE) AS LINE_TOTAL
                FROM ORDERS AS o
                JOIN DRIVER AS d
                    ON d.DRIVER_ID = o.DRIVER_ID
                JOIN BALANCE AS b
                    ON d.DRIVER_ID = b.DRIVER_ID
                    AND b.SPONSORCOMP_ID = %s
                    AND b.IS_ACTIVE = 1
                JOIN ITEMIZEDORDER AS io
                    ON io.ORDER_ID = o.ORDER_ID
                WHERE LOWER(o.ORDER_STATUS) = 'done'
                    AND o.ORDER_DTS >= %s
                    AND o.ORDER_DTS < DATE_ADD(%s, INTERVAL 1 DAY)
                ORDER BY o.DRIVER_ID, o.ORDER_ID, io.ITEMIZED_ID
                """,
                (sponsorcomp_id, start_date, end_date)
            )

            purchase_rows = cursor.fetchall()

            if not purchase_rows:
                flash ("No completed itemized purchases were found for that sponsor and date range. No invoice was created.", "error")
                return redirect(url_for("adminReports") + "#invoice")

            # calculate invoice total
            total_fee = sum (
                (Decimal(str(row["LINE_TOTAL"])) for row in purchase_rows),
                Decimal("0.00")
            )

            try:
                # save the invoice header
                cursor.execute(
                    """
                    INSERT INTO INVOICE (
                        SPONSORCOMP_ID,
                        PERIOD_START,
                        PERIOD_END,
                        TOTAL_FEE
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (sponsorcomp_id, start_date, end_date, total_fee)
                )

                invoice_id = cursor.lastrowid

                # save each item as an invoice detail
                for row in purchase_rows:
                    cursor.execute(
                        """
                        INSERT INTO INVOICEDETAIL (
                            INVOICE_ID,
                            ORDER_ID,
                            DRIVER_ID,
                            ITEM_NAME,
                            ITEM_AMOUNT,
                            ITEM_PRICE,
                            LINE_TOTAL
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            invoice_id,
                            row["ORDER_ID"],
                            row["DRIVER_ID"],
                            row["ITEM_NAME"],
                            row["ITEM_AMOUNT"],
                            row["ITEM_PRICE"],
                            row["LINE_TOTAL"]
                        )
                    )
                
                conn.commit()
            
            except Exception:
                conn.rollback()
                raise
            
            flash(f"Invoice #{invoice_id} was generated successfully.", "success")
            return redirect(url_for("adminReports") + "#invoice")

        # load sponsor companies for dropdown
        cursor.execute(
            """
            SELECT SPONSORCOMP_ID, SPONSORCOMP_NAME
            FROM SPONSORCOMP
            ORDER BY SPONSORCOMP_NAME
            """
        )
        sponsor_companies = cursor.fetchall()

        # load previously generated invoices
        cursor.execute(
            """
            SELECT
                i.INVOICE_ID,
                i.PERIOD_START,
                i.PERIOD_END,
                i.GENERATED_DTS,
                i.TOTAL_FEE,
                sc.SPONSORCOMP_NAME
            FROM INVOICE AS i
            JOIN SPONSORCOMP AS sc
                ON sc.SPONSORCOMP_ID = i.SPONSORCOMP_ID
            ORDER BY i.GENERATED_DTS DESC, i.INVOICE_ID DESC
            """
        )
        invoices = cursor.fetchall()
        
        # Load drivers and sponsors for report filtering
        cursor.callproc("GET_REPORT_USERS") # MySQL stored procedure

        report_users = []

        # Retrieve the result sets and add each row to list
        for result in cursor.stored_results():
            report_users.extend(result.fetchall())

        # Default report values
        report_type = "summary"
        report_role = "Driver"
        report_rows = []
        # Since no report at default, report_generated = false
        report_generated = (
            request.args.get("run_report") == "1"
        )

        selected_sponsorcomp_id = None
        selected_user_id = None
        selected_start_date = ""
        selected_end_date = ""

        # Generate report if requested
        if report_generated:
            # Retrieve all variables/values from UI
            try:
                report_filters = parseOrderReportFilters(
                    request.args
                )

                report_type = report_filters["report_type"]
                report_role = report_filters["role"]

                selected_sponsorcomp_id = (
                    report_filters["sponsorcomp_id"]
                )

                selected_user_id = (
                    report_filters["user_id"]
                )

                selected_start_date = (
                    str(report_filters["start_date"])
                    if report_filters["start_date"]
                    else ""
                )

                selected_end_date = (
                    str(report_filters["end_date"])
                    if report_filters["end_date"]
                    else ""
                )
                # Get Report using dictionary
                report_rows = getOrderReportRows(
                    **report_filters
                )

            except (ValueError, TypeError):
                flash(
                    "Invalid report filters.",
                    "error"
                )

                return redirect(
                    url_for("adminReports") + "#sales-drivers"
                )

        return render_template(
            "adminReports.html",

            # Existing invoice variables
            sponsor_companies=sponsor_companies,
            invoices=invoices,

            # Report variables
            report_users=report_users,
            report_type=report_type,
            report_role=report_role,
            report_rows=report_rows,
            report_generated=report_generated,

            # Selected filters
            selected_sponsorcomp_id=selected_sponsorcomp_id,
            selected_user_id=selected_user_id,
            selected_start_date=selected_start_date,
            selected_end_date=selected_end_date
        )

    finally:
        cursor.close()
        conn.close()

@app.route("/adminDash/invoices/<int:invoice_id>")
def viewInvoice(invoice_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    
    try:
        # verify the loggin in user is admin
        cursor.execute(
            "SELECT ROLE FROM USER WHERE USER_ID = %s",
            (session["user_id"],)
        )
        user = cursor.fetchone()

        if not user or user["ROLE"] != "Admin":
            return "Unauthorized", 403

        # get saved invoice header
        cursor.execute(
            """
            SELECT
                i.INVOICE_ID,
                i.PERIOD_START,
                i.PERIOD_END,
                i.GENERATED_DTS,
                i.TOTAL_FEE,
                sc.SPONSORCOMP_NAME
            FROM INVOICE AS i
            JOIN SPONSORCOMP AS sc
                ON sc.SPONSORCOMP_ID = i.SPONSORCOMP_ID
            WHERE i.INVOICE_ID = %s
            """,
            (invoice_id,)
        )
        invoice = cursor.fetchone()

        if invoice is None:
            return "Invoice not found", 404

        # get individual saved purchase lines
        cursor.execute(
            """
            SELECT
                id.ORDER_ID,
                id.DRIVER_ID,
                u.USER_FNAME,
                u.USER_LNAME,
                id.ITEM_NAME,
                id.ITEM_AMOUNT,
                id.ITEM_PRICE,
                id.LINE_TOTAL
            FROM INVOICEDETAIL AS id
            JOIN DRIVER AS d
                ON d.DRIVER_ID = id.DRIVER_ID
            JOIN USER AS u
                ON u.USER_ID = d.USER_ID
            WHERE id.INVOICE_ID = %s
            ORDER BY u.USER_LNAME, u.USER_FNAME, id.ORDER_ID,
                id.INVOICEDETAIL_ID
            """,
            (invoice_id,)
        )
        details = cursor.fetchall()

        # summarize each driver's purchases for the invoice
        cursor.execute(
            """
            SELECT
                id.DRIVER_ID,
                u.USER_FNAME,
                u.USER_LNAME,
                COUNT(DISTINCT id.ORDER_ID) AS PURCHASE_COUNT,
                SUM(id.LINE_TOTAL) AS DRIVER_TOTAL
            FROM INVOICEDETAIL AS id
            JOIN DRIVER AS d
                ON d.DRIVER_ID = id.DRIVER_ID
            JOIN USER AS u
                ON u.USER_ID = d.USER_ID
            WHERE id.INVOICE_ID = %s
            GROUP BY
                id.DRIVER_ID, u.USER_FNAME, u.USER_LNAME
            ORDER BY u.USER_LNAME, u.USER_FNAME
            """,
            (invoice_id,)
        )
        driver_summaries = cursor.fetchall()

        return render_template(
            "invoiceDetail.html",
            invoice=invoice,
            details=details,
            driver_summaries=driver_summaries
        )

    finally:
        cursor.close()
        conn.close()
    

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
        return redirect(url_for('auth.login'))

    cursor.callproc(
        "GET_LOGIN_ATTEMPTS_AUDIT",
        (None, None)
    )
        
    login_attempts = []
        
    for result in cursor.stored_results():
        login_attempts.extend(result.fetchall())

    cursor.callproc(
        "GET_PASSWORD_CHANGES_AUDIT",
        (None, None)
    )
            
    password_changes = []
            
    for result in cursor.stored_results():
        password_changes.extend(result.fetchall())

    cursor.callproc(
        "GET_DRIVER_APPLICATIONS_AUDIT",
        (None, None, None)
    )
    
    driver_applications = []
    
    for result in cursor.stored_results():
        driver_applications.extend(result.fetchall())

    cursor.callproc(
        "GET_POINT_CHANGES_AUDIT",
        (None, None, None, None)
    )

    point_changes = []

    for result in cursor.stored_results():
        point_changes.extend(result.fetchall())

    cursor.execute("""
            SELECT SPONSORCOMP_ID, SPONSORCOMP_NAME
            FROM SPONSORCOMP
            ORDER BY SPONSORCOMP_NAME
            """)
    sponsor_companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'adminAudit.html',
        login_attempts=login_attempts,
        password_changes=password_changes,
        driver_applications=driver_applications,
        point_changes=point_changes,
        sponsor_companies=sponsor_companies
    )

@app.route("/sponDash/audit")
def sponsorAudit():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
    cursor = conn.cursor(dictionary=True)

    try:
        # Get the sponsor company associated with the logged-in user.
        cursor.execute("""
            SELECT
                s.SPONSOR_ID,
                s.SPONSORCOMP_ID,
                sc.SPONSORCOMP_NAME
            FROM SPONSOR s
            JOIN USER u
                ON u.USER_ID = s.USER_ID
            JOIN SPONSORCOMP sc
                ON sc.SPONSORCOMP_ID = s.SPONSORCOMP_ID
            WHERE s.USER_ID = %s
              AND u.ROLE = 'Sponsor'
        """, (user_id,))

        sponsor = cursor.fetchone()

        if not sponsor:
            flash("You are not authorized to view these audit logs.", "error")
            return redirect(url_for("sponDash"))

        sponsorcomp_id = sponsor["SPONSORCOMP_ID"]

        # Get all driver application data for sponsor company
        cursor.callproc(
            "GET_DRIVER_APPLICATIONS_AUDIT",
            (sponsorcomp_id, None, None)
        )
            
        applications = []
            
        for result in cursor.stored_results():
            applications.extend(result.fetchall())

        # grab all point changes for sponsor company
        cursor.callproc(
            "GET_POINT_CHANGES_AUDIT",
            (sponsorcomp_id, None, None, None)
        )
        
        point_changes = []
    
        for result in cursor.stored_results():
            point_changes.extend(result.fetchall())

        # Get drivers associated with this sponsor company.
        cursor.execute("""
            SELECT DISTINCT
                d.DRIVER_ID,
                u.EMAIL AS DRIVER_EMAIL
            FROM DRIVER d
            JOIN USER u
                ON u.USER_ID = d.USER_ID
            JOIN BALANCE b
                ON b.DRIVER_ID = d.DRIVER_ID
            WHERE b.SPONSORCOMP_ID = %s
                AND b.IS_ACTIVE = 1
            ORDER BY u.EMAIL
        """, (sponsorcomp_id,))

        drivers = cursor.fetchall()

        return render_template(
            "sponsorAudit.html",
            sponsor=sponsor,
            applications=applications,
            point_changes=point_changes,
            drivers=drivers
        )

    finally:
        cursor.close()
        conn.close()

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
                SELECT b.DRIVER_ID
                FROM BALANCE AS b
                JOIN SPONSOR AS s
                    ON s.SPONSORCOMP_ID = b.SPONSORCOMP_ID
                WHERE b.DRIVER_ID = %s
                  AND s.USER_ID = %s
                  AND b.IS_ACTIVE = 1
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


@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT
                NOTIFICATION_ID,
                NOTIFICATION_TYPE,
                TITLE,
                MESSAGE,
                IS_READ,
                CREATED_DTS
            FROM NOTIFICATIONS
            WHERE USER_ID = %s
            ORDER BY CREATED_DTS DESC, NOTIFICATION_ID DESC
        """, (session["user_id"],))

        user_notifications = cursor.fetchall()

        return render_template(
            "notifications.html",
            notifications=user_notifications
        )

    finally:
        cursor.close()
        conn.close()

@app.route("/notifications/mark-read/<int:notification_id>", methods=["POST"])
def mark_notifications_read(notification_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE NOTIFICATIONS
            SET IS_READ = 1
            WHERE NOTIFICATION_ID = %s
                AND USER_ID = %s
        """, (notification_id, session["user_id"]))

        conn.commit()

    except mysql.connector.Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("notifications"))

@app.route("/notifications/settings", methods=["GET", "POST"])
def notification_settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    role = session.get("role")

    # only get notification types that apply to the user's role
    allowed_types = ROLE_NOTIFICATION_TYPES.get(role)
    if allowed_types is None:
        return "Unauthorized", 403

    # filter the full notification dictionary by the user's role
    user_notification_types = {
        notification_type: label
        for notification_type, label in NOTIFICATION_TYPES.items()
        if notification_type in allowed_types
    }

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)
    
    try:
        if request.method == "POST":
            for notification_type in user_notification_types:
                is_enabled = (
                    1 if request.form.get(notification_type) == "1"
                    else 0
                )

                cursor.execute("""
                    INSERT INTO NOTIFICATIONSETTINGS
                        (USER_ID, NOTIFICATION_TYPE, IS_ENABLED)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        IS_ENABLED = VALUES(IS_ENABLED),
                        UPDATED_DTS = CURRENT_TIMESTAMP
                """, (user_id, notification_type, is_enabled))

            conn.commit()
            flash("Notification settings saved successfully.", "success")

            return redirect(url_for("notification_settings"))
        
        cursor.execute("""
            SELECT NOTIFICATION_TYPE, IS_ENABLED
            FROM NOTIFICATIONSETTINGS
            WHERE USER_ID = %s
        """, (user_id,))

        saved_settings = {
            row["NOTIFICATION_TYPE"]: bool(row["IS_ENABLED"])
            for row in cursor.fetchall()
        }

        # without saved preferences all notifs enabled
        settings = {
            notification_type: saved_settings.get(notification_type, True)
            for notification_type in user_notification_types
        }

        return render_template(
            "notification_settings.html",
            notification_types=user_notification_types,
            settings=settings
        )

    except mysql.connector.Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

@app.context_processor
def inject_unread_notification_count():
    if "user_id" not in session:
        return {"unread_notification_count": 0}

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT COUNT(*) AS unread_count
            FROM NOTIFICATIONS
            WHERE USER_ID = %s
            AND IS_READ = 0
        """, (session["user_id"],))

        result = cursor.fetchone()

        return {
            "unread_notification_count": int(result["unread_count"])
        }
    
    finally:
        cursor.close()
        conn.close()

@app.route("/bulkUpload", methods=["POST"])
def bulkUpload():

    # Only Admins and Sponsors can upload files
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_role = session.get("role")

    if user_role not in ("Admin", "Sponsor"):
        return "Unauthorized", 403

    uploaded_file = request.files.get("file")

    if uploaded_file is None or uploaded_file.filename == "":
        return render_template(
            "bulk_upload_results.html",
            results=[],
            errors=["Please select a file to upload."]
        )

    # Validate the file before processing records
    valid_records, errors = validate_bulk_upload(
        uploaded_file,
        user_role
    )

    results = []
    upload_errors = list(errors)

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

    try:

        # Sponsors can only upload to their own organization
        sponsor_company_id = None

        if user_role == "Sponsor":

            cursor.execute("""
                SELECT SPONSORCOMP_ID
                FROM SPONSOR
                WHERE USER_ID = %s
            """, (session["user_id"],))

            sponsor = cursor.fetchone()

            if sponsor is None:
                return "Sponsor organization not found.", 403

            sponsor_company_id = sponsor["SPONSORCOMP_ID"]

        # Tracks organizations created earlier in this upload
        created_organizations = {}

        # Process records in their original file order
        valid_records.sort(key=lambda record: record["line_number"])

        for record in valid_records:

            line_number = record["line_number"]
            record_type = record["type"]

            try:

                # Each line is processed independently
                if record_type == "O":

                    if user_role != "Admin":
                        upload_errors.append(
                            f"Line {line_number}: Only Admins can create organizations."
                        )
                        continue

                    organization_name = record["organization"]

                    cursor.execute("""
                        SELECT SPONSORCOMP_ID
                        FROM SPONSORCOMP
                        WHERE SPONSORCOMP_NAME = %s
                    """, (organization_name,))

                    existing_organizations = cursor.fetchall()

                    if existing_organizations:
                        raise ValueError(
                            f"Organization '{organization_name}' already exists."
                        )

                    cursor.execute("""
                        INSERT INTO SPONSORCOMP (
                            SPONSORCOMP_NAME,
                            SPONSORCOMP_DOLLAR,
                            SPONSORCOMP_POINT
                        )
                        VALUES (%s, %s, %s)
                    """, (organization_name, 1, 10))

                    organization_id = cursor.lastrowid

                    conn.commit()

                    created_organizations[organization_name] = organization_id

                    results.append({
                        "message": f"Line {line_number}: Created organization '{organization_name}'.",
                        "email": "N/A",
                        "temporary_password": None
                    })

                    continue

                # Determine which organization this user belongs to
                if user_role == "Sponsor":

                    organization_id = sponsor_company_id

                else:

                    organization_name = record["organization"]

                    if not organization_name:
                        raise ValueError(
                            "An organization name is required for Admin uploads."
                        )

                    # First check organizations created earlier in this file
                    organization_id = created_organizations.get(
                        organization_name
                    )

                    # Otherwise, check the database
                    if organization_id is None:

                        cursor.execute("""
                            SELECT SPONSORCOMP_ID
                            FROM SPONSORCOMP
                            WHERE SPONSORCOMP_NAME = %s
                        """, (organization_name,))

                        organizations = cursor.fetchall()

                        if len(organizations) == 0:
                            raise ValueError(
                                f"Organization '{organization_name}' does not exist."
                            )

                        if len(organizations) > 1:
                            raise ValueError(
                                f"Organization '{organization_name}' is ambiguous."
                            )

                        organization_id = organizations[0]["SPONSORCOMP_ID"]

                email = record["email"]
                first_name = record["first_name"]
                last_name = record["last_name"]

                # Look for an existing user by email
                cursor.execute("""
                    SELECT USER_ID, ROLE
                    FROM `USER`
                    WHERE EMAIL = %s
                """, (email,))

                existing_user = cursor.fetchone()

                new_password = None

                # Create the user if they do not already exist
                if existing_user is None:

                    new_password = "123_password"

                    password_hash = generate_password_hash(new_password)

                    expected_role = (
                        "Driver" if record_type == "D" else "Sponsor"
                    )

                    cursor.execute("""
                        INSERT INTO USER (
                            USER_FNAME,
                            USER_LNAME,
                            ROLE,
                            EMAIL,
                            PASSWORD
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        first_name,
                        last_name,
                        expected_role,
                        email,
                        password_hash
                    ))

                    user_id = cursor.lastrowid

                else:

                    user_id = existing_user["USER_ID"]

                    expected_role = (
                        "Driver" if record_type == "D" else "Sponsor"
                    )

                    if existing_user["ROLE"] != expected_role:
                        raise ValueError(
                            f"{email} already belongs to a user with role "
                            f"'{existing_user['ROLE']}'."
                        )

                # -------------------------------------------------
                # SPONSOR RECORD
                # -------------------------------------------------
                if record_type == "S":

                    cursor.execute("""
                        SELECT SPONSORCOMP_ID
                        FROM SPONSOR
                        WHERE USER_ID = %s
                    """, (user_id,))

                    existing_sponsor = cursor.fetchone()

                    if existing_sponsor:

                        if existing_sponsor["SPONSORCOMP_ID"] != organization_id:
                            raise ValueError(
                                "This Sponsor already belongs to another organization."
                            )

                        message = f"Line {line_number}: Sponsor {email} already exists."

                    else:

                        cursor.execute("""
                            INSERT INTO SPONSOR (
                                USER_ID,
                                SPONSORCOMP_ID
                            )
                            VALUES (%s, %s)
                        """, (user_id, organization_id))

                        message = f"Line {line_number}: Created Sponsor {email}."

                # -------------------------------------------------
                # DRIVER RECORD
                # -------------------------------------------------
                elif record_type == "D":

                    cursor.execute("""
                        SELECT DRIVER_ID
                        FROM DRIVER
                        WHERE USER_ID = %s
                    """, (user_id,))

                    existing_driver = cursor.fetchone()

                    if existing_driver:

                        driver_id = existing_driver["DRIVER_ID"]

                    else:

                        cursor.execute("""
                            INSERT INTO DRIVER (USER_ID)
                            VALUES (%s)
                        """, (user_id,))

                        driver_id = cursor.lastrowid

                    # Find or create this driver's balance
                    cursor.execute("""
                        SELECT BALANCE_ID, BALANCE
                        FROM BALANCE
                        WHERE DRIVER_ID = %s
                        AND SPONSORCOMP_ID = %s
                        AND IS_ACTIVE = 1
                    """, (driver_id, organization_id))

                    balance_record = cursor.fetchone()

                    if balance_record is None:

                        cursor.execute("""
                            INSERT INTO BALANCE (
                                DRIVER_ID,
                                SPONSORCOMP_ID,
                                BALANCE,
                                IS_ACTIVE
                            )
                            VALUES (%s, %s, %s, %s)
                        """, (driver_id, organization_id, 0, 1))

                        balance_id = cursor.lastrowid

                    else:

                        balance_id = balance_record["BALANCE_ID"]

                    # Add optional points to the driver's balance
                    points = record["points"]

                    if points is not None:

                        # POINTCHANGE_AMOUNT is an INT in your database
                        if not float(points).is_integer():
                            raise ValueError(
                                "Points must be a whole number."
                            )

                        points = int(points)

                        cursor.execute("""
                            UPDATE BALANCE
                            SET BALANCE = BALANCE + %s
                            WHERE BALANCE_ID = %s
                                AND IS_ACTIVE = 1
                        """, (points, balance_id))

                        cursor.execute("""
                            INSERT INTO POINTCHANGES (
                                DRIVER_ID,
                                POINTCHANGE_AMOUNT,
                                POINTCHANGE_REASON,
                                USER_ID,
                                BALANCE_ID
                            )
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            driver_id,
                            points,
                            record["reason"],
                            session["user_id"],
                            balance_id
                        ))

                    message = f"Line {line_number}: Created/updated Driver {email}."

                # Commit this record before moving to the next line
                conn.commit()

                # Show the temporary password only for newly created accounts
                if new_password:
                    results.append({
                        "message": message,
                        "email": email,
                        "temporary_password": new_password
                    })
                else:
                    results.append({
                        "message": message,
                        "email": email,
                        "temporary_password": None
                    })

            except (mysql.connector.Error, ValueError) as e:

                # Undo only the current record; continue with the next line
                conn.rollback()

                upload_errors.append(
                    f"Line {line_number}: {str(e)}"
                )

    finally:

        cursor.close()
        conn.close()

    return render_template(
        "bulk_upload_results.html",
        results=results,
        errors=upload_errors
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)