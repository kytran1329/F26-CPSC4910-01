from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

class RoadRewardsPDF:
    def __init__(self):
        styles = getSampleStyleSheet()

        self.brand_style = ParagraphStyle(
            "BrandStyle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=8
        )

        self.title_style = ParagraphStyle(
            "AuditTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=12
        )

        self.count_style = ParagraphStyle(
            "CountStyle",
            parent=styles["Normal"],
            fontSize=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563")
        )

    def createHeader(self, title, record_count):
        return [
            Paragraph("Road Rewards", self.brand_style),
            Paragraph(title, self.title_style),
            Paragraph(
                f"Total Records: {record_count}",
                self.count_style
            ),
            Spacer(1, 20)
        ]

    
    def createTable(self, data, column_proportions=None):
        num_columns = len(data[0])
        table_width = 9 * inch

        # Default to equal column widths
        if column_proportions is None:
            column_proportions = [1] * num_columns

        # Normalize proportions
        total = sum(column_proportions)
        column_widths = [
            table_width * (proportion / total)
            for proportion in column_proportions
        ]

        # Create table with calculated column widths
        table = Table(
            data,
            colWidths=column_widths,
            repeatRows=1
        )

        # Apply shared styling
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))

        return table
