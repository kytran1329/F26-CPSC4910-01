from flask import Flask, render_template
import mysql.connector 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    conn = mysql.connector.connect(
    host="cpsc4910-f26.cobd8enwsupz.us-east-1.rds.amazonaws.com",
    user="Team01",
    password="TheFellowshipoftheFuntion",
    database="Team01_DB"
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)