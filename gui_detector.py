import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox
import psutil
from plyer import notification
from datetime import datetime
import platform
from time import strftime

# =========================================
# Suspicious Keywords
# =========================================

suspicious_keywords = [
    "keylog",
    "hook",
    "spy",
    "logger",
    "monitor",
    "capture",
    "record"
]

# =========================================
# Global Stats
# =========================================

total_scans = 0
threats_detected = 0

# =========================================
# Clock Function
# =========================================

def update_clock():

    current_time = strftime("%H:%M:%S")

    clock_label.config(text=current_time)

    clock_label.after(1000, update_clock)

# =========================================
# System Info
# =========================================

def update_system_info():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    os_name = platform.system()

    system_info_label.config(
        text=f"OS: {os_name}   |   CPU: {cpu}%   |   RAM: {ram}%"
    )

    window.after(3000, update_system_info)

# =========================================
# Threat Level
# =========================================

def get_threat_level(process_name):

    if "keylog" in process_name:
        return "HIGH"

    elif "spy" in process_name:
        return "MEDIUM"

    else:
        return "LOW"

# =========================================
# Scan Function
# =========================================

def scan_system():

    global total_scans
    global threats_detected

    total_scans += 1

    progress_bar["value"] = 0

    output_box.insert(tk.END, "\n[ SYSTEM SCAN STARTED ]\n\n")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    detected = False

    log_file = open("logs.txt", "a")

    process_list = list(psutil.process_iter(['pid', 'name']))

    total_processes = len(process_list)

    for index, process in enumerate(process_list):

        try:

            process_name = process.info['name']

            if process_name:

                process_name = process_name.lower()

                for keyword in suspicious_keywords:

                    if keyword in process_name:

                        detected = True

                        threats_detected += 1

                        threat_level = get_threat_level(process_name)

                        alert_message = (
                            f"[ THREAT DETECTED ]\n"
                            f"Process : {process_name}\n"
                            f"PID     : {process.info['pid']}\n"
                            f"Threat  : {threat_level}\n"
                            f"Time    : {current_time}\n"
                            f"----------------------------------\n"
                        )

                        output_box.insert(tk.END, alert_message)

                        notification.notify(
                            title="⚠ Threat Detected",
                            message=f"{process_name} detected",
                            timeout=5
                        )

                        log_file.write(alert_message + "\n")

        except:
            pass

        progress = ((index + 1) / total_processes) * 100

        progress_bar["value"] = progress

        window.update_idletasks()

    if not detected:

        safe_message = (
            f"[ SAFE ] No suspicious processes found\n"
            f"Time : {current_time}\n"
            f"----------------------------------\n"
        )

        output_box.insert(tk.END, safe_message)

        log_file.write(safe_message + "\n")

    log_file.close()

    stats_label.config(
        text=f"Total Scans: {total_scans}   |   Threats Detected: {threats_detected}"
    )

# =========================================
# Clear Screen
# =========================================

def clear_output():

    output_box.delete(1.0, tk.END)

# =========================================
# View Logs
# =========================================

def view_logs():

    try:

        with open("logs.txt", "r") as file:

            logs = file.read()

        output_box.delete(1.0, tk.END)

        output_box.insert(tk.END, logs)

    except:

        messagebox.showerror("Error", "No logs found")

# =========================================
# Auto Scan
# =========================================

auto_scan_running = False

def toggle_auto_scan():

    global auto_scan_running

    if auto_scan_running == False:

        auto_scan_running = True

        auto_scan_button.config(text="STOP AUTO SCAN")

        auto_scan()

    else:

        auto_scan_running = False

        auto_scan_button.config(text="START AUTO SCAN")

def auto_scan():

    if auto_scan_running:

        scan_system()

        window.after(10000, auto_scan)

# =========================================
# Exit Application
# =========================================

def exit_app():

    window.destroy()

# =========================================
# Main Window
# =========================================

window = tk.Tk()

window.title("Advanced Cybersecurity Dashboard")

window.geometry("1100x750")

window.configure(bg="black")

# =========================================
# Title
# =========================================

title_label = tk.Label(
    window,
    text="ADVANCED KEYLOGGER DETECTION TOOL",
    font=("Arial", 24, "bold"),
    fg="red",
    bg="black"
)

title_label.pack(pady=10)

# =========================================
# Clock
# =========================================

clock_label = tk.Label(
    window,
    font=("Arial", 16, "bold"),
    fg="white",
    bg="black"
)

clock_label.pack()

update_clock()

# =========================================
# System Info
# =========================================

system_info_label = tk.Label(
    window,
    font=("Arial", 12),
    fg="white",
    bg="black"
)

system_info_label.pack(pady=5)

update_system_info()

# =========================================
# Stats Label
# =========================================

stats_label = tk.Label(
    window,
    text="Total Scans: 0   |   Threats Detected: 0",
    font=("Arial", 12, "bold"),
    fg="red",
    bg="black"
)

stats_label.pack(pady=10)

# =========================================
# Button Frame
# =========================================

button_frame = tk.Frame(window, bg="black")

button_frame.pack(pady=10)

# =========================================
# Buttons
# =========================================

scan_button = tk.Button(
    button_frame,
    text="START SCAN",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=18,
    height=2,
    bd=4,
    command=scan_system
)

scan_button.grid(row=0, column=0, padx=10)

auto_scan_button = tk.Button(
    button_frame,
    text="START AUTO SCAN",
    font=("Arial", 12, "bold"),
    bg="#222222",
    fg="red",
    width=18,
    height=2,
    bd=4,
    command=toggle_auto_scan
)

auto_scan_button.grid(row=0, column=1, padx=10)

view_logs_button = tk.Button(
    button_frame,
    text="VIEW LOGS",
    font=("Arial", 12, "bold"),
    bg="#222222",
    fg="red",
    width=18,
    height=2,
    bd=4,
    command=view_logs
)

view_logs_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(
    button_frame,
    text="CLEAR SCREEN",
    font=("Arial", 12, "bold"),
    bg="#222222",
    fg="red",
    width=18,
    height=2,
    bd=4,
    command=clear_output
)

clear_button.grid(row=0, column=3, padx=10)

exit_button = tk.Button(
    button_frame,
    text="EXIT",
    font=("Arial", 12, "bold"),
    bg="darkred",
    fg="white",
    width=18,
    height=2,
    bd=4,
    command=exit_app
)

exit_button.grid(row=0, column=4, padx=10)

# =========================================
# Progress Bar
# =========================================

progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    length=900,
    mode="determinate"
)

progress_bar.pack(pady=15)

# =========================================
# Output Box
# =========================================

output_box = scrolledtext.ScrolledText(
    window,
    width=130,
    height=28,
    font=("Consolas", 10),
    bg="#111111",
    fg="red",
    insertbackground="white",
    bd=5
)

output_box.pack(pady=10)

# =========================================
# Footer
# =========================================

footer = tk.Label(
    window,
    text="Real-Time Malware & Threat Monitoring Dashboard",
    font=("Arial", 10),
    fg="white",
    bg="black"
)

footer.pack(side="bottom", pady=10)

# =========================================
# Run Window
# =========================================

window.mainloop()
