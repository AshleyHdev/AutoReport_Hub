import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
import ssl
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ✅ 載入環境變數
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # 你的 Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # 你的應用程式密碼

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise RuntimeError("❌ 環境變數未設定，請確認 .env 內包含 EMAIL_ADDRESS 和 EMAIL_PASSWORD")

# ✅ 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
CHART_PATH = os.path.join(BASE_DIR, "chart.png")
PDF_PATH = os.path.join(BASE_DIR, "report.pdf")

# ✅ 設定中文字型
FONT_PATH = "/Library/Fonts/NotoSansCJKtc-VF.ttf"
pdfmetrics.registerFont(TTFont("ChineseFont", FONT_PATH))

app = FastAPI()

# ✅ 啟用 CORS 設定 (這段是新增的)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 如果要限制為前端的網址，可改成 ["http://localhost:5173"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AutoReport Hub - 自動化數據分析報告 API 啟動成功！"}

@app.get("/api/hello")
def read_hello():
    return {"message": "Hello from FastAPI!"}

# ✅ 產生 PDF 報表 API（原本的邏輯，未變更）
@app.post("/generate_report/")
async def generate_report(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_extension = file.filename.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(io.BytesIO(contents))
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="不支援的檔案格式，請上傳 CSV 或 Excel")

        stats = df.describe()
        plt.figure(figsize=(5, 3))
        for col in df.select_dtypes(include=["number"]).columns:
            plt.plot(df.index, df[col], marker="o", label=col)
        plt.legend()
        plt.title("數據變化趨勢")
        plt.xlabel("索引")
        plt.ylabel("數值")
        plt.grid(True)

        if os.path.exists(CHART_PATH):
            os.remove(CHART_PATH)
        plt.savefig(CHART_PATH, bbox_inches='tight')
        plt.close()

        doc = SimpleDocTemplate(PDF_PATH, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.fontName = "ChineseFont"
        title_style.fontSize = 18

        title_table_data = []
        if os.path.exists(LOGO_PATH):
            logo = Image(LOGO_PATH, width=30, height=30)
            title_table_data.append([logo, Paragraph("AutoReport Hub - 自動化數據分析報告", title_style)])
        else:
            title_table_data.append(["", Paragraph("AutoReport Hub - 自動化數據分析報告", title_style)])

        title_table = Table(title_table_data, colWidths=[50, 400])
        title_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(title_table)
        elements.append(Spacer(1, 12))

        if os.path.exists(CHART_PATH):
            chart_img = Image(CHART_PATH, width=300, height=200)
            elements.append(chart_img)
            elements.append(Spacer(1, 12))

        table_data = [["欄位"] + stats.columns.tolist()]
        for stat in stats.index:
            row = [stat] + [round(stats[col][stat], 2) if pd.notna(stats[col][stat]) else "-" for col in stats.columns]
            table_data.append(row)

        table = Table(table_data, colWidths=80)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "ChineseFont"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)

        return FileResponse(PDF_PATH, filename="report.pdf", media_type="application/pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成 PDF 失敗：{str(e)}")

# ✅ 使用 Gmail SMTP 發送 Email（原本的邏輯，未變更）
@app.post("/send_email/")
async def send_email(to_email: str):
    try:
        if "@" not in to_email or "." not in to_email:
            raise HTTPException(status_code=400, detail="請提供有效的 Email 地址")

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = "AutoReport Hub - 自動化數據分析報告"
        body = "您好，請查收您的自動化數據分析報告！📊"
        msg.attach(MIMEText(body, "plain"))

        if not os.path.exists(PDF_PATH):
            raise HTTPException(status_code=400, detail="報告未生成，請先調用 /generate_report/")

        with open(PDF_PATH, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=report.pdf")
            msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        return {"message": "Email 已發送！"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
