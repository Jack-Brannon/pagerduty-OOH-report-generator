import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from src.calendar_parser import parse_calendar_url, get_events
from src.shift_classifier import classify_shifts
from src.report_generator import generate_report
from config import DEFAULT_CALENDARS, DATE_FORMAT, DEFAULT_END_DATE, DEFAULT_START_DATE

# Limit selectable dates to the last 30 days
min_date = datetime.today() - timedelta(days=30)
max_date = datetime.today()

def run_parser():
    calendars = calendar_urls.get("1.0", tk.END).strip().split("\n")
    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()
    
    if not calendars or not start_date_str or not end_date_str:
        messagebox.showerror("Input Error", "Please provide all required inputs.")
        return
    
    try:
        start_date = datetime.strptime(start_date_str, DATE_FORMAT).date()
        end_date = datetime.strptime(end_date_str, DATE_FORMAT).date()
    except ValueError:
        messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
        return
    
    all_events = []
    for calendar_url in calendars:
        calendar = parse_calendar_url(calendar_url)
        events = get_events(calendar, start_date, end_date)
        all_events.extend(events)
    
    all_events.sort(key=lambda x: x['start'])
    classified_shifts = classify_shifts(all_events)
    
    generate_report(classified_shifts)
    messagebox.showinfo("Success", "Report generated successfully as shift_report.csv")
    download_button.config(state=tk.NORMAL)

def download_report():
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        with open("shift_report.csv", "rb") as src_file:
            with open(save_path, "wb") as dest_file:
                dest_file.write(src_file.read())
        messagebox.showinfo("Download", f"Report saved as:\n{save_path}")

# GUI Setup
root = tk.Tk()
root.title("Shift Calendar Parser")

# Labels and Inputs
tk.Label(root, text="Enter Calendar URLs (one per line):").pack()
calendar_urls = tk.Text(root, height=5, width=50)
calendar_urls.pack()
calendar_urls.insert(tk.END, "\n".join(DEFAULT_CALENDARS))

tk.Label(root, text="Start Date:").pack()
start_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd", mindate=min_date, maxdate=max_date)
start_date_entry.pack()

tk.Label(root, text="End Date:").pack()
end_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd", mindate=min_date, maxdate=max_date)
end_date_entry.pack()

# Run Button
tk.Button(root, text="Run", command=run_parser).pack()

# Download Button (Initially Disabled)
download_button = tk.Button(root, text="Download Report", command=download_report, state=tk.DISABLED)
download_button.pack()

root.mainloop()
