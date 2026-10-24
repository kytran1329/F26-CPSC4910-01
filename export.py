import mysql.connector
import os
from dotenv import load_dotenv
import csv
import io

from flask import Blueprint, Response, send_file

from pdf_utils import RoadRewardsPDF

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

export = Blueprint(
    "export",
    __name__,
    url_prefix="/admin/audit"
)

# SELECT * from LOGINATTEMPTS for audit log
def getLoginAttempts():
    conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT ATTEMPTED_EMAIL, RESULT, DTS
            FROM LOGINATTEMPTS
            ORDER BY DTS DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

def getPasswordChanges():
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
                U.EMAIL,
                PC.PASSWORDCHANGE_REASON AS REASON,
                PC.DTS
            FROM PASSWORDCHANGES AS PC
            INNER JOIN `USER` AS U
                ON PC.USER_ID = U.USER_ID
            ORDER BY PC.DTS DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

#Export CSV
@export.route("/login-attempts/csv")
def exportLoginAttemptsCsv():
    login_attempts = getLoginAttempts()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Email Attempted",
        "Result",
        "Date and Time"
    ])

    for attempt in login_attempts:
        writer.writerow([
            attempt["ATTEMPTED_EMAIL"] or "N/A",
            "Success" if attempt["RESULT"] else "Failure", #Success = True / Failure = False
            attempt["DTS"]
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=login_attempts_audit.csv"
        }
    )

#Export PDF
@export.route("/login-attempts/pdf")
def exportLoginAttemptsPdf():
    login_attempts = getLoginAttempts()

    pdf_buffer = io.BytesIO()

    # Common audit log/report dimensions are letter and landscape
    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(letter),
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    pdf_style = RoadRewardsPDF()

    elements = pdf_style.createHeader(
        "Login Attempts Audit Log",
        len(login_attempts)
    )

    data = [["Email Attempted","Result","Date and Time"]]

    for attempt in login_attempts:
        data.append([
            attempt["ATTEMPTED_EMAIL"] or "N/A",
            "Success" if attempt["RESULT"] else "Failure",
            str(attempt["DTS"])
        ])

    table = pdf_style.createTable(
    data,
    column_proportions=[3.5, 2, 3.5]
    )

    elements.append(table)
    document.build(elements)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="login_attempts_audit.pdf"
    )

@export.route('/password-changes/csv')
def exportPasswordChangesCsv():
    password_changes = getPasswordChanges()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Email",
        "Reason",
        "Date and Time"
    ])

    for change in password_changes:
        writer.writerow([
            change["EMAIL"] or "N/A",
            change["REASON"] or "N/A",
            change["DTS"] or "N/A"
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=password_changes_audit.csv"
        }
    )

@export.route('/password-changes/pdf')
def exportPasswordChangesPdf():
    password_changes = getPasswordChanges()
    
    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(letter)
    )

    # Reuse your shared Road Rewards branding
    pdf_style = RoadRewardsPDF()

    elements = pdf_style.createHeader(
        "Password Changes Audit Log",
        len(password_changes)
    )

    data = [[
        "Email",
        "Reason",
        "Date and Time"
    ]]

    for change in password_changes:
        data.append([
            change["EMAIL"] or "N/A",
            change["REASON"] or "N/A",
            str(change["DTS"] or "N/A")
        ])

    table = pdf_style.createTable(
    data,
    column_proportions=[3, 4, 3]
    )

    elements.append(table)
    document.build(elements)

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="password_changes_audit.pdf"
    )
