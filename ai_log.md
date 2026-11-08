# ai_log.md - AI Usage & Self-Correction Log

## 1. AI Tools Used
- **ChatGPT / Claude / Gemini / Cursor:** Used for entity resolution algorithm design, financial reconciliation validation, and Streamlit mobile UI generation.

## 2. Key Prompts & Interactions
- **Prompt 1 (Data Reconciliation):** "Cross-reference `invoices.csv` against `payments.csv` as of October 6, 2026, and calculate exact Accounts Receivable balances."
- **Prompt 2 (Entity Matching):** "Build regex rules to unify client name variations across bookings, invoices, and text messages."
- **Prompt 3 (Jev AI Benchmark):** "Parse unstructured edit requests in `messages.txt` and map client notes to video IDs."

## 3. Instance of AI Misclassification & Human Correction
- **Initial Error:** The AI misclassified `hello@fosterdental.con` as a brand new lead and client entity due to the invalid `.con` top-level domain.
- **How I Caught It:** Checked phone numbers across files and matched `214-555-0128` directly to Dr. Grace Foster (`hello@fosterdental.com`).
- **Correction Applied:** Merged the record into Foster Dental (`hello@fosterdental.com`), preventing an artificial inflation of the client count.