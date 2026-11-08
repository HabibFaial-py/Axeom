# daily_log.md

## Day 1 (2026-10-06)
**09:00 to 18:00. What I did:**
- Extracted and audited all 8 dataset files (`leads.csv`, `bookings.csv`, `invoices.csv`, `payments.csv`, `production_board.csv`, `messages.txt`, `team.csv`, `costs.csv`).
- Built python entity-resolution scripts to normalize client names, matching aliases, phone numbers, and emails across all CSVs.
- Performed financial audit: calculated overdue Accounts Receivable ($9,050.00), unbilled completed bookings ($3,300.00), customer credit liabilities ($1,725.00), and caught billing tool errors (INV-1114 and INV-1115 marked unpaid despite received payments P5102 and P5108).
- Identified lost client edit requests in `messages.txt` and pinpointed the root cause to the August 3, 2026 WhatsApp voice note broadcast.

**What I changed my mind about, and why:**
- Initially treated Stonebridge Gym and Stonebridge Athletics as two separate clients. Realized they were a single rebrand entity after cross-referencing Hector Shah's email on August 1, 2026 (`hector@stonebridgegym.co` -> `hector@stonebridgeathletics.com`).

**What went wrong, and how I fixed it:**
- String formatting issues in `invoices.csv` and `bookings.csv` (e.g., `$300` vs `300`) broke numerical aggregation. Cleaned all currency fields with regex before performing reconciliations.

**Where the AI was wrong, and how I caught it:**
- AI originally classified `hello@fosterdental.con` as a brand new lead/client. Caught it by checking phone numbers and domain matching, identifying it as a simple typo for Dr. Grace Foster (`hello@fosterdental.com`).

---

## Day 2 (2026-10-07)
**09:00 to 17:30. What I did:**
- Selected text extraction from `messages.txt` as the core job for Jev AI (`docs.typesafe.ai`).
- Integrated Jev AI to automatically parse raw WhatsApp text, emails, and voice note transcripts into structured JSON payloads (extracting client, video title, revision type, and urgency).
- Hand-audited a sample benchmark of 40 raw message entries against Jev AI outputs, recording a 92.5% accuracy rate (37/40 correct classifications).
- Populated `answers.json` with exact data findings, entity lists, financial totals, churn risk evidence, and Monday action items.

**What I changed my mind about, and why:**
- Originally intended to use Jev AI for financial invoice matching, but realized its NLP capabilities provided significantly higher operational value when extracting unstructured video revision notes from `messages.txt`.

**What went wrong, and how I fixed it:**
- Jev AI initially misclassified casual greetings (e.g., "See you tomorrow") as revision requests. Refined the prompt instructions and system context to ignore scheduling logistics and only tag actionable video edits.

**Where the AI was wrong, and how I caught it:**
- AI suggested terminating Vista Wealth Partners as an unprofitable client. Corrected it by showing that Vista Wealth is a high-margin $2,500/month retainer account whose dissatisfaction stems entirely from fixable legal compliance naming errors ("Vista WP" vs "Vista Wealth Partners").

---

## Day 3 (2026-10-08)
**09:00 to 16:00. What I did:**
- Built the live web application frontend and backend logic. Added a dynamic "Add new files" drag-and-drop file uploader that re-runs entity resolution and financial metrics dynamically upon receiving new CSV files.
- Formatted the dashboard UI specifically for mobile screens to pass the 10-second test: highlighting total uncollected revenue ($9,050 overdue AR + $3,300 unbilled), top churn risk alert (Vista Wealth Partners), and action buttons.
- Implemented human-in-the-loop safeguards ("Suggest, never act alone") for all client notifications and invoice reminders.
- Deployed the application to a public, login-free URL and verified mobile responsiveness and private/incognito browser access.
- Recorded the 5-to-10 minute Loom video demonstration with camera on, answering the 3 reflection questions in an unedited single take.

**What I changed my mind about, and why:**
- Simplified the mobile UI by removing dense data tables from the home view. The owner needs high-level decision cards first; detailed breakdowns belong in secondary drawer tabs.

**What went wrong, and how I fixed it:**
- File upload initial tests failed when processing partial CSV uploads. Fixed backend state management so new file inputs gracefully fall back to baseline schema definitions.

**Where the AI was wrong, and how I caught it:**
- AI generator attempted to put password authentication on the public web link. Explicitly stripped authentication middleware to comply with the challenge requirement for a zero-login live link.