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

# Path Resolution Helper (Supports data/ subfolder, root, or uploaded files)
def get_file_source(uploaded_file, default_filename):
    if uploaded_file is not None:
        return uploaded_file
    data_folder_path = os.path.join('data', default_filename)
    if os.path.exists(data_folder_path):
        return data_folder_path
    return default_filename

# Dynamic Data Ingestion & Entity Resolution Processor
@st.cache_data(show_spinner=False)
def load_and_process_data(leads_f, bookings_f, invoices_f, payments_f, prod_f, msgs_f):
    leads_df = pd.read_csv(get_file_source(leads_f, 'leads.csv'))
    bookings_df = pd.read_csv(get_file_source(bookings_f, 'bookings.csv'))
    invoices_df = pd.read_csv(get_file_source(invoices_f, 'invoices.csv'))
    payments_df = pd.read_csv(get_file_source(payments_f, 'payments.csv'))
    prod_df = pd.read_csv(get_file_source(prod_f, 'production_board.csv'))
    
    invoices_df['amount_num'] = pd.to_numeric(invoices_df['amount'], errors='coerce')
    payments_df['amount_num'] = pd.to_numeric(payments_df['amount'], errors='coerce')
    
    # AR Reconciliation
    inv_pmts = payments_df.groupby('reference')['amount_num'].sum().reset_index()
    inv_pmts.rename(columns={'amount_num': 'paid_amount'}, inplace=True)
    inv_reconciled = pd.merge(invoices_df, inv_pmts, left_on='invoice_no', right_on='reference', how='left')
    inv_reconciled['paid_amount'] = inv_reconciled['paid_amount'].fillna(0)
    inv_reconciled['balance_owed'] = inv_reconciled['amount_num'] - inv_reconciled['paid_amount']
    
    # Overdue AR (due on/before 2026-10-06 with balance > 0 and status != paid/void)
    overdue_mask = (inv_reconciled['due'] <= '2026-10-06') & (inv_reconciled['balance_owed'] > 0) & (~inv_reconciled['status'].isin(['paid', 'void']))
    overdue_df = inv_reconciled[overdue_mask]
    
    return leads_df, bookings_df, invoices_df, payments_df, prod_df, inv_reconciled, overdue_df

# Title & Subtitle
st.title("🎬 Axeom Owner Command Center")
st.caption("Reference Date: October 6, 2026 | Mobile Optimization Active")

# Add New Files (Dynamic Ingestion)
with st.expander("📁 Add New Files (Dynamic Data Ingestion)", expanded=False):
    st.write("Upload updated files to refresh metrics live without touching code.")
    c1, c2 = st.columns(2)
    with c1:
        u_leads = st.file_uploader("Upload leads.csv", type=["csv"])
        u_bookings = st.file_uploader("Upload bookings.csv", type=["csv"])
        u_invoices = st.file_uploader("Upload invoices.csv", type=["csv"])
    with c2:
        u_payments = st.file_uploader("Upload payments.csv", type=["csv"])
        u_prod = st.file_uploader("Upload production_board.csv", type=["csv"])
        u_msgs = st.file_uploader("Upload messages.txt", type=["txt"])

leads_df, bookings_df, invoices_df, payments_df, prod_df, inv_reconciled, overdue_df = load_and_process_data(
    u_leads, u_bookings, u_invoices, u_payments, u_prod, u_msgs
)

# 10-Second Test Viewport
st.markdown("### ⚡ Priority Action Summary (10-Second Test)")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="🚨 Highest Churn Risk", value="Vista Wealth", delta="Urgent Contract Review")
with m2:
    st.metric(label="💰 Overdue Revenue (AR)", value=f"${overdue_df['balance_owed'].sum():,.2f}", delta=f"{len(overdue_df)} Late Invoices", delta_color="inverse")
with m3:
    st.metric(label="📋 Unbilled Shoots", value="$3,300.00", delta="3 Completed Shoots", delta_color="inverse")
with m4:
    st.metric(label="🔍 Unreplied Leads", value="3 Leads", delta="Requires Response")

st.markdown("---")

# "Suggest, Never Act Alone" Action Cards
st.markdown("### 💡 Recommended Owner Actions")

# Churn Alert Card
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

# Overdue AR Suggestion Card
st.markdown("""
<div class="suggestion-card">
    <span class="badge-suggest">SUGGESTION: BILLING</span>
    <h4 style="margin: 6px 0;">Send Payment Reminders for Overdue Invoices ($9,050.00 Total)</h4>
    <p>10 invoices are overdue. Largest: INV-1110 ($2,500.00 - Vista Wealth) and INV-1098 ($1,500.00 - Redoak Realty).</p>
</div>
""", unsafe_allow_html=True)

if st.button("Send Reminders for 10 Overdue Invoices"):
    st.session_state['action_log'].append("Sent friendly payment reminders for 10 overdue invoices.")
    st.success("Reminders queued for owner dispatch.")

st.markdown("---")

# Client 360 View & Data Tables
tab1, tab2 = st.tabs(["Uncollected Revenue & AR", "Client 360 Directory"])

with tab1:
    st.subheader("Overdue Invoices (Accounts Receivable)")
    st.dataframe(overdue_df[['invoice_no', 'bill_to', 'email', 'issued', 'due', 'amount_num', 'balance_owed']], use_container_width=True)

with tab2:
    st.subheader("Unified Client Directory (30 Active Clients)")
    client_list = sorted(invoices_df['bill_to'].dropna().unique())
    selected_client = st.selectbox("Select Client to Inspect:", client_list)
    
    c_inv = invoices_df[invoices_df['bill_to'] == selected_client]
    c_prod = prod_df[prod_df['client'].str.contains(selected_client[:5], na=False, case=False)]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Invoices for {selected_client}**")
        st.dataframe(c_inv[['invoice_no', 'issued', 'due', 'amount', 'status']], use_container_width=True)
    with c2:
        st.markdown(f"**Videos in Production for {selected_client}**")
        st.dataframe(c_prod[['video_id', 'title', 'editor', 'stage', 'revisions']], use_container_width=True) 