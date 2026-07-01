import streamlit as st
import pandas as pd
import sqlite3
import os
import webbrowser
import urllib.parse
import subprocess
from datetime import datetime
import io
import base64
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Calling CRM - Pankaj Jadhav",
    page_icon="📞",
    layout="wide"
)

# ==================== CSS ====================
st.markdown("""
<style>
    /* ===== GLOBAL RESET ===== */
    .main > div {
        padding: 0.1rem 0.5rem !important;
    }
    
    /* ===== HEADER - WHITE BACKGROUND ===== */
    .main-header {
        background: #ffffff !important;
        padding: 0.5rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: #000000 !important;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.4rem;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        letter-spacing: 1px;
        font-weight: bold;
    }
    .main-header p {
        margin: 0;
        opacity: 0.6;
        font-size: 0.6rem;
        color: #636e72 !important;
        letter-spacing: 2px;
    }
    
    /* ===== SEARCH BAR ===== */
    .search-container {
        background: #ffffff;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        border: 2px solid #6c5ce7;
        box-shadow: 0 2px 15px rgba(108, 92, 231, 0.1);
        margin-bottom: 0.5rem;
    }
    .search-container input {
        border: none !important;
        outline: none !important;
        font-size: 1rem !important;
        padding: 0.5rem !important;
        width: 100% !important;
        background: transparent !important;
    }
    .search-container input:focus {
        box-shadow: none !important;
        border: none !important;
    }
    .search-icon {
        color: #6c5ce7;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    /* ===== SEARCH RESULTS ===== */
    .search-result {
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #6c5ce7;
        margin-bottom: 0.3rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    .search-result:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
    .search-result-name {
        font-weight: bold;
        color: #000000;
        font-size: 0.9rem;
    }
    .search-result-phone {
        color: #6c5ce7;
        font-size: 0.8rem;
    }
    
    /* ===== METRIC CARDS - WHITE BACKGROUND ===== */
    .metric-card {
        background: #ffffff !important;
        padding: 0.4rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .metric-card:hover {
        border-color: #6c5ce7;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.15);
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #6c5ce7;
    }
    .metric-label {
        font-size: 0.5rem;
        opacity: 0.6;
        color: #636e72;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ===== CUSTOMER CARD - WHITE BACKGROUND ===== */
    .customer-card {
        background: #ffffff !important;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #6c5ce7;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
    }
    .customer-name {
        font-size: 1.4rem;
        font-weight: bold;
        color: #000000 !important;
        margin: 0;
    }
    .customer-phone {
        font-size: 1.1rem;
        color: #6c5ce7 !important;
        margin: 0;
    }
    .customer-status {
        color: #636e72 !important;
        font-size: 0.75rem;
        margin-top: 3px;
    }
    .customer-status strong {
        color: #6c5ce7 !important;
    }
    
    /* ===== BIG CALLING NUMBER ===== */
    .calling-number-big {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.6rem !important;
        font-weight: bold;
        margin: 0.3rem 0;
        box-shadow: 0 4px 20px rgba(108, 92, 231, 0.3);
        letter-spacing: 2px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    .calling-number-big small {
        font-size: 0.7rem;
        opacity: 0.8;
        font-weight: normal;
        display: block;
        margin-bottom: 0.2rem;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0;
        border-bottom: 2px solid rgba(108, 92, 231, 0.2);
        margin-bottom: 0.5rem;
    }
    .sidebar-brand h3 {
        color: #6c5ce7;
        margin: 0;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }
    .sidebar-brand p {
        color: #b2bec3;
        font-size: 0.6rem;
        margin: 0;
        opacity: 0.6;
    }
    
    /* ===== ADB STATUS ===== */
    .adb-status {
        padding: 0.3rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 0.75rem;
        letter-spacing: 1px;
    }
    .adb-connected {
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        box-shadow: 0 2px 10px rgba(0, 206, 201, 0.2);
    }
    .adb-disconnected {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        color: #6c5ce7;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 1px solid rgba(108, 92, 231, 0.15);
        padding-bottom: 0.2rem;
        margin-bottom: 0.3rem;
        font-weight: bold;
    }
    
    /* ===== BIG CALL BUTTONS ===== */
    .big-btn-call > button {
        background: linear-gradient(135deg, #00b894, #00cec9) !important;
        color: white !important;
        padding: 0.8rem 0.5rem !important;
        font-size: 1.4rem !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 206, 201, 0.3) !important;
        transition: all 0.3s !important;
        width: 100% !important;
        height: auto !important;
    }
    .big-btn-call > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 4px 30px rgba(0, 206, 201, 0.5) !important;
    }
    
    .big-btn-end > button {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        padding: 0.8rem 0.5rem !important;
        font-size: 1.4rem !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.3s !important;
        width: 100% !important;
        height: auto !important;
    }
    .big-btn-end > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 4px 30px rgba(255, 107, 107, 0.5) !important;
    }
    
    /* ===== BIG STATUS BUTTONS ===== */
    .status-btn > button {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
        color: #2d3436 !important;
        padding: 0.6rem 0.3rem !important;
        font-size: 0.85rem !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: 2px solid #6c5ce7 !important;
        transition: all 0.3s !important;
        width: 100% !important;
        height: auto !important;
        text-align: center !important;
        white-space: nowrap !important;
        box-shadow: 0 2px 8px rgba(108, 92, 231, 0.1) !important;
    }
    .status-btn > button:hover {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
        color: white !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 20px rgba(108, 92, 231, 0.4) !important;
        border-color: #6c5ce7 !important;
    }
    
    /* ===== SMALL BUTTONS ===== */
    .small-btn > button {
        padding: 0.1rem 0.2rem !important;
        font-size: 0.55rem !important;
        border-radius: 4px !important;
        font-weight: normal !important;
        background: rgba(108, 92, 231, 0.08) !important;
        color: #636e72 !important;
        border: 1px solid rgba(108, 92, 231, 0.15) !important;
        transition: all 0.2s !important;
        width: 100% !important;
        height: auto !important;
        min-height: 22px !important;
    }
    .small-btn > button:hover {
        background: rgba(108, 92, 231, 0.15) !important;
        color: #2d3436 !important;
        border-color: #6c5ce7 !important;
        transform: scale(1.02) !important;
    }
    
    /* ===== AUDIO BUTTONS ===== */
    .audio-btn > button {
        padding: 0.1rem 0.2rem !important;
        font-size: 0.55rem !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: auto !important;
        min-height: 22px !important;
        border: 1px solid transparent !important;
        transition: all 0.2s !important;
    }
    .audio-on > button {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
        color: white !important;
    }
    .audio-on > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 2px 10px rgba(108, 92, 231, 0.3) !important;
    }
    .audio-off > button {
        background: linear-gradient(135deg, #b2bec3, #636e72) !important;
        color: white !important;
    }
    .audio-off > button:hover {
        transform: scale(1.02) !important;
    }
    .audio-vol > button {
        background: linear-gradient(135deg, #fdcb6e, #f39c12) !important;
        color: white !important;
    }
    .audio-vol > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 2px 10px rgba(243, 156, 18, 0.3) !important;
    }
    
    /* ===== INPUTS ===== */
    .stTextInput > div > div > input {
        padding: 0.3rem 0.5rem !important;
        font-size: 0.8rem !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        border: 1px solid #dfe6e9 !important;
        color: #2d3436 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6c5ce7 !important;
        box-shadow: 0 0 15px rgba(108, 92, 231, 0.15) !important;
    }
    
    .stTextArea > div > div > textarea {
        padding: 0.3rem 0.5rem !important;
        font-size: 0.7rem !important;
        min-height: 30px !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        border: 1px solid #dfe6e9 !important;
        color: #2d3436 !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #6c5ce7 !important;
        box-shadow: 0 0 15px rgba(108, 92, 231, 0.15) !important;
    }
    
    .stAlert {
        padding: 0.2rem 0.5rem !important;
        margin: 0.2rem 0 !important;
        font-size: 0.7rem !important;
        border-radius: 8px !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe) !important;
        border-radius: 4px !important;
    }
    .stProgress > div {
        height: 4px !important;
        background: rgba(26, 26, 46, 0.1) !important;
        border-radius: 4px !important;
    }
    
    .stCaption {
        font-size: 0.5rem !important;
        color: #b2bec3 !important;
        opacity: 0.6 !important;
    }
    
    .info-box {
        background: rgba(108, 92, 231, 0.08);
        padding: 0.3rem 0.5rem;
        border-radius: 8px;
        border-left: 3px solid #6c5ce7;
        font-size: 0.7rem;
        color: #2d3436;
        margin: 0.3rem 0;
    }
    .info-box strong {
        color: #6c5ce7;
    }
    
    .stRadio > div {
        gap: 0.2rem !important;
    }
    .stRadio label {
        font-size: 0.7rem !important;
        color: #b2bec3 !important;
    }
    .stRadio label:hover {
        color: white !important;
    }
    
    .custom-divider {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(108, 92, 231, 0.2), transparent);
        margin: 0.3rem 0;
    }
    
    .status-indicator {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 4px;
    }
    .status-on {
        background: #00b894;
        box-shadow: 0 0 10px rgba(0, 206, 201, 0.3);
    }
    .status-off {
        background: #ff6b6b;
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
    }
    
    .footer {
        text-align: center;
        padding: 0.3rem;
        color: #b2bec3;
        font-size: 0.5rem;
        border-top: 1px solid rgba(108, 92, 231, 0.1);
        margin-top: 0.5rem;
    }
    
    .row-widget.stColumns {
        gap: 0.3rem !important;
    }
    .stMarkdown h2 {
        font-size: 0.9rem !important;
        margin: 0.3rem 0 !important;
        color: #6c5ce7 !important;
        letter-spacing: 1px;
    }
    .stMarkdown h3 {
        font-size: 0.65rem !important;
        margin: 0.2rem 0 !important;
        color: #b2bec3 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stMarkdown p {
        margin: 0.1rem 0 !important;
        font-size: 0.7rem !important;
    }
    
    .speaker-status-text {
        font-size: 0.55rem !important;
        color: #636e72 !important;
        margin-top: 0.1rem !important;
    }
    
    /* ===== NO RESULTS ===== */
    .no-results {
        text-align: center;
        padding: 1rem;
        color: #636e72;
        font-size: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px dashed #dfe6e9;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
def init_db():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        status TEXT,
        notes TEXT,
        call_date TEXT,
        call_time TEXT
    )''')
    conn.commit()
    conn.close()

def update_customer_status(customer_id, status, notes):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    now = datetime.now()
    c.execute("""
        UPDATE customers 
        SET status=?, notes=?, call_date=?, call_time=?
        WHERE id=?
    """, (status, notes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), customer_id))
    conn.commit()
    conn.close()

def get_all_customers():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id")
    data = c.fetchall()
    conn.close()
    return data

def get_called_customers():
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE status IS NOT NULL AND status != '' ORDER BY id")
    data = c.fetchall()
    conn.close()
    return data

def search_customers(search_term):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    # Search by name or phone
    c.execute("""
        SELECT * FROM customers 
        WHERE name LIKE ? OR phone LIKE ?
        ORDER BY id
    """, (f'%{search_term}%', f'%{search_term}%'))
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
    skipped = 0
    
    for _, row in df.iterrows():
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ''
        phone = str(row[phone_col]).strip() if pd.notna(row[phone_col]) else ''
        phone = ''.join(filter(str.isdigit, phone))
        
        if name and phone:
            c.execute("SELECT * FROM customers WHERE name=? AND phone=?", (name, phone))
            if not c.fetchone():
                c.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
                imported += 1
            else:
                skipped += 1
    
    conn.commit()
    conn.close()
    return imported, skipped

def auto_detect_columns(df):
    name_col = None
    phone_col = None
    
    name_patterns = ['name', 'names', 'customer', 'customer name', 'full name', 
                     'contact', 'contact name', 'client', 'client name', 'person']
    
    phone_patterns = ['phone', 'phones', 'phone number', 'mobile', 'mobile number', 
                      'contact no', 'contact number', 'telephone', 'cell', 'cell number',
                      'ph no', 'ph.', 'mob', 'mob no']
    
    col_lower = {col: col.lower().strip() for col in df.columns}
    
    for col, col_low in col_lower.items():
        if any(pattern in col_low for pattern in name_patterns):
            name_col = col
            break
    
    for col, col_low in col_lower.items():
        if any(pattern in col_low for pattern in phone_patterns):
            phone_col = col
            break
    
    if name_col is None:
        for col in df.columns:
            if df[col].dtype == 'object':
                sample = df[col].dropna().astype(str)
                if len(sample) > 0:
                    if sample.str.contains('[a-zA-Z]').mean() > 0.5:
                        name_col = col
                        break
    
    if phone_col is None:
        for col in df.columns:
            sample = df[col].dropna().astype(str)
            if len(sample) > 0:
                if sample.str.replace(r'[\s\+\-\(\)]', '', regex=True).str.isdigit().mean() > 0.5:
                    phone_col = col
                    break
    
    if name_col is None and len(df.columns) > 0:
        name_col = df.columns[0]
    if phone_col is None and len(df.columns) > 1:
        phone_col = df.columns[1]
    
    return name_col, phone_col

# ==================== CALL FUNCTIONS ====================
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
            return False, "Please enter a valid phone number!"
        
        check_result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        if 'device' not in check_result.stdout:
            return False, "Phone not connected!"
        
        cmd = ['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone}']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return True, f"Calling {phone}!"
        else:
            return False, "ADB Error!"
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

# ==================== VOLUME & SPEAKER ====================
def volume_up():
    try:
        cmd = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_VOLUME_UP']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Volume Up!"
        else:
            return False, "Error increasing volume!"
    except:
        return False, "Error!"

def volume_down():
    try:
        cmd = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_VOLUME_DOWN']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Volume Down!"
        else:
            return False, "Error decreasing volume!"
    except:
        return False, "Error!"

def speaker_on():
    try:
        cmd = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_HEADSETHOOK']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Speaker ON!"
        else:
            return False, "Error turning speaker ON!"
    except:
        return False, "Error!"

def speaker_off():
    try:
        cmd = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_HEADSETHOOK']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "Speaker OFF!"
        else:
            return False, "Error turning speaker OFF!"
    except:
        return False, "Error!"

# ==================== REPORT FUNCTIONS ====================
def generate_report_data():
    conn = sqlite3.connect('crm_data.db')
    df = pd.read_sql_query("SELECT * FROM customers WHERE status IS NOT NULL AND status != '' ORDER BY id", conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()
    
    df.insert(0, 'Sr No', range(1, len(df) + 1))
    report_df = df[['Sr No', 'name', 'phone', 'status', 'call_date']]
    report_df.columns = ['Sr No', 'Name', 'Phone', 'Status', 'Date']
    
    return report_df

def download_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Call Report', index=False)
    output.seek(0)
    return output

def create_pdf_html(df):
    if df.empty:
        return ""
    
    rows = ""
    for _, row in df.iterrows():
        rows += f"""
            <tr>
                <td style="padding: 6px; border-bottom: 1px solid #ddd; text-align: center;">{row['Sr No']}</td>
                <td style="padding: 6px; border-bottom: 1px solid #ddd;">{row['Name']}</td>
                <td style="padding: 6px; border-bottom: 1px solid #ddd;">{row['Phone']}</td>
                <td style="padding: 6px; border-bottom: 1px solid #ddd;">{row['Status']}</td>
                <td style="padding: 6px; border-bottom: 1px solid #ddd; text-align: center;">{row['Date'] if row['Date'] else '-'}</td>
            </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Call Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            .header {{ background: linear-gradient(135deg, #0f0c29, #302b63); color: white; padding: 15px; border-radius: 8px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 22px; }}
            .header p {{ margin: 5px 0 0 0; opacity: 0.8; font-size: 12px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }}
            th {{ background: #6c5ce7; color: white; padding: 8px; text-align: left; }}
            td {{ padding: 6px 8px; border-bottom: 1px solid #e0e0e0; }}
            tr:hover {{ background: #f0f0ff; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 11px; }}
            .count {{ background: #6c5ce7; color: white; padding: 3px 10px; border-radius: 15px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📞 Call Report</h1>
                <p>Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')} | Total: <span class="count">{len(df)}</span></p>
            </div>
            <table>
                <tr>
                    <th>Sr No</th>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Status</th>
                    <th>Date</th>
                </tr>
                {rows}
            </table>
            <div class="footer">Made with ❤️ | Calling CRM by Pankaj Jadhav</div>
        </div>
    </body>
    </html>
    """
    
    return html

# ==================== MAIN APP ====================
def main():
    init_db()
    
    # ===== HEADER - WHITE BACKGROUND =====
    st.markdown("""
    <div class="main-header">
        <h1>📞 Calling CRM</h1>
        <p>by Pankaj Jadhav</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== ADB STATUS =====
    adb_connected, device_id = check_adb()
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <h3>📞 CRM</h3>
            <p>by Pankaj Jadhav</p>
        </div>
        """, unsafe_allow_html=True)
        
        if adb_connected:
            st.markdown(f"""
            <div class="adb-status adb-connected">
                ✅ Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="adb-status adb-disconnected">
                ❌ Not Connected
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "📋 Menu",
            ["📞 Call", "📊 Reports", "📂 Import"],
            index=0
        )
        
        st.markdown("---")
        
        if menu == "📂 Import":
            st.markdown("### 📂 Import Excel")
            st.caption("Auto-detect Name & Phone columns")
            
            uploaded_file = st.file_uploader("Choose Excel file", type=["xlsx", "xls"], label_visibility="collapsed")
            
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    name_col, phone_col = auto_detect_columns(df)
                    
                    st.write(f"📊 **{len(df)}** records found")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"✅ **Name Column:** `{name_col}`" if name_col else "❌ Name column not found")
                    with col2:
                        st.markdown(f"✅ **Phone Column:** `{phone_col}`" if phone_col else "❌ Phone column not found")
                    
                    with st.expander("📋 Preview Data"):
                        preview_df = df.head(5)[[name_col, phone_col]] if name_col and phone_col else df.head(5)
                        st.dataframe(preview_df, use_container_width=True)
                    
                    if st.button("🚀 Import Data", use_container_width=True, type="primary"):
                        if name_col and phone_col:
                            imported, skipped = import_from_excel(df, name_col, phone_col)
                            st.success(f"✅ {imported} records imported! ({skipped} skipped)")
                            if imported > 0:
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("❌ Could not detect Name and Phone columns!")
                            
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Data", use_container_width=True):
            clear_database()
            st.success("✅ Cleared!")
            st.rerun()
        
        st.markdown("---")
        st.caption("📞 v2.0")
    
    # ===== CALL SCREEN =====
    if menu == "📞 Call":
        customers = get_all_customers()
        
        if not customers:
            st.warning("No customers! Please import Excel from sidebar.")
            return
        
        # Initialize session state
        if 'index' not in st.session_state:
            st.session_state.index = 0
        if 'speaker_status' not in st.session_state:
            st.session_state.speaker_status = False
        if 'search_mode' not in st.session_state:
            st.session_state.search_mode = False
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
        if 'selected_customer' not in st.session_state:
            st.session_state.selected_customer = None
        
        # ===== SEARCH BAR =====
        st.markdown("### 🔍 Search Customer")
        
        search_col1, search_col2 = st.columns([5, 1])
        with search_col1:
            search_term = st.text_input(
                "Search by Name or Phone", 
                placeholder="Type name or phone number...",
                label_visibility="collapsed",
                key="search_input"
            )
        with search_col2:
            if st.button("🔍 Search", use_container_width=True):
                if search_term.strip():
                    results = search_customers(search_term.strip())
                    if results:
                        st.session_state.search_mode = True
                        st.session_state.search_results = results
                        st.session_state.selected_customer = None
                        st.rerun()
                    else:
                        st.warning("No customers found!")
                else:
                    st.session_state.search_mode = False
                    st.session_state.search_results = []
                    st.rerun()
        
        # ===== SHOW SEARCH RESULTS OR NORMAL VIEW =====
        if st.session_state.search_mode and st.session_state.search_results:
            st.markdown("### 📋 Search Results")
            st.caption(f"Found {len(st.session_state.search_results)} customer(s)")
            
            # Show search results as clickable list
            for cust in st.session_state.search_results:
                cust_id, name, phone, status, notes, call_date, call_time = cust
                status_display = status if status else "Pending"
                
                col1, col2, col3 = st.columns([4, 3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="search-result">
                        <div class="search-result-name">👤 {name}</div>
                        <div class="search-result-phone">📞 {phone}</div>
                        <small style="color:#636e72;">Status: {status_display}</small>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button(f"📞 Call", key=f"search_call_{cust_id}", use_container_width=True):
                        st.session_state.selected_customer = cust
                        st.session_state.search_mode = False
                        st.session_state.index = customers.index(cust)
                        st.rerun()
                with col3:
                    if st.button(f"✏️ Select", key=f"search_select_{cust_id}", use_container_width=True):
                        st.session_state.selected_customer = cust
                        st.session_state.search_mode = False
                        st.session_state.index = customers.index(cust)
                        st.rerun()
            
            # Clear search button
            if st.button("🔄 Clear Search", use_container_width=True):
                st.session_state.search_mode = False
                st.session_state.search_results = []
                st.session_state.selected_customer = None
                st.rerun()
        
        else:
            # ===== NORMAL VIEW - Current Customer =====
            if st.session_state.index >= len(customers):
                st.session_state.index = len(customers) - 1
            if st.session_state.index < 0:
                st.session_state.index = 0
            
            customer = customers[st.session_state.index]
            cust_id, name, phone, status, notes, call_date, call_time = customer
            
            st.session_state.current_customer_id = cust_id
            st.session_state.current_phone = phone
            
            # ===== METRICS =====
            called = get_called_customers()
            total = len(customers)
            called_count = len(called)
            pending = total - called_count
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total}</div>
                    <div class="metric-label">Total</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{called_count}</div>
                    <div class="metric-label">Called</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{pending}</div>
                    <div class="metric-label">Pending</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                progress_pct = int(((st.session_state.index + 1) / len(customers)) * 100)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{progress_pct}%</div>
                    <div class="metric-label">Progress</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.progress((st.session_state.index + 1) / len(customers))
            st.caption(f"📌 {st.session_state.index + 1} / {len(customers)}")
            
            # ===== MAIN TWO-COLUMN LAYOUT =====
            left_col, right_col = st.columns([4, 5])
            
            # ===== LEFT COLUMN =====
            with left_col:
                st.markdown(f"""
                <div class="customer-card">
                    <div class="customer-name">👤 {name}</div>
                    <div class="customer-phone">📞 {phone}</div>
                    <div class="customer-status">
                        Status: <strong>{status if status else 'Pending'}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    custom_phone = st.text_input("📱 Phone", value=phone, key=f"edit_phone_{cust_id}", label_visibility="collapsed")
                with col2:
                    if st.button("✏️ Update", use_container_width=True, key=f"update_btn_{cust_id}"):
                        if custom_phone != phone:
                            conn = sqlite3.connect('crm_data.db')
                            c = conn.cursor()
                            c.execute("UPDATE customers SET phone=? WHERE id=?", (custom_phone, cust_id))
                            conn.commit()
                            conn.close()
                            st.success("✅ Updated!")
                            st.session_state.current_phone = custom_phone
                            st.rerun()
                
                notes_text = st.text_area("📝 Notes", value=notes if notes else "", height=30, key=f"notes_{cust_id}", label_visibility="collapsed")
                
                st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
                
                # ===== NAVIGATION (SMALL) =====
                st.markdown('<p class="section-title">📍 Navigation</p>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("⏮ First", use_container_width=True):
                        st.session_state.index = 0
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("⬅ Prev", use_container_width=True):
                        if st.session_state.index > 0:
                            st.session_state.index -= 1
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("💾 Save", use_container_width=True):
                        update_customer_status(cust_id, status if status else "Pending", notes_text if notes_text else "")
                        st.success("✅ Saved!")
                        if st.session_state.index < len(customers) - 1:
                            st.session_state.index += 1
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with col4:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("Next ➡", use_container_width=True):
                        if st.session_state.index < len(customers) - 1:
                            st.session_state.index += 1
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # ===== AUDIO (SMALL) =====
                st.markdown('<p class="section-title">🔊 Audio</p>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.session_state.speaker_status:
                        st.markdown('<div class="audio-btn audio-on">', unsafe_allow_html=True)
                        if st.button("🔊 ON", use_container_width=True):
                            if adb_connected:
                                success, msg = speaker_on()
                                if success:
                                    st.success("✅ ON!")
                                    st.session_state.speaker_status = True
                                    st.rerun()
                                else:
                                    st.error(f"❌ {msg}")
                            else:
                                st.error("❌ Not connected!")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="audio-btn audio-off">', unsafe_allow_html=True)
                        if st.button("🔇 OFF", use_container_width=True):
                            if adb_connected:
                                success, msg = speaker_off()
                                if success:
                                    st.success("✅ OFF!")
                                    st.session_state.speaker_status = False
                                    st.rerun()
                                else:
                                    st.error(f"❌ {msg}")
                            else:
                                st.error("❌ Not connected!")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="audio-btn audio-vol">', unsafe_allow_html=True)
                    if st.button("🔄 Toggle", use_container_width=True):
                        if adb_connected:
                            if st.session_state.speaker_status:
                                success, msg = speaker_off()
                                if success:
                                    st.session_state.speaker_status = False
                                    st.rerun()
                            else:
                                success, msg = speaker_on()
                                if success:
                                    st.session_state.speaker_status = True
                                    st.rerun()
                            if success:
                                st.success(f"✅ {msg}")
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Not connected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="audio-btn audio-vol">', unsafe_allow_html=True)
                    if st.button("🔊 Vol +", use_container_width=True):
                        if adb_connected:
                            success, msg = volume_up()
                            if success:
                                st.success("✅ Vol +")
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Not connected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="audio-btn audio-vol">', unsafe_allow_html=True)
                    if st.button("🔉 Vol -", use_container_width=True):
                        if adb_connected:
                            success, msg = volume_down()
                            if success:
                                st.success("✅ Vol -")
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Not connected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                status_color = "status-on" if st.session_state.speaker_status else "status-off"
                status_text = "ON" if st.session_state.speaker_status else "OFF"
                st.caption(f'<span class="status-indicator {status_color}"></span> Speaker: {status_text}', unsafe_allow_html=True)
            
            # ===== RIGHT COLUMN =====
            with right_col:
                st.markdown('<p class="section-title">📞 Call Controls</p>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="big-btn-call">', unsafe_allow_html=True)
                    if st.button("📞 CALL", use_container_width=True, key=f"call_btn_{cust_id}"):
                        if adb_connected:
                            success, msg = call_via_adb(st.session_state.current_phone)
                            if success:
                                st.success(f"✅ {msg}")
                                st.session_state.call_active = True
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Phone not connected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="big-btn-end">', unsafe_allow_html=True)
                    if st.button("⏹ END", use_container_width=True, key=f"end_call_btn_{cust_id}"):
                        if adb_connected:
                            success, msg = end_call_via_adb()
                            if success:
                                st.success(f"✅ {msg}")
                                st.session_state.call_active = False
                            else:
                                st.error(f"❌ {msg}")
                        else:
                            st.error("❌ Phone not connected!")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # ===== BIG CALLING NUMBER =====
                st.markdown(f"""
                <div class="calling-number-big">
                    <small>📞 Calling</small>
                    {st.session_state.current_phone}
                </div>
                """, unsafe_allow_html=True)
                
                # ===== STATUS BUTTONS (BIG) =====
                st.markdown('<p class="section-title">📋 Status</p>', unsafe_allow_html=True)
                
                status_options = [
                    "No Response", "Not Reachable", "Mobile Off",
                    "Meeting Mon", "Meeting Tue", "Meeting Wed",
                    "Meeting Thu", "Meeting Fri", "1 Week Later"
                ]
                
                cols = st.columns(3)
                for i, option in enumerate(status_options):
                    col_idx = i % 3
                    with cols[col_idx]:
                        st.markdown('<div class="status-btn">', unsafe_allow_html=True)
                        if st.button(option, key=f"st_{i}_{cust_id}", use_container_width=True):
                            update_customer_status(cust_id, option, notes_text if notes_text else "")
                            st.success(f"✅ {option}")
                            if st.session_state.index < len(customers) - 1:
                                st.session_state.index += 1
                                st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== REPORTS =====
    elif menu == "📊 Reports":
        st.markdown("## 📊 Reports")
        
        report_df = generate_report_data()
        
        if report_df.empty:
            st.info("No called customers yet!")
        else:
            st.success(f"✅ Total Called: {len(report_df)}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                excel_file = download_excel(report_df)
                st.download_button(
                    label="📥 Excel Report",
                    data=excel_file,
                    file_name=f"call_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                html_content = create_pdf_html(report_df)
                b64 = base64.b64encode(html_content.encode()).decode()
                href = f'''
                <a href="data:text/html;base64,{b64}" 
                   target="_blank" 
                   style="display:block;text-align:center;padding:8px;background:#6c5ce7;color:white;border-radius:8px;text-decoration:none;font-weight:bold;font-size:0.8rem;">
                    📥 PDF Report
                </a>
                '''
                st.markdown(href, unsafe_allow_html=True)
            
            with st.expander("Preview"):
                st.dataframe(report_df, use_container_width=True)

if __name__ == "__main__":
    main()

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    Made with ❤️ by Pankaj Jadhav | Calling CRM v2.0
</div>
""", unsafe_allow_html=True)