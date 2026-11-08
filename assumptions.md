# assumptions.md

## 1. Client Identity & Entity Resolution
- **Email & Phone Primary Key Alignment:** Clients with multiple record variations (e.g., `hector@stonebridgegym.co` and `hector@stonebridgeathletics.com`) were merged into a single client entity ("Stonebridge Athletics") based on the explicit rebrand email dated August 1, 2026.
- **Typographical Errors:** `hello@fosterdental.con` was assumed to be a typographical error for `hello@fosterdental.com` and mapped to Dr. Grace Foster (Foster Dental).
- **Personal vs. Business Email:** `jen.fischer.mail@gmail.com` submitting website forms was linked to Heart & Hustle Radio (`jen@heartandhustle.fm`) based on matching phone number `972-555-0140`.

## 2. Invoicing, Payments & Financial Accounting
- **Reference Date Cutoff:** The dataset reference date is strictly October 6, 2026. Any invoice with a due date on or before October 6, 2026, without a matching payment record in `payments.csv` is categorized as overdue Accounts Receivable (AR).
- **Unbilled Work:** Completed sessions in `bookings.csv` prior to October 6, 2026, lacking a corresponding record in `invoices.csv` were classified as unbilled work (e.g., booking B004 for Foster Dental at $1,500, B128 for Beacon PT at $900, and B130 for Keystone Peds at $900).
- **Third-Party Agency Billing:** Sofia Price (`sofia@northstarmktg.com`) sent explicit email instructions on June 8, 2026, directing Axeom to bill Northstar Media Co directly for Keystone Pediatrics and Beacon Physical Therapy sessions. Invoices issued directly to individual end-clients after this date were marked as billing tool routing errors.
- **Discounts:** The 25% studio session discount granted to Magnolia Church via email on May 24, 2026, applies to all studio sessions booked from June 2026 onwards ($225 instead of $300).

## 3. Customer Liabilities & Refunds
- **Prepaid Canceled Sessions:** Priya Reed (Red Oak Realty) paid in advance for a shoot on September 22, 2026, which was canceled due to a family emergency (`messages.txt`). Because the money was received but no work was performed, Axeom holds a $1,500 credit liability owed to the client.

## 4. Communication & Edit Request Workflows
- **Voice Note Revision Breakdown:** Axeom’s WhatsApp broadcast on August 3, 2026 ("send edit notes as a voice note") created an unindexed communication channel. Edit requests sent via voice note were assumed to be lost in production if they did not correspond to updated notes in `production_board.csv`.

## 5. Marketing Channel Analysis
- **ROI Calculation Limitations:** Because the dataset does not include ad spend, cost-per-click (CPC), or sales conversion labor overhead, net channel performance is calculated strictly as gross revenue generated per acquisition source minus direct production costs.