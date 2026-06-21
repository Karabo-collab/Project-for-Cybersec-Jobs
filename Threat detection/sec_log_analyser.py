"""
Security Log Analyzer

Author: Karabo Matlou

Description:
This program analyzes authentication logs to identify failed login attempts,
detect suspicious activity based on configurable thresholds, and generate
a security report summarizing potential brute-force attacks by both IP
address and username.
"""


def read_logs(filename):
    """
    Reads log entries from a text file.

    Parameters:
        filename (str): The path to the log file.

    Returns:
        list:
            A list containing each line from the log file.
            Returns an empty list if the file cannot be opened.
    """
    try:
        with open(filename, "r") as file:
            return file.readlines()

    except FileNotFoundError:
        print(f"Error: '{filename}' was not found.")
        return []

    except Exception as error:
        print(f"Unexpected error: {error}")
        return []


def count_failed_attempts(logs):
    """
    Counts failed login attempts by IP address and username.

    The function processes every log entry, extracts the username and
    IP address from failed login records, and stores the number of
    failures for each in separate dictionaries.

    Parameters:
        logs (list): A list containing log entries.

    Returns:
        tuple:
            failed_ips (dict): Maps IP addresses to failed login counts.
            failed_users (dict): Maps usernames to failed login counts.
    """

    # Dictionary storing failed login counts for each IP address
    failed_ips = {}

    # Dictionary storing failed login counts for each username
    failed_users = {}

    # Process every log entry
    for log in logs:

        # Only analyze failed login attempts
        if "status=FAILED" in log:

            # Remove whitespace/newlines and split into fields
            parts = log.strip().split(",")

            # -------------------------
            # Extract username
            # -------------------------
            username = None

            for part in parts:
                if part.startswith("user="):
                    username = part.split("=")[1]

            # Count failed attempts per username
            if username:
                if username in failed_users:
                    failed_users[username] += 1
                else:
                    failed_users[username] = 1

            # -------------------------
            # Extract IP address
            # -------------------------
            ip = None

            for part in parts:
                if part.startswith("ip="):
                    ip = part.split("=")[1]
                    break

            # Skip malformed log entries with no IP
            if ip is None:
                continue

            # Count failed attempts per IP
            if ip in failed_ips:
                failed_ips[ip] += 1
            else:
                failed_ips[ip] = 1

    return failed_ips, failed_users


def detect_suspicious_activity(items, threshold=3):
    """
    Identifies entries that exceed a specified threshold.

    This function can be reused for both IP addresses and usernames.

    Parameters:
        items (dict):
            Dictionary containing an entity (IP or username)
            mapped to its failed login count.

        threshold (int):
            Minimum number of failed attempts required before
            the entity is flagged as suspicious.
            Default = 3.

    Returns:
        dict:
            Dictionary containing only suspicious entities.
    """

    suspicious = {}

    for key, count in items.items():
        if count >= threshold:
            suspicious[key] = count

    return suspicious


def generate_report(
    logs,
    failed_ips,
    failed_users,
    suspicious_ips,
    suspicious_users,
):
    """
    Generates a human-readable security report.

    The report contains:
    - Overall statistics
    - Suspicious IP addresses
    - Failed login counts by username
    - Suspicious usernames

    Parameters:
        logs (list)
        failed_ips (dict)
        failed_users (dict)
        suspicious_ips (dict)
        suspicious_users (dict)

    Returns:
        None
    """

    with open("report.txt", "w") as report:

        report.write("SECURITY LOG ANALYSIS REPORT\n")
        report.write("=" * 50 + "\n\n")

        # -------------------------
        # Overall Summary
        # -------------------------
        report.write("SUMMARY\n")
        report.write("-" * 50 + "\n")

        report.write(f"Total log entries        : {len(logs)}\n")
        report.write(f"Total failed logins      : {sum(failed_ips.values())}\n")
        report.write(f"Unique failed IPs        : {len(failed_ips)}\n")
        report.write(f"Unique targeted users    : {len(failed_users)}\n\n")

        # -------------------------
        # Suspicious IP Addresses
        # -------------------------
        report.write("SUSPICIOUS IP ADDRESSES\n")
        report.write("-" * 50 + "\n")

        if suspicious_ips:
            for ip, count in suspicious_ips.items():
                report.write(
                    f"[HIGH RISK] {ip} -> {count} failed attempts\n"
                )
        else:
            report.write("No suspicious IP addresses detected.\n")

        report.write("\n")

        # -------------------------
        # Failed Login Attempts by Username
        # -------------------------
        report.write("FAILED LOGIN ATTEMPTS BY USERNAME\n")
        report.write("-" * 50 + "\n")

        for user, count in failed_users.items():
            report.write(
                f"{user} -> {count} failed attempt(s)\n"
            )

        report.write("\n")

        # -------------------------
        # Suspicious Usernames
        # -------------------------
        report.write("SUSPICIOUS USERS\n")
        report.write("-" * 50 + "\n")

        if suspicious_users:
            for user, count in suspicious_users.items():
                report.write(
                    f"[HIGH RISK] {user} -> {count} failed attempts\n"
                )
        else:
            report.write("No suspicious users detected.")


# ==========================================================
#                     MAIN PROGRAM
# ==========================================================

# Read log entries from the input file
logs = read_logs("logs.txt")

# Stop execution if no logs could be loaded
if not logs:
    print("No logs available to analyze.")
    exit()

# Count failed login attempts by IP and username
failed_ips, failed_users = count_failed_attempts(logs)

# Identify suspicious IP addresses and usernames
suspicious_ips = detect_suspicious_activity(failed_ips)
suspicious_users = detect_suspicious_activity(failed_users)

# Generate the final security report
generate_report(
    logs,
    failed_ips,
    failed_users,
    suspicious_ips,
    suspicious_users,
)

print("Analysis complete!")

