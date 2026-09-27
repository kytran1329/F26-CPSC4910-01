from flask import Flask, render_template, request, redirect
import mysql.connector 
import os
from dotenv import load_dotenv
from catalog import search_ebay

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__, static_folder= "styles")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Not checking credentials right now
        return redirect("/home")

    return render_template("login.html")


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
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME
        )
    cursor = conn.cursor(dictionary=True)
    
        #query gets driver info
    cursor.execute("""select
                        d.DRIVER_ID,
                        u.USER_FNAME,
                        u.USER_LNAME,
                        u.ROLE,
                        u.EMAIL,
                        d.BALANCE
                    from DRIVER as d
                    join `USER` as u
                        on u.USER_ID = d.USER_ID
                    where d.DRIVER_ID = 1""")
        
    drive_info = cursor.fetchone()

    #point history
    cursor.execute("""
        SELECT
            pc.POINTCHANGE_ID,
            pc.POINTCHANGE_AMOUNT,
            pc.POINTCHANGE_REASON,
            pc.DTS
        FROM POINTCHANGES AS pc
        WHERE pc.USER_ID = (
            SELECT d.USER_ID
            FROM DRIVER AS d
            WHERE d.DRIVER_ID = %s
        )
        ORDER BY pc.DTS DESC;
            """, (drive_info["DRIVER_ID"],))

    history = cursor.fetchall()

    #order and status
    cursor.execute("""
        SELECT 
            ORDER_ID,
            DRIVER_ID,
            POINT_TOTAL,
            ORDER_STATUS,
            ORDER_DTS
        FROM ORDERS
        WHERE DRIVER_ID = %s
        ORDER BY ORDER_DTS DESC;
            """, (drive_info["DRIVER_ID"],))

    order_stat = cursor.fetchall()

    cursor.close()
    conn.close()
    #print(drive_info)
    return render_template("driverDash.html", drive_info = drive_info,
                           history= history, order_stat = order_stat)

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

@app.route("/sponDash")
def sponDash():
    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
            )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""select 
                        u.USER_ID,
                        u.USER_FNAME,
                        u.USER_LNAME,
                        u.ROLE,
                        u.EMAIL,
                        d.DRIVER_ID,
                        d.SPONSORCOMP_ID,
                        d.BALANCE,
                        p.POINTCHANGE_AMOUNT,
                        p.POINTCHANGE_REASON,
                        p.DTS
                    from `USER` as u
                    join DRIVER as d
                        on u.USER_ID = d.USER_ID
                    join POINTCHANGES as p
                        on p.USER_ID = d.USER_ID
                    order by d.DRIVER_ID, p.DTS desc""")
    user_info = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("sponsorDash.html", user_info = user_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)