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
        select
            pc.POINTCHANGE_ID,
            pc.POINTCHANGE_AMOUNT,
            pc.POINTCHANGE_REASON,
            pc.DTS
        from POINTCHANGES as pc
        WHERE pc.USER_ID = (
            select d.USER_ID
            from DRIVER as d
            WHERE d.DRIVER_ID = %s
        )
        order by pc.DTS DESC;
            """, (drive_info["DRIVER_ID"],))

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
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

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
            ON u.USER_ID = d.USER_ID

        left join POINTCHANGES as p
            ON p.USER_ID = d.USER_ID

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
    cursor.execute("""
        select
            p.POINTCHANGE_ID,
            p.USER_ID,
            d.DRIVER_ID,
            u.USER_FNAME,
            u.USER_LNAME,
            p.POINTCHANGE_AMOUNT,
            p.POINTCHANGE_REASON,
            p.DTS

        from POINTCHANGES as p

        join DRIVER as d
            ON p.USER_ID = d.USER_ID

        join `USER` as u
            ON d.USER_ID = u.USER_ID

        order by d.DRIVER_ID, p.DTS DESC
    """)

    point_history = cursor.fetchall()


    cursor.close()
    conn.close()

    return render_template("sponsorDash.html",
        user_info=user_info,point_history=point_history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)