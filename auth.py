from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash, current_app
import mysql.connector 
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
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

            # Check whether the user exists
            if user is None:
                cursor.execute(
                """
                INSERT INTO LOGINATTEMPTS (ATTEMPTED_EMAIL, RESULT)
                VALUES (%s, %s)
                """,
                (username, False)
                )
                conn.commit()

                return render_template("login.html",error="Invalid username or password")

            global USER_ID
            USER_ID= user["USER_ID"]

            # check if hashed password matches
            if (user and check_password_hash(user["PASSWORD"], pwd)) or (user and user["PASSWORD"] == pwd):
                role = user["ROLE"]
                session["user_id"] = user["USER_ID"]
                session["role"] = user["ROLE"]

                cursor.execute(
                """
                INSERT INTO LOGINATTEMPTS (ATTEMPTED_EMAIL, RESULT)
                VALUES (%s, %s)
                """,
                (username, True)
                )

                conn.commit()

                if role == "Driver":
                    return redirect(url_for("driverDash"))
                elif role == "Sponsor":
                    return redirect(url_for("sponDash"))
                elif role == "Admin":
                    return redirect(url_for("adminDash"))
                else:
                    return redirect(url_for("home"))

            # if password doesn't match stay on the page and give an error
            cursor.execute(
            """
            INSERT INTO LOGINATTEMPTS (ATTEMPTED_EMAIL, RESULT)
            VALUES (%s, %s)
            """,
            (username, False)
            )
            conn.commit()

            return render_template( "login.html", error="Invalid username or password" )
            
        finally:
            cursor.close()
            conn.close()

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    print(session)
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # connect to sql database
    conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
        )
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
                SELECT SPONSORCOMP_ID, SPONSORCOMP_NAME
                FROM SPONSORCOMP
                ORDER BY SPONSORCOMP_NAME
                """)
    sponsor_companies = cursor.fetchall()
    
    if request.method == "POST":
        # get user info to create an account
        first_name = request.form.get("first_name") 
        last_name = request.form.get("last_name") 
        email = request.form.get("email") 
        pwd = request.form.get("password")
        sponsorcomp_id = request.form.get("sponsorcomp_id")
        role = "Driver"

        # connect to sql database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password= DB_PASSWORD,
            database= DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                    SELECT SPONSORCOMP_ID, SPONSORCOMP_NAME
                    FROM SPONSORCOMP
                    ORDER BY SPONSORCOMP_NAME
                    """)
        sponsor_companies = cursor.fetchall()

        try:
            # check if email already exists 
            cursor.execute( "SELECT USER_ID FROM `USER` WHERE EMAIL = %s", (email,) )
            if cursor.fetchone(): 
                return render_template( 
                    "signup.html", 
                    error="An account with this email already exists.",
                    sponsor_companies=sponsor_companies 
                )

            # Verify that the selected sponsor company exists
            cursor.execute("""
                SELECT SPONSORCOMP_ID
                FROM SPONSORCOMP
                WHERE SPONSORCOMP_ID = %s
            """, (sponsorcomp_id,))

            if not cursor.fetchone():
                return render_template(
                    "signup.html",
                    error="Please select a valid sponsor company.",
                    sponsor_companies=sponsor_companies
                )

            # hash the password
            hashed_password = generate_password_hash(pwd)

            # Insert the new driver
            cursor.execute(""" 
                INSERT INTO `USER` 
                (USER_FNAME, USER_LNAME, EMAIL, PASSWORD, ROLE) 
                VALUES (%s, %s, %s, %s, %s) """, 
                (first_name, last_name, email, hashed_password, "Driver")
            )

            user_id = cursor.lastrowid

            # Insert the sponsor application without an assigned sponsor user
            cursor.execute("""
                INSERT INTO APPLICATIONS
                    (USER_ID, SPONSORCOMP_ID, SPONSOR_ID)
                VALUES (%s, %s, NULL)
            """, (user_id, sponsorcomp_id))

            # Commit only after both inserts succeed
            conn.commit()

            return redirect(url_for("auth.login"))

        except mysql.connector.Error: 
            conn.rollback() 
            current_app.logger.exception("Error creating user account") 
            return render_template( 
                "signup.html", 
                error="Unable to create your account. Please try again.",
                sponsor_companies=sponsor_companies 
            )
            
        finally:
            cursor.close()
            conn.close()
    return render_template("signup.html", sponsor_companies=sponsor_companies)