from flask import Flask, render_template
import mysql.connector 
import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__, static_folder= "styles")

@app.route("/")
def home():
    return render_template("index.html")


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
                        on u.USER_ID = d.USER_ID""")
        
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

    cursor.close()
    conn.close()
    #print(drive_info)
    return render_template("driverDash.html", drive_info = drive_info,
                           history= history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)