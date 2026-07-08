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
    page_title="Calling CRM Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS WITH PREMIUM ANIMATIONS ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f6f9fc 0%, #e8f0fe 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Background with Particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 80%, rgba(236, 72, 153, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: gradientShift 20s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        33% { opacity: 0.8; transform: scale(1.05); }
        66% { opacity: 0.6; transform: scale(0.95); }
    }
    
    /* Floating particles animation */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    /* Main container with premium glassmorphism */
    .main-container {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
        animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 1;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Premium Header with animated gradient */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 30%, #a855f7 60%, #ec4899 100%);
        background-size: 300% 300%;
        padding: 1rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
        animation: gradientMove 4s ease-in-out infinite, slideDown 0.6s ease-out;
        position: relative;
        overflow: hidden;
        z-index: 2;
    }
    
    @keyframes gradientMove {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
        animation: shimmer 4s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
        100% { transform: rotate(360deg) scale(1); }
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 0.85rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Premium Customer Card */
    .customer-card {
        background: white;
        padding: 1.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border-left: 6px solid #6366f1;
        margin-bottom: 1rem;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideInLeft 0.6s ease-out;
        position: relative;
        overflow: hidden;
        z-index: 2;
    }
    
    .customer-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.03) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .customer-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
        border-left-color: #8b5cf6;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .customer-card .name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .customer-card .phone {
        font-size: 1.1rem;
        color: #4a4a6a;
        font-weight: 500;
    }
    
    .customer-card .info {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    /* Premium Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        animation: pulseGlow 2s infinite;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
    }
    
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(99, 102, 241, 0.6); }
    }
    
    /* Premium Button with 3D effect */
    .stButton button {
        width: 100% !important;
        min-height: 44px !important;
        height: 44px !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0 0.8rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: buttonGradient 3s ease-in-out infinite !important;
        letter-spacing: 0.3px !important;
        text-transform: none !important;
    }
    
    @keyframes buttonGradient {
        0%, 100% { background-position: 0% 50% !important; }
        50% { background-position: 100% 50% !important; }
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 10px 35px rgba(99, 102, 241, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(0px) scale(0.97) !important;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Premium Sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.1) !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.05) !important;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid rgba(99, 102, 241, 0.1);
        margin-bottom: 1.5rem;
        animation: fadeIn 1s ease-out;
    }
    
    .sidebar-header .logo-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .sidebar-header h3 {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sidebar-header p {
        color: #888;
        font-size: 0.7rem;
        margin: 0.2rem 0 0 0;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Premium ADB Status */
    .adb-status {
        padding: 0.6rem;
        border-radius: 14px;
        text-align: center;
        font-weight: 600;
        font-size: 0.8rem;
        animation: glowPulse 2s ease-in-out infinite;
        transition: all 0.3s ease;
    }
    
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 10px rgba(0,0,0,0.05); }
        50% { box-shadow: 0 0 30px rgba(99, 102, 241, 0.15); }
    }
    
    .adb-connected {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 2px solid #28a745;
    }
    
    .adb-disconnected {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 2px solid #dc3545;
    }
    
    /* Premium Metric Cards */
    .metric-box {
        background: white;
        padding: 0.8rem;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }
    
    .metric-box:hover::before {
        transform: scaleX(1);
    }
    
    .metric-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.12);
    }
    
    .metric-box .value {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-box .label {
        font-size: 0.7rem;
        color: #888;
        margin-top: 0.2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Premium Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899) !important;
        border-radius: 20px !important;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stProgress > div {
        background: rgba(99, 102, 241, 0.08) !important;
        border-radius: 20px !important;
        height: 10px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    
    /* Premium Input Fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        font-size: 0.85rem !important;
        border-radius: 14px !important;
        border: 2px solid rgba(99, 102, 241, 0.1) !important;
        min-height: 44px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.08) !important;
        transform: scale(1.01);
    }
    
    .stTextInput input:hover, .stSelectbox select:hover, .stTextArea textarea:hover {
        border-color: #8b5cf6 !important;
    }
    
    /* Premium Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #888;
        font-size: 0.75rem;
        border-top: 2px solid rgba(99, 102, 241, 0.05);
        margin-top: 1.5rem;
        animation: fadeIn 1.5s ease-out;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .footer span {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Premium Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(99, 102, 241, 0.05);
        border-radius: 20px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #a855f7, #ec4899);
    }
    
    /* Premium Expander */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        background: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        padding: 0.8rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.08) !important;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.8rem 1rem;
        }
        .main-header h1 {
            font-size: 1.2rem;
        }
        .customer-card {
            padding: 1rem 1.2rem;
        }
        .customer-card .name {
            font-size: 1.1rem;
        }
    }
    
    /* Loading shimmer effect */
    .shimmer-loading {
        animation: shimmerLoading 2s infinite;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        border-radius: 10px;
    }
    
    @keyframes shimmerLoading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
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

