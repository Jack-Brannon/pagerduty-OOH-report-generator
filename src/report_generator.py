import csv
from datetime import datetime
from collections import defaultdict
from config import PEOPLE

def group_user_names(summary):
    """"Group the user name checking against a list of names"""
    for name in PEOPLE:
        if name in summary:
            return name
    return None

def generate_report(classified_shifts):
    """
    Generate a CSV report summarizing shifts by user.
    """
    report_file = "shift_report.csv"

    shifts_by_user = defaultdict(list)
    for shift in classified_shifts:
        user_name = group_user_names(shift['user'])
        if not user_name:
            continue
        shifts_by_user[user_name].append(shift)

    with open(report_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Date", "Weekday", "Weekend", "Bank Holiday"])  # Header row

        for user, shifts in shifts_by_user.items():
            # Create a dictionary to count shift categories per date for each user
            date_counts = defaultdict(lambda: {"Weekday": 0, "Weekend": 0, "Bank Holiday": 0})
            for shift in shifts:
                date = shift["start"].date()
                category = shift["category"]
                if "Weekend" in category:
                    date_counts[date][category] += 0.5
                else:
                    date_counts[date][category] += 1

            # Write rows for each date and category count for the current user
            for date, counts in date_counts.items():
                writer.writerow([
                    user,
                    date.strftime("%Y-%m-%d"),
                    counts["Weekday"],
                    counts["Weekend"],
                    counts["Bank Holiday"]
                ])

    print(f"Report generated: {report_file}")
