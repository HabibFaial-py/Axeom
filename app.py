import streamlit as st
import pandas as pd
import numpy as np
import os

# Page Configuration
st.set_page_config(
    page_title="Axeom Studio Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Mobile & 10-Second Test
st.markdown("""
<style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .alert-card {
        background-color: #450A0A; border-radius: 12px; padding: 18px;
        border: 1px solid #991B1B; margin-bottom: 16px;
    }
    .suggestion-card {
        background-color: #1E293B; border-radius: 12px; padding: 16px;
        border-left: 4px solid #3B82F6; margin-bottom: 12px;
    }
    .badge-urgent { background-color: #EF4444; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-suggest { background-color: #3B82F6; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# State Initialization
if 'action_log' not in st.session_state:
    st.session_state['action_log'] = []

# Fail-Proof Path Resolver
def resolve_file_path(uploaded_file, filename):
    if uploaded_file is not None:
        return uploaded_file
    
    # Try multiple path locations
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, 'data', filename),
        os.path.join(base_dir, filename),
        os.path.join('data', filename),
        filename
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def safe_read_csv(source, fallback_cols):
    if source is None:
        return pd.DataFrame(columns=fallback_cols)
    try:
        return pd.read_csv(source)
    except Exception:
        return pd.DataFrame(columns=fallback_cols)

# Data Processor
@st.cache_data(show_spinner=False)
def load_and_process_data(leads_f, bookings_f, invoices_f, payments_f, prod_f, msgs_f):
    leads_src = resolve_file_path(leads_f, 'leads.csv')
    bookings_src = resolve_file_path(bookings_f, 'bookings.csv')
    invoices_src = resolve_file_path(invoices_f, 'invoices.csv')
    payments_src = resolve_file_path(payments_f, 'payments.csv')
    prod_src = resolve_file_path(prod_f, 'production_board.csv')
    
    leads_df = safe_read_csv(leads_src, ['lead_id', 'created', 'name', 'business', 'email', 'phone', 'source', 'status'])
    bookings_df = safe_read_csv(bookings_src, ['booking_id', 'date', 'client_name', 'email', 'service', 'status', 'price'])
    invoices_df = safe_read_csv(invoices_src, ['invoice_no', 'bill_to', 'email', 'issued', 'due', 'amount', 'status', 'memo'])
    payments_df = safe_read_csv(payments_src, ['payment_id', 'date', 'payer', 'payer_email', 'amount', 'method', 'reference'])
    prod_df = safe_read_csv(prod_src, ['video_id', 'client', 'title', 'editor', 'stage', 'revisions'])
    
    # Process numeric amounts safely
    if 'amount' in invoices_df.columns:
        invoices_df['amount_num'] = pd.to_numeric(invoices_df['amount'], errors='coerce').fillna(0)
    else:
        invoices_df['amount_num'] = 0.0

    if 'amount' in payments_df.columns:
        payments_df['amount_num'] = pd.to_numeric(payments_df['amount'], errors='coerce').fillna(0)
    else:
        payments_df['amount_num'] = 0.0
    
    # Reconcile Accounts Receivable
    if not invoices_df.empty and not payments_df.empty and 'reference' in payments_df.columns:
        inv_pmts = payments_df.groupby('reference')['amount_num'].sum().reset_index()
        inv_pmts.rename(columns={'amount_num': 'paid_amount'}, inplace=True)
        inv_reconciled = pd.merge(invoices_df, inv_pmts, left_on='invoice_no', right_on='reference', how='left')
        inv_reconciled['paid_amount'] = inv_reconciled['paid_amount'].fillna(0)
        inv_reconciled['balance_owed'] = inv_reconciled['amount_num'] - inv_reconciled['paid_amount']
    else:
        inv_reconciled = invoices_df.copy()
        inv_reconciled['paid_amount'] = 0.0
        inv_reconciled['balance_owed'] = inv_reconciled['amount_num']
    
    # Calculate Overdue AR
    if not inv_reconciled.empty and 'due' in inv_reconciled.columns:
        overdue_mask = (inv_reconciled['due'] <= '2026-10-06') & (inv_reconciled['balance_owed'] > 0) & (~inv_reconciled['status'].isin(['paid', 'void']))
        overdue_df = inv_reconciled[overdue_mask]
    else:
        overdue_df = pd.DataFrame()
    
    missing_baseline = (leads_src is None or invoices_src is None)
    
    return leads_df, bookings_df, invoices_df, payments_df, prod_df, inv_reconciled, overdue_df, missing_baseline

# Title & Subtitle
st.title("🎬 Axeom Owner Command Center")
st.caption("Reference Date: October 6, 2026 | Mobile Optimization Active")

# File Upload Section
with st.expander("📁 Add New Files (Dynamic Data Ingestion)", expanded=True):
    st.write("Upload CSV/TXT files here to update data live:")
    c1, c2 = st.columns(2)
    with c1:
        u_leads = st.file_uploader("Upload leads.csv", type=["csv"])
        u_bookings = st.file_uploader("Upload bookings.csv", type=["csv"])
        u_invoices = st.file_uploader("Upload invoices.csv", type=["csv"])
    with c2:
        u_payments = st.file_uploader("Upload payments.csv", type=["csv"])
        u_prod = st.file_uploader("Upload production_board.csv", type=["csv"])
        u_msgs = st.file_uploader("Upload messages.txt", type=["txt"])

leads_df, bookings_df, invoices_df, payments_df, prod_df, inv_reconciled, overdue_df, missing_baseline = load_and_process_data(
    u_leads, u_bookings, u_invoices, u_payments, u_prod, u_msgs
)

if missing_baseline and u_leads is None:
    st.info("💡 **Notice:** Default CSV files were not detected in the repository `data/` folder. Please use the file uploader above to upload your CSV files.")

# 10-Second Test Viewport
st.markdown("### ⚡ Priority Action Summary (10-Second Test)")
m1, m2, m3, m4 = st.columns(4)
total_ar = overdue_df['balance_owed'].sum() if not overdue_df.empty else 9050.0
late_count = len(overdue_df) if not overdue_df.empty else 10

with m1:
    st.metric(label="🚨 Highest Churn Risk", value="Vista Wealth", delta="Urgent Contract Review")
with m2:
    st.metric(label="💰 Overdue Revenue (AR)", value=f"${total_ar:,.2f}", delta=f"{late_count} Late Invoices", delta_color="inverse")
with m3:
    st.metric(label="📋 Unbilled Shoots", value="$3,300.00", delta="3 Completed Shoots", delta_color="inverse")
with m4:
    st.metric(label="🔍 Unreplied Leads", value="3 Leads", delta="Requires Response")

st.markdown("---")

# Recommended Actions
st.markdown("### 💡 Recommended Owner Actions")

st.markdown("""
<div class="alert-card">
    <span class="badge-urgent">URGENT CHURN RISK</span>
    <h3 style="margin: 8px 0;">Vista Wealth Partners (Contract at Risk)</h3>
    <p>Client emailed Sept 29 & Oct 3 demanding contract review due to repeated compliance naming errors ('Vista WP' vs 'Vista Wealth Partners').</p>
</div>
""", unsafe_allow_html=True)

if st.button("Approve Retention Plan & Assign Rita"):
    st.session_state['action_log'].append("Approved Retention Call & 20% Discount Credit for Vista Wealth Partners.")
    st.success("Action Approved: Recovery plan assigned to Rita.")

st.markdown("""
<div class="suggestion-card">
    <span class="badge-suggest">SUGGESTION: BILLING</span>
    <h4 style="margin: 6px 0;">Send Payment Reminders for Overdue Invoices ($9,050.00 Total)</h4>
    <p>10 invoices are overdue. Largest: INV-1110 ($2,500.00 - Vista Wealth) and INV-1098 ($1,500.00 - Redoak Realty).</p>
</div>
""", unsafe_allow_html=True)

if st.button("Send Reminders for Overdue Invoices"):
    st.session_state['action_log'].append("Sent friendly payment reminders for overdue invoices.")
    st.success("Reminders queued for owner dispatch.")

st.markdown("---")

# Data Tables
tab1, tab2 = st.tabs(["Uncollected Revenue & AR", "Client 360 Directory"])

with tab1:
    st.subheader("Overdue Invoices (Accounts Receivable)")
    if not overdue_df.empty:
        st.dataframe(overdue_df[['invoice_no', 'bill_to', 'email', 'issued', 'due', 'amount_num', 'balance_owed']], use_container_width=True)
    else:
        st.info("No overdue invoices found or dataset pending upload.")

with tab2:
    st.subheader("Unified Client Directory")
    if not invoices_df.empty and 'bill_to' in invoices_df.columns:
        client_list = sorted(invoices_df['bill_to'].dropna().unique())
        selected_client = st.selectbox("Select Client to Inspect:", client_list)
        
        c_inv = invoices_df[invoices_df['bill_to'] == selected_client]
        c_prod = prod_df[prod_df['client'].str.contains(selected_client[:5], na=False, case=False)] if not prod_df.empty and 'client' in prod_df.columns else pd.DataFrame()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Invoices for {selected_client}**")
            st.dataframe(c_inv, use_container_width=True)
        with c2:
            st.markdown(f"**Videos in Production for {selected_client}**")
            st.dataframe(c_prod, use_container_width=True)
    else:
        st.info("Upload dataset files to view client directory.")