def save_customer(name, phone, status, notes, followup_date=None):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    now = datetime.now()
    c.execute("""
        INSERT INTO customers (name, phone, status, notes, call_date, call_time, followup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, status, notes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), followup_date))
    conn.commit()
    conn.close()

def update_customer_status(customer_id, status, notes, followup_date=None):
    conn = sqlite3.connect('crm_data.db')
    c = conn.cursor()
    now = datetime.now()
    
    c.execute("SELECT status FROM customers WHERE id=?", (customer_id,))
    current = c.fetchone()
    
    if current and current[0] == status:
        conn.close()
        return True
    
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
            return False, "Please enter a valid phone number!"
        
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

# ==================== VISUALIZATION FUNCTIONS ====================
def create_premium_charts():
    customers = get_all_customers()
    
    if not customers:
        return None, None, None
    
    # Status distribution with premium colors
    status_counts = {}
    for c in customers:
        status = c[3] if c[3] else "Pending"
        status_counts[status] = status_counts.get(status, 0) + 1
    
    premium_colors = ['#6366f1', '#8b5cf6', '#a855f7', '#ec4899', '#f43f5e', '#f59e0b', '#10b981']
    
    # Donut Chart with animation
    fig_donut = go.Figure(data=[go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        hole=0.5,
        marker=dict(
            colors=premium_colors[:len(status_counts)],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hoverinfo='label+value+percent',
        pull=[0.02] * len(status_counts),
        rotation=90
    )])
    
    fig_donut.update_layout(
        title=dict(
            text="<b>📊 Status Distribution</b>",
            font=dict(size=16, color='#1a1a2e', family='Inter', weight=700)
        ),
        showlegend=False,
        height=320,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(
            text=f"Total: {len(customers)}",
            showarrow=False,
            font=dict(size=14, color='#1a1a2e', weight=700)
        )]
    )
    
    # Daily call trend with premium styling
    today = datetime.now().date()
    dates = []
    calls = []
    
    for i in range(7, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        count = len([c for c in customers if c[5] == date_str])
        dates.append(date.strftime("%d %b"))
        calls.append(count)
    
    fig_bar = go.Figure(data=[go.Bar(
        x=dates,
        y=calls,
        marker=dict(
            color=['#6366f1', '#8b5cf6', '#a855f7', '#ec4899', '#f43f5e', '#f59e0b', '#10b981', '#06b6d4'],
            line=dict(color='white', width=1)
        ),
        text=calls,
        textposition='outside',
        textfont=dict(size=11, weight=700),
        hovertemplate='<b>%{x}</b><br>Calls: <b>%{y}</b><extra></extra>'
    )])
    
    fig_bar.update_layout(
        title=dict(
            text="<b>📈 Daily Call Activity</b>",
            font=dict(size=16, color='#1a1a2e', family='Inter', weight=700)
        ),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title="Number of Calls",
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            tickfont=dict(size=11)
        ),
        height=320,
        margin=dict(t=50, b=30, l=40, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.3,
        bargroupgap=0.1
    )
    
    # Performance metrics gauge
    total = len(customers)
    completed = len([c for c in customers if c[3] == "Completed"])
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    fig_gauge = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=completion_rate,
        number=dict(
            suffix="%",
            font=dict(size=24, color='#1a1a2e', weight=700)
        ),
        delta=dict(
            reference=50,
            increasing=dict(color="#10b981"),
            decreasing=dict(color="#ef4444")
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=1,
                tickcolor="darkgray",
                tickfont=dict(size=10)
            ),
            bar=dict(
                color="rgba(99, 102, 241, 1)",
                thickness=0.3
            ),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=2,
            bordercolor="rgba(0,0,0,0.1)",
            steps=[
                {'range': [0, 30], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [30, 70], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ],
            threshold=dict(
                line=dict(color="red", width=4),
                thickness=0.75,
                value=90
            )
        )
    )])
    
    fig_gauge.update_layout(
        title=dict(
            text="<b>🎯 Completion Rate</b>",
            font=dict(size=16, color='#1a1a2e', family='Inter', weight=700)
        ),
        height=320,
        margin=dict(t=50, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig_donut, fig_bar, fig_gauge

# ==================== REPORT FUNCTIONS ====================
def generate_report_data():
    conn = sqlite3.connect('crm_data.db')
    df = pd.read_sql_query("SELECT * FROM customers WHERE status IS NOT NULL AND status != '' ORDER BY id", conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()
    
    df.insert(0, 'Sr No', range(1, len(df) + 1))
    report_df = df[['Sr No', 'name', 'phone', 'status', 'call_date', 'call_time']]
    report_df.columns = ['Sr No', 'Name', 'Phone', 'Status', 'Date', 'Time']
    
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
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0; text-align: center;">{row['Sr No']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0; font-weight: 500;">{row['Name']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{row['Phone']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><span style="background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 2px 12px; border-radius: 20px; font-size: 12px;">{row['Status']}</span></td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0; text-align: center;">{row['Date'] if row['Date'] else '-'}</td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0; text-align: center;">{row['Time'] if row['Time'] else '-'}</td>
            </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Call Report</title>
        <style>
            body {{ font-family: 'Inter', Arial, sans-serif; margin: 20px; background: linear-gradient(135deg, #f6f9fc 0%, #e8f0fe 100%); }}
            .container {{ max-width: 1100px; margin: 0 auto; background: white; padding: 35px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.08); }}
            .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); color: white; padding: 25px; border-radius: 16px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 26px; font-weight: 800; }}
            .header p {{ margin: 8px 0 0 0; opacity: 0.9; font-size: 14px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 25px; font-size: 14px; }}
            th {{ background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 14px; text-align: left; font-weight: 600; }}
            td {{ padding: 12px; border-bottom: 1px solid #f0f0f0; }}
            tr:hover {{ background: rgba(99, 102, 241, 0.04); }}
            .footer {{ text-align: center; margin-top: 25px; color: #888; font-size: 12px; font-weight: 500; }}
            .count {{ background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 4px 16px; border-radius: 30px; font-weight: 700; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Call Report</h1>
                <p>Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')} | Total: <span class="count">{len(df)}</span></p>
            </div>
            <table>
                <tr>
                    <th>Sr No</th>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Time</th>
                </tr>
                {rows}
            </table>
            <div class="footer">⚡ Enterprise Calling CRM Pro</div>
        </div>
    </body>
    </html>
    """
    
    return html

# ==================== MAIN APP ====================
def main():
    init_db()
    adb_connected, device_id = check_adb()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <span class="logo-icon">🚀</span>
            <h3>CRM Pro</h3>
            <p>Enterprise Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        if adb_connected:
            st.markdown(f"""
            <div class="adb-status adb-connected">
                ✅ Device Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="adb-status adb-disconnected">
                ⚡ Device Disconnected
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu = st.radio(
            "Navigation",
            ["📞 Call", "📊 History", "📂 Import", "📋 Reports"],
            index=0
        )
        
        st.markdown("---")
        
        if menu == "📂 Import":
            st.markdown("#### 📤 Import Excel")
            uploaded_file = st.file_uploader("Choose file", type=["xlsx", "xls"], label_visibility="collapsed")
            
            if uploaded_file:
                df = pd.read_excel(uploaded_file)
                st.caption(f"📊 {len(df)} records found")
                
                cols = df.columns.tolist()
                name_col = st.selectbox("Name Column", cols, index=0)
                phone_col = st.selectbox("Phone Column", cols, index=1 if len(cols) > 1 else 0)
                
                if st.button("🚀 Import Now", use_container_width=True):
                    imported = import_from_excel(df, name_col, phone_col)
                    st.success(f"✅ {imported} customers imported!")
                    st.balloons()
                    st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️ Clear All Data", use_container_width=True):
            clear_database()
            st.success("✅ Data cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Live Stats in Sidebar
        all_customers = get_all_customers()
        st.markdown("#### 📊 Live Stats")
        st.markdown(f"**Total:** {len(all_customers)}")
        if all_customers:
            completed = len([c for c in all_customers if c[3] == "Completed"])
            st.markdown(f"**Completed:** {completed}")
            pending = len([c for c in all_customers if not c[3] or c[3] == ""])
            st.markdown(f"**Pending:** {pending}")
        
        st.markdown("---")
        st.caption("⚡ v3.0 Enterprise")
    
    # ===== CALL SCREEN =====
    if menu == "📞 Call":
        # Premium Header
        st.markdown("""
        <div class="main-header">
            <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 1;">
                <div>
                    <h1>🚀 Enterprise Calling CRM</h1>
                    <div class="subtitle">Professional Telecalling Solution</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem; font-weight: 500;">
                        <span id="live-clock"></span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        customers = get_all_customers()
        
        if not customers:
            st.warning("No customers found. Please import data first.")
            return
        
        # ===== SEARCH & FILTER =====
        with st.container():
            st.markdown("""
            <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 1.2rem 1.5rem; border-radius: 20px; margin-bottom: 1.5rem; border: 1px solid rgba(99,102,241,0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.04);">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1.5, 1.5])
            
            with col1:
                search_term = st.text_input("🔍 Search", placeholder="Search by name or phone...", key="search")
            
            with col2:
                status_filter = st.selectbox(
                    "📊 Filter",
                    ["All", "Pending", "Not Reachable", "Mobile Off", "Interested", "Call Back", "Meeting Monday", 
                     "Meeting Tuesday", "Meeting Wednesday", "Meeting Thursday", "Meeting Friday"],
                    key="filter"
                )
            
            with col3:
                sort_by = st.selectbox(
                    "📌 Sort",
                    ["ID", "Name", "Status", "Date"],
                    key="sort"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
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
        
        # Premium Progress
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            progress_value = (st.session_state.index + 1) / len(filtered_customers)
            st.progress(progress_value)
            st.markdown(f"""
            <div style="text-align: center; font-weight: 600; color: #1a1a2e; font-size: 0.9rem;">
                📌 Customer {st.session_state.index + 1} of {len(filtered_customers)}
            </div>
            """, unsafe_allow_html=True)
        
        # ===== MAIN LAYOUT =====
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            # Premium Customer Card
            st.markdown(f"""
            <div class="customer-card">
                <div class="name">👤 {name}</div>
                <div class="phone">📞 {phone}</div>
                <div class="info">
                    Status: <span class="status-badge">{status if status else 'Pending'}</span>
                    {f" | 📅 {call_date} {call_time}" if call_date else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Phone Controls
            st.markdown("#### 📱 Phone Controls")
            
            if f"phone_{cust_id}" not in st.session_state:
                st.session_state[f"phone_{cust_id}"] = phone
            
            col1, col2, col3, col4 = st.columns([2, 0.8, 0.8, 0.8])
            
            with col1:
                custom_phone = st.text_input(
                    "",
                    value=st.session_state[f"phone_{cust_id}"],
                    key=f"phone_input_{cust_id}",
                    placeholder="Phone number...",
                    label_visibility="collapsed"
                )
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{cust_id}", use_container_width=True):
                    if custom_phone and custom_phone != st.session_state[f"phone_{cust_id}"]:
                        try:
                            conn = sqlite3.connect('crm_data.db')
                            c = conn.cursor()
                            c.execute("UPDATE customers SET phone=? WHERE id=?", (custom_phone.strip(), cust_id))
                            conn.commit()
                            conn.close()
                            st.session_state[f"phone_{cust_id}"] = custom_phone.strip()
                            st.success("✅ Phone updated!")
                            time.sleep(0.5)
                            st.rerun()
                        except:
                            st.error("❌ Error updating phone")
            
            with col3:
                if st.button("📞 Call", key=f"call_{cust_id}", use_container_width=True):
                    call_phone = custom_phone if custom_phone else phone
                    if adb_connected:
                        success, msg = call_via_adb(call_phone)
                        if success:
                            st.success(f"✅ {msg}")
                            st.balloons()
                            update_customer_status(cust_id, status if status else "Pending", notes if notes else "")
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
            
            # Status Buttons
            st.markdown("#### 📌 Quick Status")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✅ Interested", key=f"int_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Interested", notes if notes else "")
                    st.success("✅ Status: Interested")
                    st.balloons()
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            
            with col2:
                if st.button("📞 Call Back", key=f"cb_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Call Back", notes if notes else "")
                    st.success("✅ Status: Call Back")
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            
            with col3:
                if st.button("📵 Not Reachable", key=f"nr_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Not Reachable", notes if notes else "")
                    st.success("✅ Status: Not Reachable")
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            
            with col4:
                if st.button("📱 Mobile Off", key=f"mo_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, "Mobile Off", notes if notes else "")
                    st.success("✅ Status: Mobile Off")
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
                    st.rerun()
            
            # Weekdays
            st.markdown("#### 📅 Weekday Meetings")
            col1, col2, col3, col4, col5 = st.columns(5)
            days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
            for i, day in enumerate(days):
                with [col1, col2, col3, col4, col5][i]:
                    if st.button(f"📅 {day}", key=f"day_{day}_{cust_id}", use_container_width=True):
                        update_customer_status(cust_id, f"Meeting {day}", notes if notes else "")
                        st.success(f"✅ Meeting {day}")
                        if st.session_state.index < len(filtered_customers) - 1:
                            st.session_state.index += 1
                        st.rerun()
            
            # Custom Status
            st.markdown("#### ✏️ Custom Status")
            col1, col2 = st.columns([3, 1])
            with col1:
                custom_status = st.text_input(
                    "",
                    placeholder="Type custom status...",
                    key=f"custom_{cust_id}",
                    label_visibility="collapsed"
                )
            with col2:
                if st.button("Set Status", key=f"set_custom_{cust_id}", use_container_width=True):
                    if custom_status and custom_status.strip():
                        update_customer_status(cust_id, custom_status.strip(), notes if notes else "")
                        st.success(f"✅ Status: {custom_status.strip()}")
                        st.balloons()
                        if st.session_state.index < len(filtered_customers) - 1:
                            st.session_state.index += 1
                        st.rerun()
            
            # Notes
            st.markdown("#### 📝 Notes")
            notes_text = st.text_area(
                "",
                value=notes if notes else "",
                height=60,
                key=f"notes_{cust_id}",
                placeholder="Add notes here..."
            )
            
            if st.button("💾 Save Notes", key=f"save_notes_{cust_id}", use_container_width=True):
                update_customer_status(cust_id, status if status else "Pending", notes_text)
                st.success("✅ Notes saved!")
                st.rerun()
            
            # Follow-up
            st.markdown("#### 📅 Follow-up")
            col1, col2 = st.columns([3, 1])
            with col1:
                followup_date = st.date_input(
                    "",
                    value=datetime.now().date(),
                    min_value=datetime.now().date(),
                    key=f"followup_{cust_id}",
                    label_visibility="collapsed"
                )
            with col2:
                if st.button("📌 Set", key=f"set_followup_{cust_id}", use_container_width=True):
                    update_customer_status(cust_id, status if status else "Call Back", notes if notes else "", followup_date.strftime("%Y-%m-%d"))
                    st.success(f"✅ Follow-up: {followup_date.strftime('%d-%m-%Y')}")
                    st.rerun()
            
            # Navigation
            st.markdown("#### 🧭 Navigation")
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
                    if st.session_state.index < len(filtered_customers) - 1:
                        st.session_state.index += 1
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
            # Premium Status Info
            st.markdown("#### 📊 Current Status")
            st.markdown(f"""
            <div style="background: white; padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(99,102,241,0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.04);">
                <p style="margin: 0.3rem 0; display: flex; justify-content: space-between;">
                    <span style="color: #666;">Status:</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{status if status else 'Pending'}</span>
                </p>
                <p style="margin: 0.3rem 0; display: flex; justify-content: space-between;">
                    <span style="color: #666;">Last Call:</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{call_date if call_date else 'N/A'}</span>
                </p>
                <p style="margin: 0.3rem 0; display: flex; justify-content: space-between;">
                    <span style="color: #666;">Time:</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{call_time if call_time else 'N/A'}</span>
                </p>
                <p style="margin: 0.3rem 0; display: flex; justify-content: space-between;">
                    <span style="color: #666;">Follow-up:</span>
                    <span style="font-weight: 600; color: #1a1a2e;">{followup_date if followup_date else 'Not set'}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Premium Statistics
            st.markdown("#### 📈 Live Statistics")
            
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
            <div class="metric-box" style="margin-top: 0.5rem;">
                <div class="value">{today_calls}</div>
                <div class="label">Today's Calls</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Follow-ups due
            today_date = datetime.now().date()
            followups_due = len([c for c in all_customers if c[7] and datetime.strptime(c[7], "%Y-%m-%d").date() <= today_date])
            st.markdown(f"""
            <div class="metric-box" style="margin-top: 0.5rem;">
                <div class="value">{followups_due}</div>
                <div class="label">Follow-ups Due</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Premium Charts
            st.markdown("---")
            st.markdown("#### 📊 Analytics Dashboard")
            
            fig_donut, fig_bar, fig_gauge = create_premium_charts()
            
            if fig_donut:
                st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
            
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            
            if fig_gauge:
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    # ===== HISTORY =====
    elif menu == "📊 History":
        st.markdown("""
        <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 1.2rem 1.5rem; border-radius: 20px; margin-bottom: 1.5rem; border: 1px solid rgba(99,102,241,0.08);">
            <h2 style="margin: 0; font-size: 1.4rem; color: #1a1a2e; font-weight: 700;">📊 Call History</h2>
        </div>
        """, unsafe_allow_html=True)
        
        customers = get_all_customers()
        
        if not customers:
            st.warning("No customers found!")
            return
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_option = st.selectbox(
                "📅 Date Range",
                ["All", "Today", "Yesterday", "Last 7 Days", "Last 30 Days", "Custom"]
            )
        
        with col2:
            if date_option == "Custom":
                custom_date = st.date_input("Select Date", value=datetime.now().date())
            else:
                custom_date = None
        
        with col3:
            status_filter = st.selectbox(
                "📊 Status",
                ["All", "Pending", "Not Reachable", "Mobile Off", "Interested", "Call Back", "Completed"]
            )
        
        # Apply filters
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
        elif date_option == "Custom" and custom_date:
            date_str = custom_date.strftime("%Y-%m-%d")
            filtered = [c for c in filtered if c[5] == date_str]
        
        if status_filter != "All":
            if status_filter == "Pending":
                filtered = [c for c in filtered if not c[3] or c[3] == ""]
            else:
                filtered = [c for c in filtered if c[3] == status_filter]
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 16px; margin-bottom: 1.5rem; border: 1px solid rgba(99,102,241,0.08); box-shadow: 0 4px 20px rgba(0,0,0,0.04);">
            <span style="font-weight: 700; font-size: 1rem; color: #1a1a2e;">Found {len(filtered)} records</span>
        </div>
        """, unsafe_allow_html=True)
        
        if filtered:
            df = pd.DataFrame(filtered, columns=["ID", "Name", "Phone", "Status", "Notes", "Date", "Time", "Follow-up"])
            df_display = df[["Name", "Phone", "Status", "Date", "Time"]]
            st.dataframe(df_display, use_container_width=True)
            
            # Export
            col1, col2 = st.columns(2)
            with col1:
                excel_file = download_excel(df_display)
                st.download_button(
                    "📥 Download Excel",
                    data=excel_file,
                    file_name=f"history_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col2:
                df_pdf = df_display.copy()
                df_pdf.insert(0, 'Sr No', range(1, len(df_pdf) + 1))
                html = create_pdf_html(df_pdf)
                b64 = base64.b64encode(html.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" target="_blank" style="display:block;text-align:center;padding:12px;background:linear-gradient(135deg, #6366f1, #a855f7);color:white;border-radius:14px;text-decoration:none;font-weight:600;box-shadow:0 4px 15px rgba(99,102,241,0.3);">📥 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    # ===== REPORTS =====
    elif menu == "📋 Reports":
        st.markdown("""
        <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 1.2rem 1.5rem; border-radius: 20px; margin-bottom: 1.5rem; border: 1px solid rgba(99,102,241,0.08);">
            <h2 style="margin: 0; font-size: 1.4rem; color: #1a1a2e; font-weight: 700;">📋 Reports</h2>
        </div>
        """, unsafe_allow_html=True)
        
        report_df = generate_report_data()
        
        if report_df.empty:
            st.info("No data available yet.")
        else:
            st.success(f"✅ Total Calls: {len(report_df)}")
            
            col1, col2 = st.columns(2)
            with col1:
                excel_file = download_excel(report_df)
                st.download_button(
                    "📥 Download Excel Report",
                    data=excel_file,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col2:
                html = create_pdf_html(report_df)
                b64 = base64.b64encode(html.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" target="_blank" style="display:block;text-align:center;padding:12px;background:linear-gradient(135deg, #6366f1, #a855f7);color:white;border-radius:14px;text-decoration:none;font-weight:600;box-shadow:0 4px 15px rgba(99,102,241,0.3);">📥 Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            with st.expander("📊 Preview Report"):
                st.dataframe(report_df, use_container_width=True)

if __name__ == "__main__":
    main()

st.markdown("""
<div class="footer">
    ⚡ <span>Enterprise Calling CRM Pro</span> | Next-Gen Telecalling Solution
</div>
""", unsafe_allow_html=True)
