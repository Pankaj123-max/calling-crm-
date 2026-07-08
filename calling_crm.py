import streamlit as st
import pandas as pd
import sqlite3
import os
import subprocess
from datetime import datetime, timedelta
import io
import base64
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Call Flow CRM - Pankaj Jadhav",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INIT ====================
if 'call_mode' not in st.session_state:
    st.session_state.call_mode = "Laptop"
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'customers' not in st.session_state:
    st.session_state.customers = []
if 'refresh_counter' not in st.session_state:
    st.session_state.refresh_counter = 0

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* ===== STANDARD FONT SIZE ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Main text sizes */
    .stMarkdown, .stText, .stCaption, p, div, span, label {
        font-size: 14px !important;
        color: #1a1a2e !important;
    }
    
    /* Headers */
    h1 {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    h2 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    h3 {
        font-size: 17px !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
    }
    h4, .stSubheader {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
    }
    
    /* ===== LAYOUT ===== */
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* ===== HEADER ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-header .brand .logo-icon {
        font-size: 28px;
        background: rgba(255,255,255,0.15);
        padding: 6px 12px;
        border-radius: 10px;
    }
    .main-header .brand .title-group {
        display: flex;
        flex-direction: column;
    }
    .main-header .brand h1 {
        font-size: 22px !important;
        margin: 0;
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .main-header .brand .subtitle {
        color: rgba(255,255,255,0.85) !important;
        font-size: 13px !important;
        margin: 0;
        font-weight: 400;
    }
    .main-header .creator {
        color: #FFFFFF !important;
        font-size: 13px !important;
        text-align: right;
        font-weight: 500;
        background: rgba(255,255,255,0.15);
        padding: 4px 16px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header .creator span {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* ===== CUSTOMER CARD ===== */
    .customer-card {
        background: white;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .customer-card .name {
        font-size: 18px !important;
        font-weight: 700;
        color: #1a1a2e;
    }
    .customer-card .phone {
        font-size: 16px !important;
        color: #667eea;
        font-weight: 600;
    }
    .customer-card .info {
        font-size: 13px !important;
        color: #666;
        margin-top: 2px;
    }
    
    /* ===== STATUS BADGE ===== */
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-size: 13px !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102,126,234,0.3);
    }
    
    /* ===== BUTTONS ===== */
    .stButton button {
        width: 100% !important;
        min-height: 36px !important;
        height: 36px !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 0 0.8rem !important;
        box-shadow: 0 2px 10px rgba(102,126,234,0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
    }
    
    /* ===== INPUTS ===== */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        font-size: 14px !important;
        border-radius: 10px !important;
        border: 2px solid #e8e8e8 !important;
        min-height: 38px !important;
        padding: 0.5rem 0.8rem !important;
        background: white !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102,126,234,0.1) !important;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div {
        height: 6px !important;
        background: #e8e8e8 !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
        height: 6px !important;
    }
    
    /* ===== METRIC BOX ===== */
    .metric-box {
        background: white;
        padding: 0.5rem 0.8rem;
        border-radius: 10px;
        border: 1px solid #e8e8e8;
        text-align: center;
        margin-bottom: 0.3rem;
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .metric-box .value {
        font-size: 20px !important;
        font-weight: 700;
        color: #667eea;
    }
    .metric-box .label {
        font-size: 11px !important;
        color: #888;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg {
        background: rgba(255,255,255,0.95) !important;
        backdrop-filter: blur(10px) !important;
        padding-top: 0.5rem !important;
        border-right: 1px solid #e8e8e8 !important;
    }
    .sidebar-header {
        text-align: center;
        padding: 0.8rem 0;
        border-bottom: 2px solid #e8e8e8;
        margin-bottom: 0.8rem;
    }
    .sidebar-header .logo {
        font-size: 32px !important;
        display: block;
        margin-bottom: 4px;
    }
    .sidebar-header h3 {
        font-size: 18px !important;
        margin: 0;
        color: #1a1a2e !important;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-header .creator-name {
        font-size: 12px !important;
        color: #888 !important;
        margin: 2px 0 0 0;
        font-weight: 500;
    }
    .sidebar-header .creator-name span {
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* ===== ADB STATUS ===== */
    .adb-status {
        padding: 0.4rem 0.8rem;
        border-radius: 10px;
        text-align: center;
        font-size: 13px !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .adb-connected {
        background: #d4edda;
        color: #155724 !important;
        border: 1px solid #28a745;
    }
    .adb-disconnected {
        background: #f8d7da;
        color: #721c24 !important;
        border: 1px solid #dc3545;
    }
    
    /* ===== MODE SELECTOR ===== */
    .mode-selector {
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        border: 1px solid #e8e8e8;
        margin-bottom: 0.5rem;
    }
    .mode-selector .title {
        font-size: 12px !important;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: 0.5px;
    }
    .mode-status-text {
        text-align: center;
        font-size: 12px !important;
        font-weight: 600;
        margin-top: 0.3rem;
        padding: 4px 8px;
        border-radius: 6px;
    }
    
    /* ===== MOBILE CALL ===== */
    .mobile-call-container {
        background: linear-gradient(135deg, #f8f9ff, #e8f0fe);
        padding: 0.8rem;
        border-radius: 12px;
        border: 2px solid rgba(102,126,234,0.15);
        margin: 0.3rem 0;
    }
    .mobile-call-btn {
        display: block;
        padding: 8px 12px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px !important;
        text-align: center;
        margin: 4px 0;
        transition: all 0.3s ease;
    }
    .mobile-call-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .call-now-btn {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white !important;
    }
    .sms-btn {
        background: linear-gradient(135deg, #17a2b8, #0dcaf0);
        color: white !important;
    }
    .whatsapp-btn {
        background: linear-gradient(135deg, #25d366, #128C7E);
        color: white !important;
    }
    
    /* ===== NAVIGATION RADIO ===== */
    .stRadio > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
    }
    .stRadio label {
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stRadio label:hover {
        background: #f0f0ff !important;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 0.5rem;
        color: #888;
        font-size: 12px !important;
        border-top: 1px solid #e8e8e8;
        margin-top: 0.5rem;
    }
    .footer .heart {
        color: #ec4899;
    }
    .footer .name {
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* ===== HIDE DEFAULT ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 0.5rem;
        }
        .main-header .creator {
            text-align: center;
            margin-top: 4px;
        }
        .customer-card .name {
            font-size: 16px !important;
        }
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f0f0f0;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE FUNCTIONS ====================
def init_db():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE customers ADD COLUMN followup_date TEXT")
    except:
        pass
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        status TEXT,
        notes TEXT,
        call_date TEXT,
        call_time TEXT,
        followup_date TEXT
    )''')
    conn.commit()
    conn.close()

def update_customer_status(customer_id, status, notes, followup_date=None):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    now = datetime.now()
    
    if followup_date:
        c.execute("""
            UPDATE customers 
            SET status=?, notes=?, call_date=?, call_time=?, followup_date=?
            WHERE id=?
        """, (status, notes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), followup_date, customer_id))
    else:
        c.execute("""
            UPDATE customers 
            SET status=?, notes=?, call_date=?, call_time=?
            WHERE id=?
        """, (status, notes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), customer_id))
    
    conn.commit()
    conn.close()
    return True

def update_customer_phone(customer_id, new_phone):
    try:
        conn = sqlite3.connect('crm_data.db')
        c = conn.cursor()
        c.execute("UPDATE customers SET phone=? WHERE id=?", (new_phone.strip(), customer_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_all_customers():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id")
    data = c.fetchall()
    conn.close()
    return data

def clear_database():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM customers")
    conn.commit()
    conn.close()

def import_from_excel(df, name_col, phone_col):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    imported = 0
    for _, row in df.iterrows():
        name = str(row[name_col]).strip()
        phone = str(row[phone_col]).strip()
        phone = ''.join(filter(str.isdigit, phone))
        if name and phone:
            c.execute("SELECT * FROM customers WHERE name=? AND phone=?", (name, phone))
            if not c.fetchone():
                c.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
                imported += 1
    conn.commit()
    conn.close()
    return imported

# ==================== ADB FUNCTIONS ====================
def check_adb():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        if 'device' in result.stdout and 'List of devices' in result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                if '\tdevice' in line:
                    return True, line.split('\t')[0]
        return False, None
    except:
        return False, None

def call_via_adb(phone):
    try:
        phone = ''.join(filter(str.isdigit, phone))
        if not phone:
            return False, "Invalid phone number!"
        check_result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        if 'device' not in check_result.stdout:
            return False, "Phone not connected!"
        cmd = ['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone}']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, f"Call initiated to {phone}!"
        else:
            return False, f"ADB Error: {result.stderr}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def end_call_via_adb():
    try:
        cmd = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_ENDCALL']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Call ended!"
        else:
            return False, "Error ending call!"
    except:
        return False, "Error!"

# ==================== MOBILE CALL HTML ====================
def get_mobile_call_html(phone):
    phone = ''.join(filter(str.isdigit, phone))
    return f'''
    <div class="mobile-call-container">
        <a href="tel:{phone}" class="mobile-call-btn call-now-btn">📞 Call Now</a>
        <a href="sms:{phone}" class="mobile-call-btn sms-btn">💬 Send SMS</a>
        <a href="https://wa.me/{phone}" target="_blank" class="mobile-call-btn whatsapp-btn">💚 WhatsApp</a>
    </div>
    '''

# ==================== MAIN APP ====================
def main():
    init_db()
    adb_connected, device_id = check_adb()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <span class="logo">📞</span>
            <h3>Call Flow CRM</h3>
            <div class="creator-name">by <span>Pankaj Jadhav</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # ADB Status
        if adb_connected:
            st.markdown(f'<div class="adb-status adb-connected">✅ Device Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="adb-status adb-disconnected">❌ Device Disconnected</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mode Selector
        st.markdown("""
        <div class="mode-selector">
            <div class="title">📱 Calling Mode</div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💻 Laptop", use_container_width=True, key="mode_laptop"):
                st.session_state.call_mode = "Laptop"
                st.rerun()
        with col2:
            if st.button("📱 Mobile", use_container_width=True, key="mode_mobile"):
                st.session_state.call_mode = "Mobile"
                st.rerun()
        
        if st.session_state.call_mode == "Laptop":
            st.markdown('<div class="mode-status-text" style="background:#d4edda;color:#155724;">💻 Laptop Mode Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="mode-status-text" style="background:#cce5ff;color:#004085;">📱 Mobile Mode Active</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        menu = st.radio(
            "📋 Menu",
            ["📞 Call", "📊 History", "📂 Import", "📋 Reports"],
            index=0,
            key="menu_nav"
        )
        
        st.markdown("---")
        
        # Import Section
        if menu == "📂 Import":
            st.markdown("**📤 Import Excel**")
            uploaded_file = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                st.caption(f"📊 {len(df)} records found")
                cols = df.columns.tolist()
                name_col = st.selectbox("Name Column", cols, index=0, key="name_col")
                phone_col = st.selectbox("Phone Column", cols, index=1 if len(cols) > 1 else 0, key="phone_col")
                if st.button("🚀 Import Now", use_container_width=True):
                    imported = import_from_excel(df, name_col, phone_col)
                    st.success(f"✅ {imported} customers imported!")
                    st.balloons()
                    st.rerun()
        
        if st.button("🗑️ Clear All Data", use_container_width=True):
            clear_database()
            st.success("✅ Data cleared!")
            st.rerun()
        
        st.markdown("---")
        st.caption("⚡ v3.0 | Made with ❤️")
    
    # ===== CALL SCREEN =====
    if menu == "📞 Call":
        # ===== HEADER =====
        st.markdown("""
        <div class="main-header">
            <div class="brand">
                <span class="logo-icon">📞</span>
                <div class="title-group">
                    <h1>Call Flow CRM</h1>
                    <div class="subtitle">Professional Telecalling Solution</div>
                </div>
            </div>
            <div class="creator">
                👨‍💻 <span>Pankaj Jadhav</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        customers = get_all_customers()
        if not customers:
            st.warning("No customers found. Please import data first.")
            return
        
        # ===== SEARCH & FILTER =====
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        with col1:
            search_term = st.text_input("🔍 Search", placeholder="Search by name or phone...", key="search")
        with col2:
            status_filter = st.selectbox("📊 Filter", ["All", "Pending", "Not Reachable", "Mobile Off", "Interested", "Call Back"], key="filter")
        with col3:
            sort_by = st.selectbox("📌 Sort", ["ID", "Name", "Status", "Date"], key="sort")
        
        # Apply filters
        filtered_customers = customers
        if search_term and len(search_term) >= 2:
            filtered_customers = [c for c in filtered_customers if search_term.lower() in c[1].lower() or search_term in c[2]]
        if status_filter != "All":
            if status_filter == "Pending":
                filtered_customers = [c for c in filtered_customers if not c[3] or c[3] == ""]
            else:
                filtered_customers = [c for c in filtered_customers if c[3] == status_filter]
        if sort_by == "Name":
            filtered_customers = sorted(filtered_customers, key=lambda x: x[1])
        elif sort_by == "Status":
            filtered_customers = sorted(filtered_customers, key=lambda x: x[3] if x[3] else "")
        elif sort_by == "Date":
            filtered_customers = sorted(filtered_customers, key=lambda x: x[5] if x[5] else "", reverse=True)
        
        if not filtered_customers:
            st.info("No customers match your filters.")
            return
        
        # Progress
        if 'index' not in st.session_state:
            st.session_state.index = 0
        if st.session_state.index >= len(filtered_customers):
            st.session_state.index = len(filtered_customers) - 1
        
        customer = filtered_customers[st.session_state.index]
        cust_id, name, phone, status, notes, call_date, call_time, followup_date = customer
        
        # Progress Bar
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            progress_value = (st.session_state.index + 1) / len(filtered_customers)
            st.progress(progress_value)
            st.caption(f"📌 Customer {st.session_state.index + 1} of {len(filtered_customers)}")
        
        # ===== MAIN LAYOUT =====
        col_left, col_right = st.columns([7, 3])
        
        with col_left:
            # ===== CUSTOMER CARD =====
            st.markdown(f"""
            <div class="customer-card">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div class="name">👤 {name}</div>
                        <div class="phone">📞 {phone}</div>
                        <div class="info">
                            Status: <span class="status-badge">{status if status else 'Pending'}</span>
                            {f" | 📅 {call_date} {call_time}" if call_date else ''}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ===== PHONE CONTROLS =====
            if st.session_state.call_mode == "Laptop":
                if f"phone_{cust_id}" not in st.session_state:
                    st.session_state[f"phone_{cust_id}"] = phone
                
                st.markdown("**📱 Phone Controls**")
                col1, col2, col3, col4 = st.columns([2, 0.8, 0.8, 0.8])
                with col1:
                    custom_phone = st.text_input("", value=st.session_state[f"phone_{cust_id}"], key=f"phone_{cust_id}", label_visibility="collapsed", placeholder="Enter phone number...")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{cust_id}", use_container_width=True):
                        if custom_phone and custom_phone != st.session_state[f"phone_{cust_id}"]:
                            if update_customer_phone(cust_id, custom_phone):
                                st.session_state[f"phone_{cust_id}"] = custom_phone
                                st.success("✅ Phone updated!")
                                st.rerun()
                with col3:
                    if st.button("📞 Call", key=f"call_{cust_id}", use_container_width=True):
                        call_phone = custom_phone if custom_phone else phone
                        if adb_connected:
                            success, msg = call_via_adb(call_phone)
                            if success:
                                st.success(f"✅ {msg}")
                                st.balloons()
                                update_customer_status(cust_id, status if status else "Pending", notes if notes else "")
                                # Auto move to next customer after call
                                if st.session_state.index < len(filtered_customers) - 1:
                                    st.session_state.index += 1
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Phone not connected!")
                with col4:
                    if st.button("⏹ End", key=f"end_{cust_id}", use_container_width=True):
                        if adb_connected:
                            success, msg = end_call_via_adb()
                            if success:
                                st.success(f"✅ {msg}")
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Phone not connected!")
            else:
                # Mobile Mode
                st.markdown("**📱 Mobile Direct Call**")
                mobile_html = get_mobile_call_html(phone)
                st.components.v1.html(mobile_html, height=150)
                st.info("📱 Click any button above to call directly from your mobile!")
            
            st.markdown("---")
            
            # ===== STATUS & WEEKDAYS =====
            st.markdown("**📌 Quick Status**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("✅ Interested", key=f"int_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Interested", notes if notes else "")
                    st.success("✅ Status: Interested")
                    st.balloons()
                    # Auto move to next customer after status update
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            with col2:
                if st.button("📞 Call Back", key=f"cb_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Call Back", notes if notes else "")
                    st.success("✅ Status: Call Back")
                    # Auto move to next customer after status update
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            with col3:
                if st.button("📵 Not Reachable", key=f"nr_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Not Reachable", notes if notes else "")
                    st.success("✅ Status: Not Reachable")
                    # Auto move to next customer after status update
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            with col4:
                if st.button("📱 Mobile Off", key=f"mo_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Mobile Off", notes if notes else "")
                    st.success("✅ Status: Mobile Off")
                    # Auto move to next customer after status update
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            
            st.markdown("**📅 Weekday Meetings**")
            col1, col2, col3, col4, col5 = st.columns(5)
            days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
            for i, day in enumerate(days):
                with [col1, col2, col3, col4, col5][i]:
                    if st.button(f"📅 {day}", key=f"day_{day}_{cust_id}", use_container_width=True):
                        update_customer_status(cust_id, f"Meeting {day}", notes if notes else "")
                        st.success(f"✅ Meeting {day}")
                        # Auto move to next customer after status update
                        if st.session_state.index < len(filtered_customers) - 1:
                            st.session_state.index += 1
                        st.rerun()
            
            st.markdown("**✏️ Custom Status**")
            col1, col2 = st.columns([3, 1])
            with col1:
                custom_status = st.text_input("", placeholder="Type custom status...", key=f"custom_{cust_id}", label_visibility="collapsed")
            with col2:
                if st.button("Set Status", key=f"set_custom_{cust_id}", use_container_width=True):
                    if custom_status and custom_status.strip():
                        update_customer_status(cust_id, custom_status.strip(), notes if notes else "")
                        st.success(f"✅ Status: {custom_status.strip()}")
                        st.balloons()
                        # Auto move to next customer after status update
                        if st.session_state.index < len(filtered_customers) - 1:
                            st.session_state.index += 1
                        st.rerun()
            
            st.markdown("---")
            
            # ===== NOTES & FOLLOW-UP =====
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("**📝 Notes**")
                notes_text = st.text_area("", value=notes if notes else "", height=50, key=f"notes_{cust_id}", placeholder="Add notes here...")
            with col2:
                st.markdown("**📅 Follow-up**")
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    followup_date = st.date_input("", value=datetime.now().date(), min_value=datetime.now().date(), key=f"followup_{cust_id}", label_visibility="collapsed")
                with col_b:
                    if st.button("📌 Set", key=f"set_followup_{cust_id}", use_container_width=True):
                        update_customer_status(cust_id, status if status else "Call Back", notes if notes else "", followup_date.strftime("%Y-%m-%d"))
                        st.success(f"✅ Follow-up: {followup_date.strftime('%d-%m-%Y')}")
                        st.rerun()
                
                if st.button("💾 Save Notes", key=f"save_notes_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, status if status else "Pending", notes_text)
                    st.success("✅ Notes saved!")
                    st.rerun()
            
            st.markdown("---")
            
            # ===== NAVIGATION =====
            st.markdown("**🧭 Navigation**")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                if st.button("⏮ First", key="nav_first", use_container_width=True):
                    st.session_state.index = 0
                    st.rerun()
            with col2:
                if st.button("◀ Prev", key="nav_prev", use_container_width=True):
                    if st.session_state.index > 0:
                        st.session_state.index -= 1
                        st.rerun()
            with col3:
                if st.button("💾 Save", key="nav_save", use_container_width=True):
                    update_customer_status(cust_id, status if status else "Pending", notes_text)
                    st.success("✅ Saved!")
                    st.rerun()
            with col4:
                if st.button("Next ▶", key="nav_next", use_container_width=True):
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                        st.rerun()
            with col5:
                if st.button("Last ⏭", key="nav_last", use_container_width=True):
                    st.session_state.index = len(filtered_customers) - 1
                    st.rerun()
        
        with col_right:
            # ===== CURRENT STATUS =====
            st.markdown("""
            <div style="background:white;padding:0.8rem;border-radius:12px;border:1px solid #e8e8e8;margin-bottom:0.5rem;">
                <h4 style="margin:0 0 0.3rem 0;">📊 Current Status</h4>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <p style="margin:0.2rem 0;"><strong>Status:</strong> {status if status else 'Pending'}</p>
            <p style="margin:0.2rem 0;"><strong>Last Call:</strong> {call_date if call_date else 'N/A'}</p>
            <p style="margin:0.2rem 0;"><strong>Time:</strong> {call_time if call_time else 'N/A'}</p>
            <p style="margin:0.2rem 0;"><strong>Follow-up:</strong> {followup_date if followup_date else 'Not set'}</p>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # ===== STATISTICS =====
            st.markdown("### 📈 Live Statistics")
            all_customers = get_all_customers()
            total = len(all_customers)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{total}</div>
                    <div class="label">Total</div>
                </div>
                """, unsafe_allow_html=True)
                interested = len([c for c in all_customers if c[3] == "Interested"])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{interested}</div>
                    <div class="label">Interested</div>
                </div>
                """, unsafe_allow_html=True)
                not_reachable = len([c for c in all_customers if c[3] == "Not Reachable"])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{not_reachable}</div>
                    <div class="label">Not Reachable</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                pending = len([c for c in all_customers if not c[3] or c[3] == ""])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{pending}</div>
                    <div class="label">Pending</div>
                </div>
                """, unsafe_allow_html=True)
                callback = len([c for c in all_customers if c[3] == "Call Back"])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{callback}</div>
                    <div class="label">Call Back</div>
                </div>
                """, unsafe_allow_html=True)
                completed = len([c for c in all_customers if c[3] == "Completed"])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="value">{completed}</div>
                    <div class="label">Completed</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Today's calls
            today = datetime.now().strftime("%Y-%m-%d")
            today_calls = len([c for c in all_customers if c[5] == today])
            st.markdown(f"""
            <div class="metric-box" style="margin-top:0.3rem;">
                <div class="value">{today_calls}</div>
                <div class="label">Today's Calls</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Follow-ups due
            today_date = datetime.now().date()
            followups_due = len([c for c in all_customers if c[7] and datetime.strptime(c[7], "%Y-%m-%d").date() <= today_date])
            st.markdown(f"""
            <div class="metric-box" style="margin-top:0.3rem;">
                <div class="value">{followups_due}</div>
                <div class="label">Follow-ups Due</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== HISTORY =====
    elif menu == "📊 History":
        st.markdown("## 📊 Call History")
        customers = get_all_customers()
        if not customers:
            st.warning("No customers found!")
            return
        
        col1, col2, col3 = st.columns(3)
        with col1:
            date_option = st.selectbox("📅 Date Range", ["All", "Today", "Yesterday", "Last 7 Days", "Last 30 Days"])
        with col2:
            if date_option == "Custom":
                custom_date = st.date_input("Select Date", value=datetime.now().date())
        with col3:
            status_filter = st.selectbox("📊 Status", ["All", "Pending", "Not Reachable", "Mobile Off", "Interested", "Call Back", "Completed"])
        
        filtered = customers
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        last_7_days = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        last_30_days = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        if date_option == "Today":
            filtered = [c for c in filtered if c[5] == today]
        elif date_option == "Yesterday":
            filtered = [c for c in filtered if c[5] == yesterday]
        elif date_option == "Last 7 Days":
            filtered = [c for c in filtered if c[5] and c[5] >= last_7_days]
        elif date_option == "Last 30 Days":
            filtered = [c for c in filtered if c[5] and c[5] >= last_30_days]
        
        if status_filter != "All":
            if status_filter == "Pending":
                filtered = [c for c in filtered if not c[3] or c[3] == ""]
            else:
                filtered = [c for c in filtered if c[3] == status_filter]
        
        st.markdown(f"**Found {len(filtered)} records**")
        if filtered:
            df = pd.DataFrame(filtered, columns=["ID", "Name", "Phone", "Status", "Notes", "Date", "Time", "Follow-up"])
            df_display = df[["Name", "Phone", "Status", "Date", "Time"]]
            st.dataframe(df_display, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_display.to_excel(writer, index=False)
                st.download_button("📥 Download Excel", data=output.getvalue(), file_name=f"history_{datetime.now().strftime('%Y%m%d')}.xlsx", use_container_width=True)
    
    # ===== REPORTS =====
    elif menu == "📋 Reports":
        st.markdown("## 📋 Reports")
        conn = sqlite3.connect('crm_data.db')
        df = pd.read_sql_query("SELECT * FROM customers WHERE status IS NOT NULL AND status != '' ORDER BY id", conn)
        conn.close()
        
        if df.empty:
            st.info("No data available yet.")
        else:
            df.insert(0, 'Sr No', range(1, len(df) + 1))
            report_df = df[['Sr No', 'name', 'phone', 'status', 'call_date', 'call_time']]
            report_df.columns = ['Sr No', 'Name', 'Phone', 'Status', 'Date', 'Time']
            st.success(f"✅ Total Calls: {len(report_df)}")
            st.dataframe(report_df, use_container_width=True)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                report_df.to_excel(writer, sheet_name='Call Report', index=False)
            st.download_button("📥 Download Excel Report", data=output.getvalue(), file_name=f"report_{datetime.now().strftime('%Y%m%d')}.xlsx", use_container_width=True)

if __name__ == "__main__":
    main()

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    ⚡ <strong>Call Flow CRM</strong> | Made with <span class="heart">❤️</span> by <span class="name">Pankaj Jadhav</span> | v3.0
</div>
""", unsafe_allow_html=True)
