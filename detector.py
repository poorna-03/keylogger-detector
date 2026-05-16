import psutil
from plyer import notification
from datetime import datetime

# suspicious keywords
suspicious_keywords = [
    "keylog",
    "hook",
    "spy",
    "logger",
    "monitor"
]

print("Scanning system processes...\n")

detected = False

# open log file
log_file = open("logs.txt", "a")

# current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for process in psutil.process_iter(['pid', 'name']):

    try:
        process_name = process.info['name']

        if process_name:
            process_name = process_name.lower()

            for keyword in suspicious_keywords:

                if keyword in process_name:

                    detected = True

                    alert_message = (
                        f"Detected: {process_name} | "
                        f"PID: {process.info['pid']} | "
                        f"Time: {current_time}"
                    )

                    print("[ALERT] Suspicious process found!")
                    print(alert_message)
                    print()

                    # desktop notification
                    notification.notify(
                        title="Keylogger Alert!",
                        message=f"Suspicious process detected: {process_name}",
                        timeout=5
                    )

                    # write to log file
                    log_file.write(alert_message + "\n")

    except:
        pass

if not detected:
    print("No suspicious processes detected.")
    log_file.write(f"No suspicious processes detected | Time: {current_time}\n")

# close log file
log_file.close()

print("Scan completed.")
