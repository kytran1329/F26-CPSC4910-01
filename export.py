import mysql.connector
import os
from dotenv import load_dotenv
import csv
import io

from flask import Blueprint, Response, send_file, request

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
def getLoginAttempts(start_date=None, end_date=None):
    conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            "GET_LOGIN_ATTEMPTS_AUDIT",
            (start_date, end_date)
        )

        login_attempts = []

        for result in cursor.stored_results():
            login_attempts.extend(result.fetchall())

        return login_attempts

    finally:
        cursor.close()
        conn.close()

def getPasswordChanges(start_date=None, end_date=None):
    conn = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASSWORD,
                        database=DB_NAME
                    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            "GET_PASSWORD_CHANGES_AUDIT",
            (start_date, end_date)
        )

        password_changes = []

        for result in cursor.stored_results():
            password_changes.extend(result.fetchall())

        return password_changes

    finally:
        cursor.close()
        conn.close()

def getDriverApplications(sponsorcomp_id=None,start_date=None,end_date=None):
    conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            "GET_DRIVER_APPLICATIONS_AUDIT",
            (sponsorcomp_id, start_date, end_date)
        )

        applications = []

        for result in cursor.stored_results():
            applications.extend(result.fetchall())

        return applications
    
    finally:
            cursor.close()
            conn.close()

def getPointChangesForExport(sponsorcomp_id=None,start_date=None,end_date=None):
    conn = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASSWORD,
                        database=DB_NAME
                    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            "GET_POINT_CHANGES_AUDIT", # Tried making GET_POINT_CHANGES_AUDIT
            (sponsorcomp_id, start_date, end_date)
        )

        point_changes = []

        for result in cursor.stored_results():
            point_changes.extend(result.fetchall())

        return point_changes

    finally:
        cursor.close()
        conn.close()

#Export CSV
@export.route("/login-attempts/csv")
def exportLoginAttemptsCsv():
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    login_attempts = getLoginAttempts(start_date, end_date)

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
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    login_attempts = getLoginAttempts(start_date, end_date)

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
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    password_changes = getPasswordChanges(start_date, end_date)
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
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    password_changes = getPasswordChanges(start_date, end_date)
    
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

@export.route("/driver-applications/csv")
def exportDriverApplicationsCsv():
    sponsorcomp_id = request.args.get("sponsorcomp_id", type=int)
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    
    applications = getDriverApplications(sponsorcomp_id,start_date,end_date)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Sponsor Company",
        "Driver Email",
        "Sponsor Email",
        "Status",
        "Reason",
        "Created Date",
        "Updated Date"
    ])

    for application in applications:
        writer.writerow([
            application["SPONSORCOMP_NAME"] or "N/A",
            application["DRIVER_EMAIL"] or "N/A",
            application["SPONSOR_EMAIL"] or "N/A",
            application["STATUS"] or "N/A",
            application["REASON"] or "N/A",
            application["CREATED_DTS"] or "N/A",
            application["UPDATED_DTS"] or "N/A"
        ])

    response = Response(output.getvalue(), mimetype="text/csv")

    response.headers["Content-Disposition"] = (
        "attachment; filename=driver_applications_audit.csv"
    )

    return response
    
@export.route("/driver-applications/pdf")
def exportDriverApplicationsPdf():
    sponsorcomp_id = request.args.get("sponsorcomp_id", type=int)
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None

    applications = getDriverApplications(sponsorcomp_id,start_date,end_date)

    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(letter)
    )

    pdf_style = RoadRewardsPDF()

    elements = pdf_style.createHeader(
        "Driver Applications Audit Log",
        len(applications)
    )

    data = [[
        "Sponsor",
        "Driver Email",
        "Sponsor Email",
        "Status",
        "Reason",
        "Created",
        "Updated"
    ]]

    for application in applications:

        created_date = (
            application["CREATED_DTS"].strftime("%Y-%m-%d")
            if application["CREATED_DTS"] else "N/A"
        )

        updated_date = (
            application["UPDATED_DTS"].strftime("%Y-%m-%d")
            if application["UPDATED_DTS"] else "N/A"
        )

        data.append([
            application["SPONSORCOMP_NAME"] or "N/A",
            application["DRIVER_EMAIL"] or "N/A",
            application["SPONSOR_EMAIL"] or "N/A",
            application["STATUS"] or "N/A",
            application["REASON"] or "N/A",
            created_date,
            updated_date
        ])

    table = pdf_style.createTable(
        data,
        column_proportions=[1.0, 1.8, 1.8, 0.8, 1.7, 1.0, 1.0]
    )

    elements.append(table)
    document.build(elements)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="driver_applications_audit.pdf"
    )

@export.route("/point-changes/csv")
def exportPointChangesCsv():
    sponsorcomp_id = request.args.get("sponsorcomp_id", type=int)
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None

    point_changes = getPointChangesForExport(
        sponsorcomp_id,
        start_date,
        end_date
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Driver Email",
        "Changed By",
        "Points Changed",
        "Reason",
        "Balance ID",
        "Sponsor Company",
        "Date and Time"
    ])

    for change in point_changes:
        writer.writerow([
            change["DRIVER_EMAIL"] or "N/A",
            change["CHANGED_BY_EMAIL"] or "N/A",
            change["POINTCHANGE_AMOUNT"],
            change["POINTCHANGE_REASON"] or "N/A",
            change["BALANCE_ID"] or "N/A",
            change["SPONSORCOMP_NAME"] or "N/A",
            change["DTS"] or "N/A"
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=point_changes_audit.csv"
    )

    return response

@export.route("/point-changes/pdf")
def exportPointChangesPdf():
    sponsorcomp_id = request.args.get("sponsorcomp_id", type=int)
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None

    point_changes = getPointChangesForExport(
        sponsorcomp_id,
        start_date,
        end_date
    )

    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(letter)
    )

    pdf_style = RoadRewardsPDF()

    elements = pdf_style.createHeader(
        "Point Changes Audit Log",
        len(point_changes)
    )

    data = [[
        "Driver Email",
        "Changed By",
        "Points Changed",
        "Reason",
        "Balance ID",
        "Sponsor Company",
        "Date and Time"
    ]]

    for change in point_changes:

        change_date = (
            change["DTS"].strftime("%Y-%m-%d %H:%M:%S")
            if change["DTS"] else "N/A"
        )

        data.append([
            change["DRIVER_EMAIL"] or "N/A",
            change["CHANGED_BY_EMAIL"] or "N/A",
            str(change["POINTCHANGE_AMOUNT"]),
            change["POINTCHANGE_REASON"] or "N/A",
            str(change["BALANCE_ID"] or "N/A"),
            change["SPONSORCOMP_NAME"] or "N/A",
            change_date
        ])

    table = pdf_style.createTable(
        data,
        column_proportions=[1.8, 1.8, 0.9, 1.8, 0.9, 1.5, 1.5]
    )

    elements.append(table)
    document.build(elements)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="point_changes_audit.pdf"
    )