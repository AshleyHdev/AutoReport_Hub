AutoReport_Hub

An automated reporting system built using FastAPI & Vue. This project provides functionality to generate PDF reports, send reports via email, and is designed to be extended with a frontend interface for user interaction.

📌 Features

PDF Generation: Generate beautiful, well-structured reports from provided data.

Logo Integration: Embed custom logos in the generated PDF reports.

Email Functionality: Automatically send generated reports to specified email addresses.

Easy Configuration: Supports .env files for sensitive configuration (email credentials, etc.).

Scalable Backend: Built using FastAPI for high-performance asynchronous processing.

📁 Project Structure

🚀 Getting Started

Installation

Clone the repository:

Create a virtual environment & activate it:

Install dependencies:

Configuration

Create a .env file in the root directory:

Running the Server

Server will be running at: http://127.0.0.1:8000

📬 Usage

PDF Generation

Visit: http://127.0.0.1:8000/generate-pdf

Generates a PDF with charts and logo and saves it as report.pdf.

Email Sending

Visit: http://127.0.0.1:8000/send-email

Sends the generated report.pdf as an email attachment.

💡 Future Plans

Integrate with a Vue frontend for better user interaction.

Add file upload interface for CSV/Excel processing.

# AutoReport Hub (自動化報告系統)

### 📌 專案簡介
AutoReport Hub 是一個以 **FastAPI** 和 **Vue** 打造的自動化報告生成系統。後端負責生成 PDF 報告、處理資料、並提供 Email 發送功能；前端則提供檔案上傳、報告生成、與 Email 發送的使用者介面。

---

## 🔍 專案功能
### ✅ 後端功能 (FastAPI)
1. **檔案上傳與資料處理**
    - 接收使用者上傳的 Excel 或 CSV 檔案。
    - 進行資料分析與生成圖表。
2. **PDF 報告生成**
    - 將分析結果轉換成美觀的 PDF 報告檔案。
    - 支援自訂標題、表格格式、公司 Logo 等。
3. **Email 自動發送**
    - 提供 Email 發送功能，自動寄送報告檔案給指定的 Email 地址。

### ✅ 前端功能 (Vue)
1. **檔案上傳介面**
    - 提供使用者選擇檔案並上傳到後端進行處理。
2. **報告生成頁面**
    - 顯示生成的 PDF 報告並提供下載功能。
3. **Email 發送頁面**
    - 提供 Email 地址輸入並自動將報告寄送出去。

---

## 📂 專案結構
```bash
AutoReport_Hub/
│
├── backend/                # 後端 FastAPI 相關檔案
│   ├── main.py              # FastAPI 主檔案 (包含 PDF 生成、Email 發送等功能)
│   └── .env                 # 環境變數檔案 (包含 API 密鑰與 Email 設定)【未上傳】
│
├── frontend/               # 前端 Vue 相關檔案
│   ├── index.html           # 前端入口檔案
│   └── src/                 # Vue 檔案 (組件與 API 請求設定)
│
├── .gitignore              # 設定忽略的檔案與資料夾
├── README.md               # 專案說明文件 (就是這個檔案！)
└── requirements.txt        # Python 套件需求檔案
```

---

## 🚀 如何執行
### 後端 (FastAPI)
1. 建立虛擬環境並啟用：
```bash
python3 -m venv venv
source venv/bin/activate  # MacOS
```
2. 安裝所需套件：
```bash
pip install -r requirements.txt
```
3. 啟動後端服務：
```bash
uvicorn main:app --reload
```
4. 瀏覽 API 文件 (Swagger UI)：
```
http://127.0.0.1:8000/docs
```

### 前端 (Vue)
1. 安裝相依套件：
```bash
npm install
```
2. 啟動前端開發伺服器：
```bash
npm run dev
```
3. 瀏覽應用程式：
```
http://127.0.0.1:5173
```

---

## 📧 環境變數設定 (.env)
後端 FastAPI 的環境變數檔 `.env` 必須包含以下內容：
```
EMAIL_USER=你的email帳號
EMAIL_PASS=你的email密碼
```

---

## 💡 注意事項
- 請確認 `.env` 檔案存在且設定正確。
- 確認所有相依套件已安裝完畢。
- 前端與後端請分開啟動。
- `.gitignore` 已設為忽略 `node_modules/`、`venv/`、`__pycache__/`、`.env` 等檔案。

---

## 📌 作者
這個專案由 **AshleyH.dev (小九)** 製作，並已成功上傳至 GitHub！🎉🚀

歡迎提出問題或改進建議！

Implement email customization and scheduling.

📜 License

This project is licensed under the MIT License.

