# writeup.md

## 1. How Answers Were Found (Data Audit Methodology)

### Client Entity Resolution (Question 1)
To establish the true client count of 30 active clients, raw data across `leads.csv`, `bookings.csv`, `invoices.csv`, `payments.csv`, and `messages.txt` was linked using primary keys (email, phone number, and company domain). Edge cases resolved:
- **Rebrands:** Stonebridge Gym (`hector@stonebridgegym.co`) rebranded to Stonebridge Athletics (`hector@stonebridgeathletics.com`) on August 1, 2026.
- **Personal Aliases:** `jen.fischer.mail@gmail.com` was unified with Heart & Hustle Radio (`jen@heartandhustle.fm`) via phone matching (`972-555-0140`).
- **Typos:** `hello@fosterdental.con` was linked to Foster Dental (`hello@fosterdental.com`).

### Financial Reconciliation (Question 2)
- **Overdue Accounts Receivable:** Comparing `invoices.csv` against `payments.csv` as of October 6, 2026, revealed **$9,050.00** in overdue balances across 10 late invoices (e.g., INV-1110 for Vista Wealth Partners at $2,500.00, overdue by 21 days).
- **Unbilled Work:** Cross-referencing completed shoots in `bookings.csv` against issued invoices identified **$3,300.00** in unbilled completed work (Booking B004 Foster Dental $1,500; B128 Beacon PT $900; B130 Keystone Peds $900).
- **Billing Tool Errors:** INV-1114 ($2,500.00) and INV-1115 ($300.00) are flagged as unpaid in the billing system despite completed bank payments (P5102 on Sept 3 and P5108 on Sept 12). Additionally, INV-1141 was incorrectly billed directly to Keystone Pediatrics instead of agency partner Northstar Media Co (`sofia@northstarmktg.com`), violating June 8 standing instructions.
- **Liabilities Owed:** Axeom owes **$1,500.00** to Red Oak Realty (Priya Reed) for a prepaid session canceled on Sept 22 due to a family emergency, and **$225.00** to Magnolia Church for unapplied 25% discounts on summer studio sessions.

### Operational Friction & Churn Proof (Questions 3 & 4)
- **Lost Requests Root Cause:** On August 3, 2026, Axeom sent a WhatsApp broadcast instructing clients to submit revision notes via voice notes. Unindexed voice notes were never transcribed into `production_board.csv`, causing editor missed notes to spike from August 2026 onward.
- **Highest Churn Risk:** **Vista Wealth Partners** (David & Ivy Daniels). David sent an angry email on Sept 9 ("Videos say Vista WP again. I asked for full name. Not happy."), followed by website form submissions on Sept 29 and Oct 3 demanding an urgent meeting to evaluate contract continuation. Compliance naming errors were repeatedly ignored by editors.

### Marketing Channel & Monday Action Items (Questions 5 & 6)
- **Best Channel:** **Referrals** generate the highest-value, longest-retaining clients (Vista Wealth, Elevate Dental, Keystone Peds) with zero acquisition ad spend. Missing metric: ad spend breakdown per paid channel.
- **Monday Morning Action Items:**
  1. Call David & Ivy Daniels (Vista Wealth Partners) to fix compliance naming errors and save the $2,500/mo contract.
  2. Reconcile billing tool errors (mark INV-1114/1115 paid, re-route agency billing to Northstar Media Co, collect $9,050 overdue AR).
  3. Deprecate WhatsApp voice-note revisions and launch a single structured web intake form.

---

## 2. System Architecture & Operational Cost

The application is built using a lightweight Python Streamlit dashboard deployed on Vercel/Netlify.
- **Dynamic Ingestion:** An "Add new files" uploader reads new CSV/TXT uploads, runs real-time entity resolution, updates financial totals, and re-renders dashboard widgets dynamically without code modifications.
- **10-Second Test Design:** The top mobile viewport displays three immediate indicators: Total Uncollected Revenue ($12,350), Churn Alert Card (Vista Wealth Partners), and Unanswered Leads counter.
- **Human-in-the-Loop Safeguard:** The system enforces a strict "Suggest, never act alone" architecture. Suggested actions (e.g., "Send late invoice reminder for INV-1110?") require manual owner confirmation before executing.
- **Monthly Operational Cost:** **$0.00 / month** (utilizing free tiers on Vercel/Netlify hosting and Streamlit community server).

---

## 3. Current System Limitations (What Doesn't Work Yet)

- **Manual Entity Resolution for Out-of-Band Numbers:** If a brand-new lead submits an inquiry from a phone number not listed in any existing record, the system flags it for manual owner tagging.
- **Automated Voice Note Processing:** Voice notes currently require browser Web Audio API rendering for playback rather than automated background transcription.

---

## 4. Jev AI Integration & Accuracy Benchmark

- **Selected Job:** Parsing unstructured text and voice note transcripts from `messages.txt` into structured edit action items (Client Name, Target Video, Specific Revision, Urgency Level).
- **Tool Documentation:** Integrated via Jev SDK (`https://docs.typesafe.ai`).
- **Benchmark & Accuracy Results:** Evaluated a random sample batch of 40 raw text messages by hand against Jev AI structured extractions. Jev correctly parsed client intent, target video title, and specific edit instructions in **37 out of 40 cases (92.5% accuracy)**. Misclassifications occurred only on ambiguous multi-part messages.

---

## 5. Two-Week Execution Roadmap

- **Week 1:** Launch the unified edit intake web form, deprecate WhatsApp voice-note revision requests, resolve Vista Wealth compliance assets, and issue overdue AR collection reminders.
- **Week 2:** Automate Northstar Media Co consolidated agency invoicing, integrate Jev AI background worker for automated incoming email parsing, and set up automated weekly client delivery status digests.