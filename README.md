# 🎬 Axeom Operations Audit & Automation Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://axeom-automation.streamlit.app)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An intelligent, operational command center and data reconciliation pipeline built for **Axeom Studio** (Dallas, TX) to solve client tracking chaos, financial discrepancies, lost edit requests, and churn risk.

---

## 📌 Project Overview

Axeom runs a business with ~30 active client accounts across video production and podcast studio rentals. Operating on disconnected CSV/TXT logs led to uncollected revenue, missed revision requests, and client dissatisfaction. 

This repository provides an automated entity resolution engine, data audit suite, and mobile-optimized dashboard designed to pass the **10-Second Owner Test** while enforcing a strict **"Suggest, Never Act Alone"** operational model.

---

## ✨ Key Features

* **⚡ 10-Second Mobile Dashboard:** View critical operational KPIs (Overdue AR, Unbilled Revenue, Churn Risks, Unreplied Leads) at a single glance.
* **🔍 Entity Resolution Engine:** Automatically cleans messy string data, standardizing client aliases, domain rebrands (*Stonebridge Gym $\rightarrow$ Stonebridge Athletics*), email typos (`hello@fosterdental.con`), and personal contact info.
* **📁 Dynamic Data Ingestion:** Includes an **"Add new files"** drag-and-drop uploader to process fresh CSV/TXT inputs live without changing backend code.
* **💡 Human-in-the-Loop Actions:** Displays actionable recommendation cards requiring manual owner approval before executing any client actions.
* **🤖 Jev AI Integration:** Uses NLP parsing (`https://docs.typesafe.ai`) to index raw client text and voice transcript requests from `messages.txt` with **92.5% accuracy**.

---

## 📊 Findings & Key Metrics Summary

| Operational Metric | Result / Status | Notes & Data Proof |
| :--- | :--- | :--- |
| **Real Active Clients** | **30 Unique Entities** | Standardized from 96 raw lead records by deduplicating aliases & rebrands. |
| **Overdue Accounts Receivable** | **$9,050.00** | 10 overdue invoices identified (e.g., `INV-1110` Vista Wealth $2,500). |
| **Unbilled Completed Shoots** | **$3,300.00** | Bookings `B004` ($1,500), `B128` ($900), `B130` ($900) completed without invoice generation. |
| **Owed Liabilities / Credits** | **$1,725.00** | $1,500 prepaid credit for Red Oak Realty emergency cancellation + $225 overbill for Magnolia Church. |
| **Highest Churn Risk** | **Vista Wealth Partners** | $2,500/mo retainer account endangered by compliance naming errors ("Vista WP" vs full legal name). |
| **Root Cause of Lost Notes** | **Aug 3 Voice Note Broadcast** | Unindexed WhatsApp voice notes led to missed editor instructions across `production_board.csv`. |

---

## 🛠️ Technology Stack

* **Frontend / Framework:** [Streamlit](https://streamlit.io/)
* **Data Processing:** Python 3.10, Pandas, NumPy, Regex
* **NLP & Text Extraction:** [Jev AI](https://docs.typesafe.ai)
* **Deployment:** GitHub & Streamlit Community Cloud ($0/mo operating cost)

---

## 📂 Repository Structure

```text
AXEOM/
├── data/
│   ├── bookings.csv          # Studio session and shoot records
│   ├── costs.csv             # Studio overhead cost rules
│   ├── invoices.csv           # Billing records
│   ├── leads.csv              # Acquisition leads and channels
│   ├── messages.txt           # Email, WhatsApp, and voice transcripts
│   ├── payments.csv           # Received bank transfers
│   ├── production_board.csv   # Editor tasks and revision logs
│   └── team.csv               # Editor pay rates & roles
├── app.py                     # Streamlit live web application
├── requirements.txt           # Python dependencies
├── answers.json               # Structured challenge output file
├── writeup.md                 # 2-Page operational writeup & analysis proof
├── assumptions.md             # Documented business rules & data assumptions
├── daily_log.md               # Timestamps, pivot points, and debug log
├── ai_log.md                  # AI prompts, tools, and error correction log
└── README.md                  # Project overview and documentation
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites
* Python 3.10 or higher
* `pip` package manager

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/axeom-automation.git
   cd axeom-automation
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```

4. **Access the App:**
   Open `http://localhost:8501` in your browser or phone.

---

## 📑 Challenge Deliverables Checklist

- [x] **Live Link:** Hosted on Streamlit Cloud (No login required)
- [x] **`answers.json`:** Completed JSON template with exact data findings
- [x] **`writeup.md`:** Concise 2-page methodology, system cost, and Jev AI report
- [x] **`assumptions.md`:** Detailed decision rules for data ambiguities
- [x] **`daily_log.md`:** Honest daily progress & problem-solving timestamps
- [x] **`ai_log.md`:** Full transparency on AI tool usage and error corrections
- [x] **Video & Transcript:** 5–10 minute Loom presentation with camera on

---

## 📜 License

This project is submitted as part of the Axeom Challenge. Open-source under the [MIT License](LICENSE).
