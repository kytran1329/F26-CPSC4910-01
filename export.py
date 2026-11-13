import mysql.connector
import os
from dotenv import load_dotenv
import csv
import io

from datetime import date
from decimal import Decimal

from flask import Blueprint, Response, send_file, request, session, abort

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

from xml.sax.saxutils import escape

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

export = Blueprint(
    "export",
    __name__,
    url_prefix="/admin/export"
)

def getLoggedInSponsorCompanyId():
    user_id = session.get("user_id")

    if not user_id:
        abort(401)

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT SPONSORCOMP_ID
            FROM SPONSOR
            WHERE USER_ID = %s
        """, (user_id,))

        sponsor = cursor.fetchone()

        if not sponsor:
            abort(403)

        return sponsor["SPONSORCOMP_ID"]

    finally:
        cursor.close()
        conn.close()

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

def getPointChanges(sponsorcomp_id=None,start_date=None,end_date=None,driver_id=None):
    conn = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASSWORD,
                        database=DB_NAME
                    )
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            "GET_POINT_CHANGES_AUDIT",
            (sponsorcomp_id, start_date, end_date, driver_id)
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

    point_changes = getPointChanges(
        sponsorcomp_id,
        start_date,
        end_date,
        None
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

    point_changes = getPointChanges(
        sponsorcomp_id,
        start_date,
        end_date,
        None
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

@export.route("/sponsor-applications/csv")
def exportSponsorApplicationsCsv():
    sponsorcomp_id = getLoggedInSponsorCompanyId()
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None

    applications = getDriverApplications(
        sponsorcomp_id, start_date, end_date
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Driver Email", "Status", "Reason",
        "Reviewed By", "Created Date", "Updated Date"
    ])

    for application in applications:
        writer.writerow([
            application.get("DRIVER_EMAIL") or "N/A",
            application.get("STATUS") or "N/A",
            application.get("REASON") or "N/A",
            application.get("REVIEWED_BY_EMAIL") or "N/A",
            application.get("CREATED_DTS") or "N/A",
            application.get("UPDATED_DTS") or "N/A"
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=sponsor_applications_audit.csv"
        }
    )

@export.route("/sponsor-applications/pdf")
def exportSponsorApplicationsPdf():
    sponsorcomp_id = getLoggedInSponsorCompanyId()
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None

    applications = getDriverApplications(
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
        "Sponsor Driver Applications Audit Log",
        len(applications)
    )

    data = [[
        "Driver Email", "Status", "Reason",
        "Reviewed By", "Created", "Updated"
    ]]

    for application in applications:
        data.append([
            application.get("DRIVER_EMAIL") or "N/A",
            application.get("STATUS") or "N/A",
            application.get("REASON") or "N/A",
            application.get("REVIEWED_BY_EMAIL") or "N/A",
            str(application.get("CREATED_DTS") or "N/A"),
            str(application.get("UPDATED_DTS") or "N/A")
        ])

    elements.append(pdf_style.createTable(
        data,
        column_proportions=[1.5, 0.8, 1.5, 1.5, 1.3, 1.3]
    ))

    document.build(elements)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="sponsor_applications_audit.pdf"
    )

@export.route("/sponsor-point-changes/csv")
def exportSponsorPointChangesCsv():
    sponsorcomp_id = getLoggedInSponsorCompanyId()
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    driver_id = request.args.get("driver_id", type=int)

    changes = getPointChanges(
        sponsorcomp_id,
        start_date,
        end_date,
        driver_id
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Driver Email", "Changed By", "Points Changed",
        "Reason", "Date and Time"
    ])

    for change in changes:
        writer.writerow([
            change.get("DRIVER_EMAIL") or "N/A",
            change.get("CHANGED_BY_EMAIL") or "N/A",
            change.get("POINTCHANGE_AMOUNT"),
            change.get("POINTCHANGE_REASON") or "N/A",
            change.get("DTS") or "N/A"
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=sponsor_point_changes_audit.csv"
        }
    )

@export.route("/sponsor-point-changes/pdf")
def exportSponsorPointChangesPdf():
    sponsorcomp_id = getLoggedInSponsorCompanyId()
    start_date = request.args.get("start_date") or None
    end_date = request.args.get("end_date") or None
    driver_id = request.args.get("driver_id", type=int)

    changes = getPointChanges(
        sponsorcomp_id, start_date, end_date, driver_id
    )

    pdf_buffer = io.BytesIO()
    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(letter)
    )

    pdf_style = RoadRewardsPDF()
    elements = pdf_style.createHeader(
        "Sponsor Point Changes Audit Log",
        len(changes)
    )

    data = [[
        "Driver Email", "Changed By", "Points Changed",
        "Reason", "Date and Time"
    ]]

    for change in changes:
        data.append([
            change.get("DRIVER_EMAIL") or "N/A",
            change.get("CHANGED_BY_EMAIL") or "N/A",
            str(change.get("POINTCHANGE_AMOUNT", "N/A")),
            change.get("POINTCHANGE_REASON") or "N/A",
            str(change.get("DTS") or "N/A")
        ])

    elements.append(pdf_style.createTable(
        data,
        column_proportions=[1.7, 1.7, 1.0, 2.0, 2.0]
    ))

    document.build(elements)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="sponsor_point_changes_audit.pdf"
    )

# Helper function to validate all filter values
def parseOrderReportFilters(values):
    reportType = (
        values.get("report_type") or "summary"
    ).strip().lower()

    role = (
        values.get("role") or "Driver"
    ).strip().title()

    if reportType not in ("summary", "detailed"):
        raise ValueError("Invalid report type")

    if role not in ("Driver", "Sponsor"):
        raise ValueError("Invalid role")

    def optionalId(name):
        text = (values.get(name) or "").strip()

        if not text:
            return None

        result = int(text)

        if result <= 0:
            raise ValueError("Invalid ID")

        return result

    def optionalDate(name):
        text = (values.get(name) or "").strip()

        return date.fromisoformat(text) if text else None

    # Filters Dictionary
    filters = {
        "report_type": reportType,
        "sponsorcomp_id": optionalId("sponsorcomp_id"),
        "user_id": optionalId("user_id"),
        "start_date": optionalDate("start_date"),
        "end_date": optionalDate("end_date"),
        "role": role
    }

    if (
        filters["start_date"] is not None
        and filters["end_date"] is not None
        and filters["start_date"] > filters["end_date"]
    ):
        raise ValueError(
            "End date must be on or after start date"
        )

    return filters

# Retrieve Report Rows using Filters
def getOrderReportRows(
    report_type,
    role,
    sponsorcomp_id=None,
    user_id=None,
    start_date=None,
    end_date=None,
):

    # Uses MySQL stored procedure names for different forms
    procedures = {
        "summary": "GET_ORDER_SUMMARY",
        "detailed": "GET_ORDER_DETAILED"
    }

    if report_type not in procedures:
        raise ValueError("Invalid report type")

    if role not in ("Driver", "Sponsor"):
        raise ValueError("Invalid role")

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc(
            procedures[report_type],
            (
                sponsorcomp_id,
                user_id,
                start_date,
                end_date,
                role
            )
        )

        rows = []

        for result in cursor.stored_results():
            rows.extend(result.fetchall())

        return rows

    finally:
        cursor.close()
        conn.close()

@export.route("/orders/<report_type>/csv")
def exportOrderReportCsv(report_type):
    try:
        # Retrieve arguments/filters
        args = request.args.to_dict()
        args["report_type"] = report_type

        # Validate filters
        filters = parseOrderReportFilters(args)

    except (ValueError, TypeError):
        abort(400, "Invalid report filters")

    # Retrieve orders from the stored procedure using filter dictionary 
    orders = getOrderReportRows(**filters)

    output = io.StringIO()
    writer = csv.writer(output) # Create CSV writer to StringIO buffer

    if report_type == "summary":
        
        writer.writerow([
            "Ordered By",
            "Sponsor Company",
            "Number of Purchases",
            "Points Used",
            "Total Sales"
        ])

        for order in orders:
            writer.writerow([
                order["ORDERED_BY_NAME"],
                order["SPONSORCOMP_NAME"],
                order["PURCHASE_COUNT"],
                order["TOTAL_POINTS_USED"],
                order["TOTAL_SALES"]
            ])

    else:

        writer.writerow([
            "Order ID",
            "Ordered By",
            "Receiving Driver",
            "Sponsor Company",
            "Date",
            "Item",
            "Points Used",
            "Total Sales"
        ])

        for order in orders:
            writer.writerow([
                order["ORDER_ID"],
                order["ORDERED_BY_NAME"],
                order["DRIVER_NAME"] or "N/A",
                order["SPONSORCOMP_NAME"],
                order["ORDER_DTS"],
                order["ITEM_NAME"],
                order["POINTS_USED"]
                    if order["POINTS_USED"] is not None
                    else "",
                order["LINE_TOTAL"]
            ])

    # Create HTTP response
    response = Response(
        output.getvalue(), # Retrieves generated CSV text
        mimetype="text/csv" # Tell browser the content is CSV
    )
    # Create HTTP response header
    response.headers["Content-Disposition"] = (
        f"attachment; filename="
        f"sales_by_{filters['role'].lower()}_{report_type}.csv"
    )

    return response

@export.route("/orders/<report_type>/pdf")
def exportOrderReportPdf(report_type):
    try:
        # Retrieve arguments/filters
        args = request.args.to_dict()
        args["report_type"] = report_type
        # Validate filters
        filters = parseOrderReportFilters(args)

    except (ValueError, TypeError):
        abort(400, "Invalid report filters")

    # Retrieve orders from the stored procedure using filter dictionary
    orders = getOrderReportRows(**filters)

    pdf_buffer = io.BytesIO() # Create PDF buffer

    document = SimpleDocTemplate(
        pdf_buffer, # buffer where completed PDF to be stored
        pagesize=landscape(letter)
    )

    # Custom PDF styling from RoadRewards Class
    pdf_style = RoadRewardsPDF()

    elements = pdf_style.createHeader(
        f"Sales by {filters['role']}s - {report_type.title()}",
        len(orders)
    )

    if report_type == "summary":

        data = [[
            "Ordered By",
            "Sponsor Company",
            "Purchases",
            "Points Used",
            "Total Sales"
        ]]

        for order in orders:
            data.append([
                order["ORDERED_BY_NAME"],
                order["SPONSORCOMP_NAME"],
                str(order["PURCHASE_COUNT"]),
                str(order["TOTAL_POINTS_USED"]),
                str(order["TOTAL_SALES"])
            ])
        # Custom column sizes to fit data
        column_proportions = [2, 2, 1, 1, 1]

    else:

        data = [[
            "Order ID",
            "Ordered By",
            "Receiving Driver",
            "Sponsor",
            "Date",
            "Item",
            "Points Used",
            "Sales"
        ]]

        for order in orders:
            data.append([
                str(order["ORDER_ID"]),
                order["ORDERED_BY_NAME"],
                order["DRIVER_NAME"] or "N/A",
                order["SPONSORCOMP_NAME"],
                str(order["ORDER_DTS"]),
                order["ITEM_NAME"],
                str(order["POINTS_USED"])
                    if order["POINTS_USED"] is not None
                    else "",
                str(order["LINE_TOTAL"])
            ])
        # Custom column sizes to fit data
        column_proportions = [
            0.7, 1.2, 1.2, 1.2,
            1.1, 1.5, 0.8, 0.8
        ]

    # Wrap text for detailed reports
    # NO WRAP = OVERFLOW
    if report_type == "detailed":

        # Header styling
        header_style = ParagraphStyle(
            "ReportHeader",
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            textColor=colors.white,
            splitLongWords=1
        )

        # Data styling
        cell_style = ParagraphStyle(
            "ReportCell",
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=colors.black,
            splitLongWords=1
        )

        # Wrap header text
        data[0] = [
            Paragraph(escape(str(value)), header_style)
            for value in data[0]
        ]

        # Wrap table data
        data[1:] = [
            [
                Paragraph(escape(str(value)), cell_style)
                for value in row
            ]
            for row in data[1:]
        ]

    table = pdf_style.createTable(
        data,
        column_proportions=column_proportions
    )
    # Adds table to the list of elements that will appear
    elements.append(table)

    document.build(elements)
    pdf_buffer.seek(0) # reset buffer pointer/cursor to beginning

    # Use Flask's built in function for sending files
    # Unlike CSV, the PDF buffer is binary
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=(
            f"sales_by_{filters['role'].lower()}_{report_type}.pdf"
        )
    )