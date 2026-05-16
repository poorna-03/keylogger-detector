import streamlit as st
import psutil
import pandas as pd
from datetime import datetime
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: white;
    }

    .welcome-box {
        background-color: black;
        border: 2px solid red;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        margin-top: 100px;
        box-shadow: 0px 0px 25px red;
    }

    .welcome-title {
        color: red;
        font-size: 55px;
        font-weight: bold;
        animation: blink 1s infinite;
    }

    .welcome-sub {
        color: white;
        font-size: 22px;
        margin-top: 20px;
    }

    .dashboard-title {
        color: red;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }

    .safe {
        color: lime;
        font-size: 20px;
        font-weight: bold;
    }

    .danger {
        color: red;
        font-size: 20px;
        font-weight: bold;
    }

    @keyframes blink {
        50% {
            opacity: 0.4;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# WELCOME SCREEN
# ==========================================

if "welcome_done" not in st.session_state:

    st.session_state.welcome_done = False

if not st.session_state.welcome_done:

    welcome_placeholder = st.empty()

    with welcome_placeholder.container():

        st.markdown(
            """
            <div class='welcome-box'>
                <div class='welcome-title'>WELCOME</div>
                <div class='welcome-sub'>
                    Advanced Cybersecurity Monitoring System<br><br>
                    Initializing Threat Detection Engine...
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    time.sleep(3)

    st.session_state.welcome_done = True

    st.rerun()

# ==========================================
# DASHBOARD TITLE
# ==========================================

st.markdown(
    "<div class='dashboard-title'>ADVANCED KEYLOGGER DETECTION TOOL</div>",
    unsafe_allow_html=True
)

st.write("### Real-Time Cybersecurity Threat Dashboard")

# ==========================================
# SUSPICIOUS KEYWORDS
# ==========================================

suspicious_keywords = [
    "keylog",
    "spy",
    "hook",
    "logger",
    "monitor",
    "capture",
    "record"
]

# ==========================================
# SYSTEM INFORMATION
# ==========================================

cpu = psutil.cpu_percent()
ram = psutil.virtual_memory().percent

col1, col2 = st.columns(2)

with col1:
    st.metric("CPU Usage", f"{cpu}%")

with col2:
    st.metric("RAM Usage", f"{ram}%")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛡️ Security Panel")

st.sidebar.info(
    "This dashboard scans suspicious processes and displays possible threats."
)

scan_option = st.sidebar.selectbox(
    "Choose Scan Type",
    ["Quick Scan", "Full Scan"]
)

# ==========================================
# SCAN BUTTON
# ==========================================

if st.button("🚨 START SYSTEM SCAN"):

    progress_bar = st.progress(0)

    detected_processes = []

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    process_list = list(psutil.process_iter(['pid', 'name']))

    total_processes = len(process_list)

    for index, process in enumerate(process_list):

        try:

            process_name = process.info['name']

            if process_name:

                process_name = process_name.lower()

                for keyword in suspicious_keywords:

                    if keyword in process_name:

                        detected_processes.append({
                            "Process": process_name,
                            "PID": process.info['pid'],
                            "Threat Level": "HIGH",
                            "Detected Time": current_time
                        })

        except:
            pass

        progress = int(((index + 1) / total_processes) * 100)

        progress_bar.progress(progress)

    # ==========================================
    # RESULTS
    # ==========================================

    st.write("---")

    if detected_processes:

        st.markdown(
            "<p class='danger'>⚠ Suspicious Processes Detected</p>",
            unsafe_allow_html=True
        )

        df = pd.DataFrame(detected_processes)

        st.dataframe(df, use_container_width=True)

    else:

        st.markdown(
            "<p class='safe'>✅ No Suspicious Processes Found</p>",
            unsafe_allow_html=True
        )

# ==========================================
# FOOTER
# ==========================================

st.write("---")

st.write("### 🔐 Educational Cybersecurity Monitoring Dashboard")
